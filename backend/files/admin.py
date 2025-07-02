from django.contrib import admin
from .models import File

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'uploaded_by', 'uploaded_at')
    list_filter = ('uploaded_by', 'uploaded_at')
    search_fields = ('file', 'uploaded_by__username')
