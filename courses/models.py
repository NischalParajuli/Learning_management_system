"""Models for courses and student enrollments.

Defines Course and Enrollment models that represent the learning structure
of the system, including course metadata, scheduling, and student enrollment.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import timedelta

User = get_user_model()


class Course(models.Model):
    """Represents an online course.
    
    Attributes:
        title: Course title.
        description: Detailed course description.
        instructor: ForeignKey to the User who teaches the course.
        difficulty: The course difficulty level (Beginner, Intermediate, Advanced).
        created_at: Timestamp when course was created.
        updated_at: Timestamp when course was last updated.
        is_published: Whether the course is visible to students.
        start_date: When the course begins.
        duration_days: How long the course lasts in days.
        end_date: When the course ends (automatically calculated from start_date and duration_days).
    """
    DIFFICULTY_CHOICES = (
        ('beg', 'Beginner'),
        ('int', 'Intermediate'),
        ('adv', 'Advanced'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='courses')
    difficulty = models.CharField(max_length=3, choices=DIFFICULTY_CHOICES, default='beg')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_published = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    duration_days = models.IntegerField()
    end_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """Calculate end_date from start_date and duration_days.
        
        The end date is automatically computed when the course is saved.
        """
        if self.start_date and self.duration_days:
            self.end_date = self.start_date + timedelta(days=self.duration_days)
        super().save(*args, **kwargs)

    def clean(self):
        """Validate that duration cannot be negative.
        
        Raises:
            ValidationError: If duration_days is negative.
        """
        if self.start_date and self.duration_days is not None:
            if self.duration_days < 0:
                raise ValidationError("Duration cannot be negative")

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    """Represents a student's enrollment in a course.
    
    Tracks a student's participation in a course, including their progress,
    enrollment status, and when they enrolled.
    
    Attributes:
        student: ForeignKey to the enrolled User.
        course: ForeignKey to the Course being enrolled in.
        progress: Percentage of course completion (0-100).
        status: Current enrollment status (Active, Complete, Dropped).
        enrolled_at: Timestamp when student enrolled.
    """
    STATUS = (
        ('act', 'Active'),
        ('com', 'Complete'),
        ('dro', 'Dropped'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    progress = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    status = models.CharField(max_length=3, choices=STATUS, default='act')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure each student enrolls only once per course
        unique_together = ('student', 'course')
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"
