from django.db import models
from django.conf import settings

def upload_path(instance, filename):
    return f"uploads/{filename}"

class File(models.Model):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
