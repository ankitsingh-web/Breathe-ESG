from django.db import models
from simple_history.models import HistoricalRecords


class Tenant(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DataSource(models.TextChoices):
    SAP = 'SAP', 'SAP'
    UTILITY = 'UTILITY', 'UTILITY'
    TRAVEL = 'TRAVEL', 'TRAVEL'


class EmissionScope(models.TextChoices):
    SCOPE1 = 'SCOPE1', 'Scope 1'
    SCOPE2 = 'SCOPE2', 'Scope 2'
    SCOPE3 = 'SCOPE3', 'Scope 3'


class UploadedFile(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    source_type = models.CharField(max_length=50, choices=DataSource.choices)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.CharField(max_length=255)
    processing_status = models.CharField(max_length=50, default='PENDING')

    def __str__(self):
        return f'{self.source_type} - {self.id}'


class EmissionRecord(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    uploaded_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    source_type = models.CharField(max_length=50)
    scope = models.CharField(max_length=50, choices=EmissionScope.choices)
    activity_type = models.CharField(max_length=255)
    raw_unit = models.CharField(max_length=50)
    normalized_unit = models.CharField(max_length=50)
    raw_value = models.FloatField()
    normalized_value = models.FloatField()
    emission_factor = models.FloatField(default=0)
    emission_kg_co2e = models.FloatField(default=0)
    record_date = models.DateField()
    status = models.CharField(max_length=50, default='PENDING')
    anomaly_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.activity_type
