from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import ShareToken
from records.models import Record
from records.serializers import RecordTimelineSerializer
from records.pagination import StandardResultsSetPagination
from django.utils import timezone
import logging
logger = logging.getLogger(__name__)

import uuid
from django.core.exceptions import ValidationError

class GenerateShareTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        record_id = request.data.get('record_id')
        record = None

        if record_id:
            try:
                record_uuid = uuid.UUID(record_id)
                record = Record.objects.get(id=record_uuid, user=request.user)
            except (ValueError, ValidationError, Record.DoesNotExist):
                return Response(
                    {"error": "Record not found or access denied."},
                    status=status.HTTP_404_NOT_FOUND
                )

            ShareToken.objects.filter(user=request.user, record=record).delete()
        else:
            ShareToken.objects.filter(user=request.user, record__isnull=True).delete()

        share_token = ShareToken.objects.create(user=request.user, record=record)

        share_url = request.build_absolute_uri(f"/share/{share_token.token}/")

        logger.info(
            f"Share token generated | user_id={request.user.id} | token={share_token.token}"
        )

        return Response({
            "token": share_token.token,
            "share_url": share_url,
            "expires_at": share_token.expires_at,
            "record_id": share_token.record.id if share_token.record else None
        }, status=status.HTTP_201_CREATED)


class AccessSharedRecordsView(APIView):
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

    def get(self, request, token):
        try:
            share_token = ShareToken.objects.get(token=token)
        except ShareToken.DoesNotExist:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_404_NOT_FOUND)

        if not share_token.is_valid():
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_404_NOT_FOUND)

        # ✅ Logging after validation
        ip = request.META.get('REMOTE_ADDR', 'Unknown IP')
        logger.info(
            f"Share token accessed | token_owner_id={share_token.user.id} | token={share_token.token} | ip={ip}"
        )

        # ✅ Selective sharing logic
        if share_token.record and share_token.record.user_id == share_token.user_id:
            # 🔥 Better: skip pagination for single record
            serializer = RecordTimelineSerializer(
                [share_token.record],
                many=True,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        # 🔁 Normal flow (multiple records)
        records = Record.objects.filter(user=share_token.user)\
            .select_related('blockchain_tx')\
            .order_by('-record_date', '-created_at')

        paginator = self.pagination_class()
        paginated_records = paginator.paginate_queryset(records, request, view=self)

        # ✅ SAFETY FIX (important)
        if paginated_records is not None:
            serializer = RecordTimelineSerializer(
                paginated_records,
                many=True,
                context={'request': request}
            )
            return paginator.get_paginated_response(serializer.data)

        # fallback (if pagination disabled)
        # fallback (if pagination disabled)
        serializer = RecordTimelineSerializer(records, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework import viewsets
from rest_framework.decorators import action
from .models import AccessRequest, AccessGrant
from .serializers import AccessRequestSerializer, AccessGrantSerializer

class AccessRequestViewSet(viewsets.ModelViewSet):
    serializer_class = AccessRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'DOCTOR':
            return AccessRequest.objects.filter(doctor=user).order_by('-created_at')
        return AccessRequest.objects.filter(patient=user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        patient_email = request.data.get('patient_email')
        if not patient_email:
            return Response({"error": "patient_email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            patient = User.objects.get(email=patient_email, role='PATIENT')
        except User.DoesNotExist:
            return Response({"error": "Patient with this email not found."}, status=status.HTTP_404_NOT_FOUND)

        if AccessRequest.objects.filter(doctor=request.user, patient=patient, status='Pending').exists():
            return Response({"error": "A pending request already exists for this patient."}, status=status.HTTP_400_BAD_REQUEST)

        access_request = AccessRequest.objects.create(
            doctor=request.user,
            patient=patient,
            reason=request.data.get('reason', '')
        )
        serializer = self.get_serializer(access_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        access_request = self.get_object()
        if access_request.patient != request.user:
            return Response({"error": "Unauthorized"}, status=403)
        
        access_request.status = 'Approved'
        access_request.save()

        # Create Grant automatically
        AccessGrant.objects.get_or_create(patient=request.user, doctor=access_request.doctor)
        return Response({"status": "Approved"})

    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        access_request = self.get_object()
        if access_request.patient != request.user:
            return Response({"error": "Unauthorized"}, status=403)
        access_request.status = 'Declined'
        access_request.save()
        return Response({"status": "Declined"})

class AccessGrantViewSet(viewsets.ModelViewSet):
    serializer_class = AccessGrantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'DOCTOR':
            return AccessGrant.objects.filter(doctor=user).order_by('-created_at')
        return AccessGrant.objects.filter(patient=user).order_by('-created_at')

class GrantedPatientRecordsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, patient_id):
        if not AccessGrant.objects.filter(doctor=request.user, patient_id=patient_id).exists():
            return Response({"error": "Access denied. Patient has not granted you access."}, status=status.HTTP_403_FORBIDDEN)
            
        records = Record.objects.filter(user_id=patient_id).select_related('blockchain_tx').order_by('-record_date', '-created_at')
        from records.serializers import RecordTimelineSerializer
        serializer = RecordTimelineSerializer(records, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
