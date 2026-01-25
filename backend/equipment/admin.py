from django.contrib import admin
from equipment.models import Equipment, DataUpload, UserProfile


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature', 'created_at')
    list_filter = ('equipment_type', 'created_at')
    search_fields = ('equipment_name',)
    ordering = ('-created_at',)


@admin.register(DataUpload)
class DataUploadAdmin(admin.ModelAdmin):
    list_display = ('filename', 'user', 'uploaded_at', 'total_records', 'avg_flowrate')
    list_filter = ('uploaded_at', 'user')
    search_fields = ('filename',)
    ordering = ('-uploaded_at',)
    readonly_fields = ('uploaded_at',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
