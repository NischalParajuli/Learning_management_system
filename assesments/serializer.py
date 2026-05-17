"""Serializers for assignment and submission models."""

from django.utils import timezone
from rest_framework import serializers
from .models import Assignment, Submission
from courses.models import Enrollment


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'student', 'content', 'feedback', 'grade', 'status', 'submitted_at']
        read_only_fields = ['student', 'status']
    
    def to_representation(self, instance):
        """Hide grade and feedback from students."""
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user.role == 'student':
            data.pop('feedback', None)
            data.pop('grade', None)
        return data

    def validate(self, data):
        request = self.context.get('request')
        user = request.user

        if not data.get('assignment'):
            raise serializers.ValidationError({"assignment": "Required"})

        assignment = data.get('assignment')

        if user.role == 'student':  #  only validate for students
            # check enrollment
            enrolled_courses = Enrollment.objects.filter(
                student=user
            ).values_list('course', flat=True)

            if assignment.course_id not in enrolled_courses:
                raise serializers.ValidationError(
                    {'assignment': 'You are not enrolled in this course.'}
                )

            # check duplicate submission
            if Submission.objects.filter(student=user, assignment=assignment).exists():
                raise serializers.ValidationError(
                    {'assignment': 'You have already submitted this assignment.'}
                )

            # block grading fields
            forbidden = ['grade', 'feedback', 'status']
            for field in forbidden:
                if field in data:
                    raise serializers.ValidationError(
                        {field: f'Students are not allowed to set {field}.'}
                    )

        return data

    def create(self, validated_data):
        request = self.context['request']
        assignment = validated_data.get('assignment')

        #  always set student
        validated_data['student'] = request.user

        #  always save, mark late if past deadline
        if timezone.now() > assignment.due_date:
            validated_data['status'] = 'late'

        return super().create(validated_data)  #  always returns, not just when late

    def update(self, instance, validated_data):
        request = self.context['request']
        user = request.user

        if user.role == 'student':
            if user != instance.student:
                raise serializers.ValidationError("You cannot edit this submission")
            if timezone.now() > instance.assignment.due_date:
                raise serializers.ValidationError("Deadline passed: You cannot edit this")
            validated_data.pop('grade', None)
            validated_data.pop('feedback', None)
            validated_data.pop('status', None)

        elif user.role == 'instructor':
            if instance.assignment.course.instructor != user:
                raise serializers.ValidationError("You cannot grade this submission")
            validated_data.pop('content', None)
            validated_data['status'] = 'grd'

        elif user.role == 'admin':
            pass

        return super().update(instance, validated_data)