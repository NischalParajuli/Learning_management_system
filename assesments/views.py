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
    """API viewset for managing course assignments.
    
    Provides CRUD operations for assignments with role-based filtering.
    Only students can create, instructors/admins can update, only admins can delete.
    Filters assignments by user role and course enrollment.
    """
    queryset = Assignment.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'course__title', 'instructor__username']
    serializer_class = AssignmentSerializer

    def get_permissions(self):
        """Determine required permissions based on action.
        
        Returns:
            list: Permission classes required for the action.
        """
        if self.action == 'create':
            return [IsStudent()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated()]
        elif self.action == 'destroy':
            return [IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Filter assignments based on user role.
        
        Admins see all assignments. Instructors see their own assignments.
        Students see assignments from courses they're enrolled in.
        
        Returns:
            QuerySet: Filtered assignments.
        """
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
        """Set the current user as the assignment instructor.
        
        Args:
            serializer: Assignment serializer instance.
        """
        serializer.save(instructor=self.request.user)


class SubmissionView(viewsets.ModelViewSet):
    """API viewset for managing assignment submissions.
    
    Provides CRUD operations for student submissions with role-based filtering.
    Students create/update their own submissions, instructors grade them.
    """
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def get_permissions(self):
        """Determine required permissions based on action.
        
        Returns:
            list: Permission classes required for the action.
        """
        if self.action == 'create':
            return [IsStudent()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated()]
        elif self.action == 'destroy':
            return [IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Filter submissions based on user role.
        
        Admins see all submissions. Instructors see submissions for their courses.
        Students see only their own submissions.
        
        Returns:
            QuerySet: Filtered submissions.
        """
        user = self.request.user

        if user.role == 'admin':
            return Submission.objects.all()

        if user.role == 'instructor':
            return Submission.objects.filter(assignment__course__instructor=user)

        if user.role == 'student':
            return Submission.objects.filter(student=user)

        return Submission.objects.none()

    def perform_create(self, serializer):
        """Set the current user as the student submitting.
        
        Args:
            serializer: Submission serializer instance.
        """
        serializer.save(student=self.request.user)


class QuizView(viewsets.ModelViewSet):
    """API viewset for managing course quizzes.
    
    Provides CRUD operations for quizzes with role-based access control.
    Only instructors can create/modify/delete quizzes. Includes search and filtering.
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'course__title', 'instructor__username']

    def get_permissions(self):
        """Determine required permissions based on action.
        
        Returns:
            list: Permission classes required for the action.
        """
        if self.action == 'create':
            return [IsInstructor()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsInstructor()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Filter quizzes based on user role.
        
        Admins see all quizzes. Instructors see their own quizzes.
        Students see quizzes from courses they're enrolled in.
        
        Returns:
            QuerySet: Filtered quizzes.
        """
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
        """Set the current user as the quiz instructor.
        
        Args:
            serializer: Quiz serializer instance.
        """
        serializer.save(instructor=self.request.user)


class QuestionView(viewsets.ModelViewSet):
    """API viewset for managing quiz questions.
    
    Provides CRUD operations for quiz questions with role-based access.
    Only instructors can create/modify/delete questions for their quizzes.
    Ensures instructors can only manage their own quizzes' questions.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        """Determine required permissions based on action.
        
        Returns:
            list: Permission classes required for the action.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsInstructor()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Filter questions based on user role.
        
        Admins see all questions. Instructors see questions in their quizzes.
        Students see questions in quizzes from courses they're enrolled in.
        
        Returns:
            QuerySet: Filtered questions.
        """
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
        """Verify that instructor owns the quiz before allowing modifications.
        
        Args:
            quiz: The quiz object to verify ownership of.
        
        Raises:
            PermissionDenied: If instructor doesn't own the quiz.
        """
        if self.request.user.role == 'instructor' and quiz.instructor != self.request.user:
            raise PermissionDenied("You can only manage questions for your own quizzes.")

    def perform_create(self, serializer):
        """Verify quiz ownership before creating a question.
        
        Args:
            serializer: Question serializer instance.
        """
        self._check_quiz_ownership(serializer.validated_data['quiz'])
        serializer.save()

    def perform_update(self, serializer):
        """Verify quiz ownership before updating a question.
        
        Args:
            serializer: Question serializer instance.
        """
        self._check_quiz_ownership(serializer.instance.quiz)
        serializer.save()

    def perform_destroy(self, instance):
        """Verify quiz ownership before deleting a question.
        
        Args:
            instance: Question instance to delete.
        """
        self._check_quiz_ownership(instance.quiz)
        instance.delete()


class QuizSubmissionView(viewsets.ModelViewSet):
    """API viewset for managing quiz submissions.
    
    Handles student quiz submission and answer recording. Automatically
    calculates scores. Only students can create, only admins can delete.
    """
    queryset = QuizSubmission.objects.all()
    serializer_class = QuizSubmissionSerializer
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    def get_permissions(self):
        """Determine required permissions based on action.
        
        Returns:
            list: Permission classes required for the action.
        """
        if self.action == 'create':
            return [IsStudent()]
        elif self.action == 'destroy':
            return [IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Filter quiz submissions based on user role.
        
        Admins see all submissions. Instructors see submissions for their quizzes.
        Students see only their own submissions.
        
        Returns:
            QuerySet: Filtered quiz submissions.
        """
        user = self.request.user

        if user.role == 'admin':
            return QuizSubmission.objects.all()

        if user.role == 'instructor':
            return QuizSubmission.objects.filter(quiz__instructor=user)

        if user.role == 'student':
            return QuizSubmission.objects.filter(student=user)

        return QuizSubmission.objects.none()


def send_email(request):
    """Send a test email (placeholder function).
    
    Args:
        request: HTTP request object.
    
    Returns:
        HttpResponse: Success or error response.
    """
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