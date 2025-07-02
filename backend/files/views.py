from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import File

import os
import re
import requests
from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import File

class UploadFileView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if not user.is_ops_user:
            return Response({"error": "Only Ops users can upload files."}, status=403)

        file_url = request.data.get("file_url")

        if not file_url:
            return Response({"error": "file_url is required."}, status=400)

        allowed_extensions = ['.pptx', '.docx', '.xlsx']

        try:
            # ✅ Handle Google Docs/Sheets/Slides
            if "docs.google.com" in file_url:
                match = re.search(r"/d/([a-zA-Z0-9_-]+)", file_url)
                if not match:
                    return Response({"error": "Invalid Google Docs URL format."}, status=400)
                file_id = match.group(1)

                if "document" in file_url:
                    file_url = f"https://docs.google.com/document/d/{file_id}/export?format=docx"
                    filename = f"{file_id}.docx"
                elif "spreadsheets" in file_url:
                    file_url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx"
                    filename = f"{file_id}.xlsx"
                elif "presentation" in file_url:
                    file_url = f"https://docs.google.com/presentation/d/{file_id}/export?format=pptx"
                    filename = f"{file_id}.pptx"
                else:
                    return Response({"error": "Unsupported Google Docs file type."}, status=400)

            elif "drive.google.com" in file_url:
                match = re.search(r"/d/([a-zA-Z0-9_-]+)", file_url)
                if match:
                    file_id = match.group(1)
                    file_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                    filename = f"{file_id}"
                else:
                    return Response({"error": "Invalid Google Drive URL format."}, status=400)

            else:
                # fallback for direct links
                filename = os.path.basename(file_url.split("?")[0])

            # ✅ Validate file extension
            if not any(filename.lower().endswith(ext) for ext in allowed_extensions):
                return Response({"error": "Invalid file type. Only .pptx, .docx, .xlsx allowed."}, status=400)

            # ✅ Download the file
            response = requests.get(file_url)
            response.raise_for_status()

            # ✅ Save to DB
            content_file = ContentFile(response.content, name=filename)
            File.objects.create(uploaded_by=user, file=content_file)

            return Response({"message": "File fetched and uploaded successfully."}, status=201)

        except requests.RequestException:
            return Response({"error": "Failed to fetch file from the provided URL."}, status=400)
        


        
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import File
from users.models import CustomUser

class FileListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_client_user:
            return Response({"error": "Only client users can view the file list."}, status=403)

        files = File.objects.all().values('id', 'file', 'uploaded_by__username', 'uploaded_at')
        return Response(files, status=200)




from itsdangerous import URLSafeSerializer
from django.conf import settings

serializer = URLSafeSerializer(settings.SECRET_KEY, salt="download-salt")

class GenerateDownloadLinkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id):
        user = request.user
        if not user.is_client_user:
            return Response({"error": "Only client users can download files."}, status=403)

        token = serializer.dumps({"file_id": file_id, "user_id": user.id})
        download_url = request.build_absolute_uri(
            reverse('download-file') + f'?token={token}'
        )
        return Response({"download_url": download_url})



from django.http import FileResponse, Http404

class SecureDownloadView(APIView):
    def get(self, request):
        token = request.GET.get("token")
        try:
            data = serializer.loads(token)
            file_id = data["file_id"]
            user_id = data["user_id"]

            user = request.user
            if not user.is_authenticated or user.id != user_id or not user.is_client_user:
                return Response({"error": "Unauthorized access."}, status=403)

            file = File.objects.get(id=file_id)
            return FileResponse(file.file.open(), as_attachment=True)

        except Exception:
            raise Http404("Invalid or expired token.")
