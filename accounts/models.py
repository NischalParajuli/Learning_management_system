"""User models for the accounts application.

Defines custom user model extending Django's AbstractUser with role-based
access control for different user types in the learning management system.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model with role-based access control.
    
    Extends Django's AbstractUser to add a role field that determines
    user permissions and access levels in the system.
    
    Attributes:
        role: The user's role in the system (admin, instructor, student, sponsor).
    """
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
        ('sponsor', 'Sponsor')
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
