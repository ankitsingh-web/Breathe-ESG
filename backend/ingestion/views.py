import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import UploadedFile, EmissionRecord, Tenant
from .serializers import EmissionRecordSerializer
from .utils import normalize_unit, calculate_emission, detect_anomaly


class FileUploadView(APIView):

    def post(self, request):
        uploaded_file = request.FILES.get('file')
        source_type = request.data.get('source_type')

        if not uploaded_file or not source_type:
            return Response(
                {'detail': 'file and source_type are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        tenant, _ = Tenant.objects.get_or_create(name='Demo Company')

        stored_file = UploadedFile.objects.create(
            tenant=tenant,
            source_type=source_type,
            file=uploaded_file,
            uploaded_by='admin'
        )

        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file)

        for _, row in df.iterrows():
            raw_value = float(row['value'])
            raw_unit = row['unit']
            normalized_value, normalized_unit = normalize_unit(raw_value, raw_unit)
            factor, emission = calculate_emission(row['activity_type'], normalized_value)

            EmissionRecord.objects.create(
                tenant=tenant,
                uploaded_file=stored_file,
                source_type=source_type,
                scope=row['scope'],
                activity_type=row['activity_type'],
                raw_unit=raw_unit,
                normalized_unit=normalized_unit,
                raw_value=raw_value,
                normalized_value=normalized_value,
                emission_factor=factor,
                emission_kg_co2e=emission,
                record_date=row['record_date'],
                anomaly_flag=detect_anomaly(normalized_value)
            )

        stored_file.processing_status = 'COMPLETED'
        stored_file.save()

        return Response({'message': 'File processed successfully'}, status=status.HTTP_201_CREATED)


class EmissionRecordListView(APIView):

    def get(self, request):
        queryset = EmissionRecord.objects.all().order_by('-created_at')
        serializer = EmissionRecordSerializer(queryset, many=True)
        return Response(serializer.data)


class ApproveRecordView(APIView):

    def patch(self, request, pk):
        record = get_object_or_404(EmissionRecord, pk=pk)
        record.status = 'APPROVED'
        record.save()
        return Response({'message': 'Record approved'}, status=status.HTTP_200_OK)
