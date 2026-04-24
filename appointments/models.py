import uuid
from django.db import models
from django.conf import settings

class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments', db_index=True)
    doctor_name = models.CharField(max_length=200)
    specialty = models.CharField(max_length=200, blank=True)
    appointment_date = models.DateField(db_index=True)
    appointment_time = models.TimeField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=50, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['appointment_date', 'appointment_time']

    def __str__(self):
        return f"{self.user.email} with {self.doctor_name} on {self.appointment_date}"
