"""Views for managing student and course sponsorships.

Provides REST API endpoints for sponsors to manage their sponsorships of
student enrollments and courses. Includes filtering and search capabilities.
"""

from django.shortcuts import render
from rest_framework import viewsets
from accounts.permissions import IsSponsor, IsAdmin
from .models import Sponsorship, CourseSponsor
from .serializer import SponsorshipSerializer, CourseSponsorSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class SponsorshipViewset(viewsets.ModelViewSet):
    """API viewset for managing student sponsorships.
    
    Allows sponsors to sponsor student enrollments. Provides filtering by
    amount, date, and status, plus search by course/student/sponsor.
    """
    queryset = Sponsorship.objects.all()
    serializer_class = SponsorshipSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['amount', 'sponsored_at', 'status']
    search_fields = ['enrollment__course__title', 'enrollment__student__username', 'sponsor__username']

    def get_queryset(self):
        """Filter sponsorships based on user role.
        
        Admin users see all sponsorships. Sponsors see only their own.
        
        Returns:
            QuerySet: Filtered sponsorships.
        """
        user = self.request.user

        if user.role == 'admin':
            return Sponsorship.objects.all()
        
        if user.role == 'sponsor':
            return Sponsorship.objects.filter(sponsor=user)
        
        return Sponsorship.objects.none()

    def get_permissions(self):
        """Determine required permissions based on action.
        
        Returns:
            list: Permission classes required for the action.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsSponsor(), IsAdmin()]
        return [IsAdmin()]

    def perform_create(self, serializer):
        """Set the current user as the sponsoring sponsor.
        
        Args:
            serializer: Sponsorship serializer instance.
        """
        serializer.save(sponsor=self.request.user)


class CourseSponsorViewset(viewsets.ModelViewSet):
    """API viewset for managing course sponsorships.
    
    Allows sponsors to sponsor entire courses. Provides filtering and
    search capabilities similar to student sponsorships.
    """
    queryset = CourseSponsor.objects.all()
    serializer_class = CourseSponsorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['amount', 'sponsored_at', 'status']
    search_fields = ['enrollment__course__title', 'sponsor__username']

    def get_queryset(self):
        """Filter course sponsorships based on user role.
        
        Admin users see all sponsorships. Sponsors see only their own.
        
        Returns:
            QuerySet: Filtered sponsorships.
        """
        user = self.request.user

        if user.role == 'admin':
            return CourseSponsor.objects.all()
        
        if user.role == 'sponsor':
            return CourseSponsor.objects.filter(sponsor=user)
        
        return CourseSponsor.objects.none()

    def get_permissions(self):
        """Determine required permissions based on action.
        
        Returns:
            list: Permission classes required for the action.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsSponsor(), IsAdmin()]
        return [IsAdmin()]
    
    def perform_create(self, serializer):
        """Set the current user as the sponsoring sponsor.
        
        Args:
            serializer: CourseSponsor serializer instance.
        """
        serializer.save(sponsor=self.request.user)