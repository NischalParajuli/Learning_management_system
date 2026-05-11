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
from django.core.mail import send_mail
from django.http import HttpResponse

# Create your views here.



class AssignmentView(viewsets.ModelViewSet):
  queryset = Assignment.objects.all()
  filter_backends = [DjangoFilterBackend,SearchFilter]
  search_fields = ['title','course__title','instructor__username']
  serializer_class = AssignmentSerializer

  def get_permissions(self):
    if self.action == 'create':
      return[IsInstructor() , IsAdmin()]
    elif self.action in ['update','partial_update','destroy']:
      return[IsAdmin() , IsInstructor()]
    return[IsAuthenticated()]

  def get_queryset(self):
    user = self.request.user

    if user.role == 'admin':
      return Assignment.objects.all()
    
    if user.role == 'instructor':
      return Assignment.objects.filter(instructor = user)
    
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
    return[IsAdmin()]
  

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


def send_email(request):
  try:
    print("Sending Email")
    send_mail(
      subject='Email from Django',
      message='This is an email sent from Django application.',
      from_email='reply@demomailtrap.co',
      recipient_list=['parajulig113@gmail.com'],
      fail_silently=False,
      html_message='<p>This is a <strong>HTML test email</strong> sent from Django application.</p>',
    )

    return HttpResponse("Email test Sucessfull")
  except Exception as e :
    return HttpResponse(f'Failed to send email : {str(e)}')




