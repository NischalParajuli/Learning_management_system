"""Views for managing courses and student enrollments.

Provides REST API endpoints for creating, retrieving, and managing courses,
and handling student course enrollments with role-based access control.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from accounts.permissions import IsAdmin, IsInstructor
from .models import Course, Enrollment
from .serializer import CourseSerializer, EnrollmentSerializer
from .pagination import CoursePagination
from rest_framework.exceptions import MethodNotAllowed



class CourseViewset(viewsets.ModelViewSet):
    """API viewset for managing courses.
    
    Provides CRUD operations for courses with filtering, searching, and pagination.
    Only instructors and admins can create courses. Admins can modify/delete.
    Includes custom enroll action for students to join courses.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'instructor__username', 'difficulty']
    filterset_fields = ['difficulty', 'is_published']
    ordering_fields = ['title', 'created_at']


    def create(self, request, *args, **kwargs):
        if request.user.role == 'student':
            raise MethodNotAllowed('POST', detail='Students cannot create courses')
        return super().create(request, *args, **kwargs)


    def get_permissions(self):
        """Determine required permissions based on action.
        
        Returns:
            list: Permission classes required for the action.
        """
        if self.action == 'create':
            return [IsAdmin()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        elif self.action == 'enroll':
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """Set the current user as the course instructor.
        
        Args:
            serializer: Course serializer instance.
        """
        serializer.save(instructor=self.request.user)

    @action(detail=True, methods=['post'], url_path='enroll')
    def enroll(self, request, pk=None):
        """Handle course enrollment for authenticated students.
        
        Args:
            request: HTTP request object.
            pk: Primary key of the course.
        
        Returns:
            Response: Success message or error if already enrolled.
        """
        course = self.get_object()
        student = request.user

        if Enrollment.objects.filter(student=student, course=course).exists():
            return Response(
                {'error': 'You are already enrolled in this course'},
                status=status.HTTP_400_BAD_REQUEST
            )

        Enrollment.objects.create(student=student, course=course)
        return Response(
            {'message': f'Successfully enrolled in {course.title}'},
            status=status.HTTP_201_CREATED
        )




class EnrollmentViewset(viewsets.ModelViewSet):
    """API viewset for managing student course enrollments.
    
    Allows students to enroll in courses and view their enrollments.
    Only admins can delete enrollments.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        """Filter enrollments based on user role.
        
        Admin users see all enrollments. Students see only their own.
        
        Returns:
            QuerySet: Filtered enrollments.
        """
        user = self.request.user
        if user.role == 'admin':
            return Enrollment.objects.all()
        return Enrollment.objects.filter(student=user)

    def get_permissions(self):
        """Determine required permissions based on action.
        
        Returns:
            list: Permission classes required for the action.
        """
        if self.action == 'destroy':
            return [IsAdmin()]
        elif self.action in ['update', 'partial_update']:
            return [IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """Set the current user as the enrolling student.
        
        Args:
            serializer: Enrollment serializer instance.
        """
        serializer.save(student=self.request.user)