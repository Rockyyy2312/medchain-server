from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Appointment
from .serializers import AppointmentSerializer

from rest_framework.pagination import PageNumberPagination

class AppointmentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = AppointmentPagination

    def get_queryset(self):
        user = self.request.user
        status_filter = self.request.query_params.get('status', None)

        if user.role == 'DOCTOR':
            from django.db.models import Q
            first = user.first_name or ''
            last = user.last_name or ''

            # Primary: exact FK match (set at booking time when doctor account found)
            # Fallback: name-string match for records where doctor FK was not set
            name_q = Q()
            if first and last:
                name_q = Q(doctor_name__icontains=first) & Q(doctor_name__icontains=last)
            elif first:
                name_q = Q(doctor_name__icontains=first)
            elif last:
                name_q = Q(doctor_name__icontains=last)

            qs = Appointment.objects.filter(
                Q(doctor=user) | (name_q & Q(doctor__isnull=True))
            )
        else:
            qs = Appointment.objects.filter(user=user)

        if status_filter:
            qs = qs.filter(status=status_filter)

        return qs.order_by('appointment_date', 'appointment_time')

    def perform_create(self, serializer):
        doctor_name = serializer.validated_data.get('doctor_name', '')
        clean_name = doctor_name.replace('Dr. ', '').replace('Dr.', '').strip()
        
        doctor_user = None
        if clean_name:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            parts = clean_name.split(' ')
            if len(parts) >= 2:
                first = parts[0]
                last = ' '.join(parts[1:])
                doctor_user = User.objects.filter(role='DOCTOR', first_name__iexact=first, last_name__iexact=last).first()
            if not doctor_user:
                doctor_user = User.objects.filter(role='DOCTOR', first_name__icontains=clean_name).first() or \
                              User.objects.filter(role='DOCTOR', last_name__icontains=clean_name).first()
                              
        serializer.save(user=self.request.user, doctor=doctor_user)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        appointment = self.get_object()
        
        # Either the booking patient or the doctor can confirm
        is_allowed = (appointment.user == request.user or appointment.doctor == request.user)
        if not is_allowed and request.user.role == 'DOCTOR':
            first = request.user.first_name or ''
            last = request.user.last_name or ''
            if first and last and first in appointment.doctor_name and last in appointment.doctor_name:
                is_allowed = True
                
        if not is_allowed:
            return Response({"error": "Only the booking patient or the assigned doctor can confirm."}, status=status.HTTP_403_FORBIDDEN)
            
        if appointment.status != 'Pending':
            return Response({"error": f"Cannot confirm an appointment with status '{appointment.status}'."}, status=status.HTTP_400_BAD_REQUEST)
        
        appointment.status = 'Confirmed'
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        
        # Either the booking patient or the doctor can cancel
        is_allowed = (appointment.user == request.user or appointment.doctor == request.user)
        if not is_allowed and request.user.role == 'DOCTOR':
            first = request.user.first_name or ''
            last = request.user.last_name or ''
            if first and last and first in appointment.doctor_name and last in appointment.doctor_name:
                is_allowed = True
                
        if not is_allowed:
            return Response({"error": "Only the booking patient or the assigned doctor can cancel."}, status=status.HTTP_403_FORBIDDEN)
            
        if appointment.status == 'Cancelled':
            return Response({"error": "Appointment is already cancelled."}, status=status.HTTP_400_BAD_REQUEST)
        
        appointment.status = 'Cancelled'
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)
