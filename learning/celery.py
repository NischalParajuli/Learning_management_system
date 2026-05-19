"""Celery configuration for the learning management system.

Configures Celery for asynchronous task processing including
periodic tasks for reminders and progress reports.
"""
import os
from celery import Celery


# Set the default Django settings module for the Celery program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learning.settings')

# Create Celery application instance
app = Celery('learning')

# Load configuration from Django settings with CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered apps
app.autodiscover_tasks()