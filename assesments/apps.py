"""Configuration for the assessments application.

Registers the assessments app and signal handlers for notifications.
"""
from django.apps import AppConfig


class AssesmentsConfig(AppConfig):
    """App configuration for assignments, quizzes, and submissions.
    
    Configures the assessments app and automatically imports signal handlers
    for sending notification emails when assignments are graded or quizzes submitted.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assesments'

    def ready(self):
        """Initialize signal handlers when app is ready.
        
        Imports signal handlers to enable automatic email notifications.
        """
        import assesments.signals

   