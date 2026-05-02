from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import *
from .serializer import *
from accounts.permissions import IsAdmin ,IsInstructor , IsStudent ,IsSponsor
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

# Create your views here.



class AssignmentView(viewsets.ModelViewSet):
  queryset = Assignment.objects.all()
  filter_backends = [DjangoFilterBackend,SearchFilter]
  search_fields = ['title','course__title','instructor__username']
  serializer_class = AssignmentSerializer

  def get_permissions(self):
    if self.action == 'create':
      return[IsInstructor()] or [IsAdmin()]
    elif self.action in ['update','partial_update','destroy']:
      return[IsAdmin()]  or [IsInstructor()]
    return[IsAuthenticated()]

  def get_queryset(self):
    user = self.request.user

    if user.role == 'admin':
      return Assignment.objects.all()
    
    if user.role == 'instructor':
      return Assignment.objects.all(instructor = user)
    
    return Assignment.objects.all()


  def perform_create(self, serializer):
    serializer.save(instructor = self.request.user) 



class SubmissionView(viewsets.ModelViewSet):
  queryset = Submission.objects.all()
  serializer_class = SubmissionSerializer
  
  def get_permissions(self):
    if self.action == 'create':
      return[IsStudent()]
    elif self.action in ['update','partial_update']:
      return[IsStudent()]
    elif self.action == 'destroy':
      return [IsAdmin()]
    return[IsAuthenticated()]
  

  def get_queryset(self):
    user = self.request.user

    if user.role == 'admin':
      return Submission.objects.all()
    
    if user.role == 'instructor':
      return Submission.objects.filter(assignment__course__instructor = user)

    if user.role == 'student':
      return Submission.objects.filter(student=user)
    
    return Submission.objects.none()
  

  def perform_create(self, serializer):
    serializer.save(student=self.request.user)