"""Configuration for the accounts application.

Registers the accounts app and its configuration.
"""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """App configuration for user accounts and authentication.
    
    Configures the accounts app which handles user models,
    authentication, and authorization.
    """
    name = 'accounts'
