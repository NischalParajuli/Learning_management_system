"""Serializers for Course and Enrollment models.

Provides serialization for Course and Enrollment objects with custom
validation to prevent duplicate enrollments.
"""

from rest_framework import serializers
from .models import Enrollment, Course


class CourseSerializer(serializers.ModelSerializer):
    """Serializes Course model instances to/from JSON."""

    class Meta:
        model = Course
        fields = '__all__'


class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializes Enrollment model instances to/from JSON.
    
    Validates that students don't enroll in the same course multiple times.
    """

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'progress', 'status', 'enrolled_at']
        read_only_fields = ['student', 'progress', 'status']

    def validate(self, data):
        """Validate enrollment data.
        
        Ensures course is provided and student isn't already enrolled.
        
        Args:
            data: Data to validate.
        
        Returns:
            dict: Validated data.
            
        Raises:
            ValidationError: If course is missing or student already enrolled.
        """
        student = self.context['request'].user
        course = data.get('course')

        if not course:
            raise serializers.ValidationError("Course is Required")

        # Check if student is already enrolled in this course
        if Enrollment.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError('You are already enrolled in this course')

        return data