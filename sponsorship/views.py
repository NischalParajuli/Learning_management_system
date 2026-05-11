from django.shortcuts import render
from rest_framework import viewsets
from accounts.permissions import IsSponsor , IsAdmin
from .models import Sponsorship , CourseSponsor
from .serializer import SponsorshipSerializer , CourseSponsorSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


# Create your views here.
class SponsorshipViewset(viewsets.ModelViewSet):
  queryset = Sponsorship.objects.all()
  serializer_class = SponsorshipSerializer
  filter_backends = [DjangoFilterBackend,SearchFilter]
  filterset_fields = ['amount','sponsored_at','status']
  search_fields = ['enrollment__course__title','enrollment__student__username','sponsor__username']

  def get_queryset(self):
    user = self.request.user

    if user.role == 'admin':
      return Sponsorship.objects.all()
    
    if user.role == 'sponsor':
      return Sponsorship.objects.filter(sponsor = user)
    
    return Sponsorship.objects.none()



  def get_permissions(self):
    if self.action in ['create','update','partial_update','destroy']:
      return[IsSponsor() , IsAdmin()]
    return[IsAdmin()]
  

  def perform_create(self, serializer):
    serializer.save(sponsor=self.request.user)


class CourseSponsorViewset(viewsets.ModelViewSet):
  queryset = CourseSponsor.objects.all()
  serializer_class = CourseSponsorSerializer
  filter_backends = [DjangoFilterBackend,SearchFilter]
  filterset_fields = ['amount','sponsored_at','status']
  search_fields = ['enrollment__course__title','sponsor__username']


  def get_queryset(self):
    user = self.request.user

    if user.role == 'admin':
      return CourseSponsor.objects.all()
    
    if user.role == 'sponsor':
      return CourseSponsor.objects.filter(sponsor = user)
    
    return CourseSponsor.objects.none()
  

  def get_permissions(self):
    if self.action in ['create','update','partial_update','destroy']:
      return[IsSponsor() , IsAdmin()]
    return[IsAdmin]
  
  def perform_create(self, serializer):
    serializer.save(sponsor=self.request.user)

