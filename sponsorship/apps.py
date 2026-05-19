"""Configuration for the sponsorship application.

Registers the sponsorship app and its configuration.
"""
from django.apps import AppConfig


class SponsorshipConfig(AppConfig):
    """App configuration for student and course sponsorships.
    
    Configures the sponsorship app which handles financial sponsorships
    for student enrollments and entire courses.
    """
    name = 'sponsorship'
