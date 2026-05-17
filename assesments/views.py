"""Views for assignments, submissions, and email functionality."""

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializer import *
from accounts.permissions import IsAdmin, IsInstructor, IsStudent
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.core.mail import send_mail
from django.http import HttpResponse
from courses.models import Enrollment


class AssignmentView(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'course__title', 'instructor__username']
    serializer_class = AssignmentSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsStudent()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated()]
        elif self.action == 'destroy':
            return [IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'admin':
            return Assignment.objects.all()

        if user.role == 'instructor':
            return Assignment.objects.filter(instructor=user)

        if user.role == 'student':
            enrolled_courses = Enrollment.objects.filter(
                student=user
            ).values_list('course', flat=True)
            print(f"Student: {user.username}")       
            print(f"Enrolled courses: {list(enrolled_courses)}")
            assignments = Assignment.objects.filter(course__in=enrolled_courses)
            print(f"Assignments: {list(assignments)}")
            return Assignment.objects.filter(course__in=enrolled_courses)  

        return Assignment.objects.none()

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)


class SubmissionView(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsStudent()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated()]
        elif self.action == 'destroy':
            return [IsAdmin()]
        return [IsAuthenticated()] 

    def get_queryset(self):
        user = self.request.user

        if user.role == 'admin':
            return Submission.objects.all()

        if user.role == 'instructor':
            return Submission.objects.filter(assignment__course__instructor=user)

        if user.role == 'student':
            return Submission.objects.filter(student=user)

        return Submission.objects.none()

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


def send_email(request):
    try:
        send_mail(
            subject='Email from Django',
            message='This is an email sent from Django application.',
            from_email='reply@demomailtrap.co',
            recipient_list=['parajulig113@gmail.com'],
            fail_silently=False,
            html_message='<p>This is a <strong>HTML test email</strong> sent from Django application.</p>',
        )
        return HttpResponse("Email test Sucessfull")
    except Exception as e:
        return HttpResponse(f'Failed to send email : {str(e)}')


def home(request):
    return render(request, 'home.html')