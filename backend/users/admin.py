from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # This shows in the user list table
    list_display = ('username', 'email', 'is_client_user', 'is_ops_user', 'is_active', 'email_verified')
    
    # These fields will be shown in the user detail page
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('is_client_user', 'is_ops_user', 'email_verified')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
