from django.urls import path
from .views import GenerateDownloadLinkView, SecureDownloadView, UploadFileView,FileListView

urlpatterns = [
    path('upload/', UploadFileView.as_view(), name='file-upload'),
     path('list/', FileListView.as_view(), name='file-list'),
     path('generate-download-link/<int:file_id>/', GenerateDownloadLinkView.as_view(), name='generate-download'),
    path('download/', SecureDownloadView.as_view(), name='download-file'),
]
