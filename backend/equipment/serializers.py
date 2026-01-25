from rest_framework import serializers
from django.contrib.auth.models import User
from equipment.models import Equipment, DataUpload, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ('id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature', 'created_at')
        read_only_fields = ('id', 'created_at')


class DataUploadSerializer(serializers.ModelSerializer):
    equipment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = DataUpload
        fields = ('id', 'filename', 'uploaded_at', 'total_records', 'avg_flowrate', 
                  'avg_pressure', 'avg_temperature', 'equipment_count')
        read_only_fields = ('id', 'uploaded_at')
    
    def get_equipment_count(self, obj):
        return obj.equipment_items.count()


class DataSummarySerializer(serializers.Serializer):
    """Serializer for data summary statistics"""
    total_count = serializers.IntegerField()
    avg_flowrate = serializers.FloatField()
    avg_pressure = serializers.FloatField()
    avg_temperature = serializers.FloatField()
    equipment_type_distribution = serializers.DictField()
    recent_uploads = DataUploadSerializer(many=True, read_only=True)


class UploadCSVSerializer(serializers.Serializer):
    """Serializer for CSV file upload"""
    file = serializers.FileField()
    
    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("File must be a CSV file")
        if value.size > 5242880:  # 5MB
            raise serializers.ValidationError("File size must be less than 5MB")
        return value
