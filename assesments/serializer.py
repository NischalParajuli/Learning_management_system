"""Serializers for assignment and submission models.

Provides serialization for Assignment and Submission models with custom
validation logic to enforce deadlines and permissions.
"""

from django.db import models
from django.utils import timezone
from rest_framework import serializers
from .models import Assignment, Submission


class AssignmentSerializer(serializers.ModelSerializer):
    """Serializes Assignment model instances to/from JSON."""

    class Meta:
        model = Assignment
        fields = '__all__'


class SubmissionSerializer(serializers.ModelSerializer):
    """Serializes Submission model instances to/from JSON.
    
    Enforces business logic for submissions including deadline checking,
    role-based edit permissions, and automatic status determination.
    """

    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ['student', 'status']

    def create(self, validated_data):
        """Create submission and check if submitted after deadline.
        
        Args:
            validated_data: Dictionary containing validated submission data.
        
        Returns:
            Submission: Newly created submission with status set to 'late' if past due.
        """
        request = self.context['request']
        student = request.user
        assignment = validated_data.get('assignment')

        # Automatically mark submission as late if submitted after deadline
        if timezone.now() > assignment.due_date:
            validated_data['status'] = 'late'

            validated_data['student'] = student

            return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update submission with role-based restrictions.
        
        Students can only edit content before deadline. Instructors can only
        grade submissions. Admins have full access.
        
        Args:
            instance: Existing submission instance.
            validated_data: Dictionary containing validated update data.
        
        Returns:
            Submission: Updated submission instance.
            
        Raises:
            ValidationError: If restrictions are violated.
        """
        request = self.context['request']
        user = request.user

        if user.role == 'student':
            # Verify ownership and deadline not passed
            if user != instance.student:
                raise serializers.ValidationError("You cannot edit this submission")

            if timezone.now() > instance.assignment.due_date:
                raise serializers.ValidationError("Deadline passed: You cannot edit this")

            # Students cannot modify grading fields
            validated_data.pop('grade', None)
            validated_data.pop('feedback', None)
            validated_data.pop('status', None)

        elif user.role == 'instructor':
            # Verify instructor owns the course
            if instance.assignment.course.instructor != user:
                raise serializers.ValidationError("You cannot grade this submission")

            # Instructors cannot edit submission content
            validated_data.pop('content', None)

            # Automatically mark as graded when instructor updates
            validated_data['status'] = 'grd'

        elif user.role == 'admin':
            # Admins have full access
            pass

        return super().update(instance, validated_data)

    def validate(self, data):
        """Validate that assignment is provided.
        
        Args:
            data: Data to validate.
        
        Returns:
            dict: Validated data.
            
        Raises:
            ValidationError: If assignment is missing.
        """
        if not data.get('assignment'):
            raise serializers.ValidationError({"assignment": "Required"})
        return data