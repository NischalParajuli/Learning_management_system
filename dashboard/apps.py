"""Configuration for the dashboard application.

Registers the dashboard app and its configuration.
"""
from django.apps import AppConfig


class DashboardConfig(AppConfig):
    """App configuration for administrative dashboards.
    
    Configures the dashboard app which provides statistics and reporting
    endpoints for administrators and sponsors.
    """
    name = 'dashboard'
