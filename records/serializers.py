from rest_framework import serializers
from django.utils import timezone
from .models import Record

class RecordUploadSerializer(serializers.ModelSerializer):
    record_date = serializers.DateField(required=False, default=timezone.localdate)

    class Meta:
        model = Record
        fields = ('id', 'record_type', 'record_date', 'doctor_name', 'file_url')
        read_only_fields = ('id',)


class RecordTimelineSerializer(serializers.ModelSerializer):
    blockchain_status = serializers.SerializerMethodField()

    def get_blockchain_status(self, obj):
        return getattr(obj.blockchain_tx, 'status', 'PENDING')

    file_url = serializers.SerializerMethodField()
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file_url:
            return request.build_absolute_uri(obj.file_url.url)
        return None

    class Meta:
        model = Record
        fields = ('id', 'record_type', 'doctor_name', 'record_date', 'file_url', 'blockchain_status')
