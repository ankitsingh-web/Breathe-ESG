from django.urls import path
from .views import FileUploadView, EmissionRecordListView, ApproveRecordView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='upload-file'),
    path('records/', EmissionRecordListView.as_view(), name='records-list'),
    path('approve/<int:pk>/', ApproveRecordView.as_view(), name='approve-record'),
]
