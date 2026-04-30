from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from accounts.permissions import IsAdmin
from .models import Course
from .serializer import CourseSerializer , EnrollmentSerializer
from .pagination import CoursePagination 
from django.shortcuts import render


class CourseViewset(viewsets.ModelViewSet):
  queryset = Course.objects.all()
  serializer_class = CourseSerializer
  pagination_class = CoursePagination


  filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
  search_fields= ['title','instructor','difficulty']
  filterset_fields = ['difficulty','is_published']
  ordering_fields = ['title','created_at']


  def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
          return [IsAdmin()]
        return [IsAuthenticated()]  
