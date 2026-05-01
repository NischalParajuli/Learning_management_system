from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from accounts.permissions import IsAdmin
from .models import Course , Enrollment
from .serializer import CourseSerializer , EnrollmentSerializer
from .pagination import CoursePagination 
from django.shortcuts import render
from accounts.permissions import IsAdmin , IsInstructor


class CourseViewset(viewsets.ModelViewSet):
  queryset = Course.objects.all()
  serializer_class = CourseSerializer
  pagination_class = CoursePagination


  filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
  search_fields= ['title','instructor__username','difficulty']
  filterset_fields = ['difficulty','is_published']
  ordering_fields = ['title','created_at']


  def get_permissions(self):
        if self.action in ['create']:
          return[IsInstructor()]
        elif self.action in ['update','partial_update','destroy']:
          return[IsAdmin()] 
        return[IsAuthenticated()] 
  
  def perform_create(self, serializer):
     serializer.save(instructor=self.request.user)
  

class EnrollmentViewset(viewsets.ModelViewSet):
  queryset = Enrollment.objects.all()
  serializer_class = EnrollmentSerializer

  def get_queryset(self):
    user = self.request.user
    if user.role == 'admin':
       return Enrollment.objects.all ()
    return Enrollment.objects.filter(student = user)

  def get_permissions(self):
    if self.action == 'destroy':
      return [IsAdmin()]
    return [IsAuthenticated()] 

  def perform_create(self,serializer):
     serializer.save(student=self.request.user)

  