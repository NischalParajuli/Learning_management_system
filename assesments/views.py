"""Views for assignments, submissions, and email functionality."""

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import *
from .serializer import *
from accounts.permissions import IsAdmin, IsInstructor, IsStudent
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.core.mail import send_mail
from django.http import HttpResponse
from courses.models import Enrollment
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser


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


class QuizView(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'course__title', 'instructor__username']

    def get_permissions(self):
        if self.action == 'create':
            return [IsInstructor()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsInstructor()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'admin':
            return Quiz.objects.all()

        if user.role == 'instructor':
            return Quiz.objects.filter(instructor=user)

        if user.role == 'student':
            enrolled_courses = Enrollment.objects.filter(
                student=user
            ).values_list('course', flat=True)
            return Quiz.objects.filter(course__in=enrolled_courses)

        return Quiz.objects.none()

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)


class QuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsInstructor()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'admin':
            return Question.objects.all()

        if user.role == 'instructor':
            return Question.objects.filter(quiz__instructor=user)

        if user.role == 'student':
            enrolled_courses = Enrollment.objects.filter(
                student=user
            ).values_list('course', flat=True)
            return Question.objects.filter(quiz__course__in=enrolled_courses)

        return Question.objects.none()

    def _check_quiz_ownership(self, quiz):
        if self.request.user.role == 'instructor' and quiz.instructor != self.request.user:
            raise PermissionDenied("You can only manage questions for your own quizzes.")

    def perform_create(self, serializer):
        self._check_quiz_ownership(serializer.validated_data['quiz'])
        serializer.save()

    def perform_update(self, serializer):
        self._check_quiz_ownership(serializer.instance.quiz)
        serializer.save()

    def perform_destroy(self, instance):
        self._check_quiz_ownership(instance.quiz)
        instance.delete()


class QuizSubmissionView(viewsets.ModelViewSet):
    queryset = QuizSubmission.objects.all()
    serializer_class = QuizSubmissionSerializer
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    def get_permissions(self):
        if self.action == 'create':
            return [IsStudent()]
        elif self.action == 'destroy':
            return [IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'admin':
            return QuizSubmission.objects.all()

        if user.role == 'instructor':
            return QuizSubmission.objects.filter(quiz__instructor=user)

        if user.role == 'student':
            return QuizSubmission.objects.filter(student=user)

        return QuizSubmission.objects.none()


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