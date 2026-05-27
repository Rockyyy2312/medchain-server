from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    patient_id = serializers.UUIDField(source='user.id', read_only=True)
    patient_email = serializers.EmailField(source='user.email', read_only=True)
    patient_first_name = serializers.CharField(source='user.first_name', read_only=True)
    patient_last_name = serializers.CharField(source='user.last_name', read_only=True)
    doctor_id = serializers.UUIDField(source='doctor.id', read_only=True, default=None)

    class Meta:
        model = Appointment
        fields = (
            'id', 'doctor_name', 'specialty', 'appointment_date', 'appointment_time',
            'reason', 'status', 'created_at',
            'patient_id', 'patient_email', 'patient_first_name', 'patient_last_name',
            'doctor_id',
        )
        read_only_fields = (
            'id', 'created_at', 'status',
            'patient_id', 'patient_email', 'patient_first_name', 'patient_last_name',
            'doctor_id',
        )
