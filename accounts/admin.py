from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom admin configuration for User model.
    
    Extends Django's UserAdmin to include the custom 'role' field
    for role-based access control management.
    """
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
