from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully", "user_id": user.id, "role": user.role}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        # exclude password from response
        data = dict(serializer.data)
        data.pop('password', None)
        return Response(data, status=status.HTTP_200_OK)

from sharing.models import AccessGrant
from appointments.models import Appointment
from records.models import Record

class DoctorAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'DOCTOR':
            return Response({"error": "Only doctors can view analytics."}, status=status.HTTP_403_FORBIDDEN)

        # 1. Total unique patients the doctor has an active grant for
        total_patients = AccessGrant.objects.filter(doctor=request.user).values('patient').distinct().count()

        # 2. Total appointments
        total_appointments = Appointment.objects.filter(doctor=request.user).count()

        # 3. Total records accessible
        accessible_records = Record.objects.filter(grants__doctor=request.user).distinct()
        total_records = accessible_records.count()

        # 4. Breakdown of record types for charts
        # Since we use free-form record_type in Record model, we group by it
        from django.db.models import Count
        record_distribution = accessible_records.values('record_type').annotate(count=Count('id'))
        
        # Build dictionary for the donut chart
        types_breakdown = {}
        for item in record_distribution:
            rt = item['record_type'] or "Uncategorized"
            types_breakdown[rt] = item['count']

        return Response({
            "total_patients": total_patients,
            "total_appointments": total_appointments,
            "total_records": total_records,
            "record_types": types_breakdown
        }, status=status.HTTP_200_OK)


class DoctorListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        doctors = User.objects.filter(role='DOCTOR')
        data = []
        for doc in doctors:
            first = doc.first_name or ''
            last = doc.last_name or ''
            full_name = f"{first} {last}".strip()
            if not full_name:
                full_name = doc.email.split('@')[0]
            
            if not full_name.lower().startswith('dr.'):
                full_name = f"Dr. {full_name}"

            specialty = "General Medicine"
            email_lower = doc.email.lower()
            if 'harpreet' in email_lower:
                specialty = "Cardiology"
            elif 'subramaniam' in email_lower:
                specialty = "Dermatology"
            elif 'rohan' in email_lower:
                specialty = "Neurology"
            elif 'alok' in email_lower:
                specialty = "Orthopedics"
            elif 'shah' in email_lower:
                specialty = "General Medicine"
            elif 'laukik' in email_lower:
                specialty = "Pulmonology"
            elif 'rocky' in email_lower:
                specialty = "Cardiology"
            
            data.append({
                "id": str(doc.id),
                "email": doc.email,
                "name": full_name,
                "specialty": specialty
            })
        return Response(data, status=status.HTTP_200_OK)

