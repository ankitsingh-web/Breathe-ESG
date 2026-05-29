from django.contrib import admin
from .models import Tenant, UploadedFile, EmissionRecord


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'tenant', 'source_type', 'uploaded_by', 'processing_status', 'uploaded_at')
    list_filter = ('source_type', 'processing_status')


@admin.register(EmissionRecord)
class EmissionRecordAdmin(admin.ModelAdmin):
    list_display = ('activity_type', 'scope', 'emission_kg_co2e', 'status', 'anomaly_flag', 'created_at')
    list_filter = ('scope', 'status', 'anomaly_flag')
