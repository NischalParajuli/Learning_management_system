"""Configuration for the courses application.

Registers the courses app and its configuration.
"""
from django.apps import AppConfig


class CoursesConfig(AppConfig):
    """App configuration for courses and enrollments.
    
    Configures the courses app which handles course creation,
    management, and student enrollments.
    """
    name = 'courses'
