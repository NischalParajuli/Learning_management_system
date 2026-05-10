from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Enrollment, Course

User = get_user_model()


class Sponsorship(models.Model):

    STATUS_CHOICES = (
        ('act', 'Active'),
        ('com', 'Complete'),
        ('can', 'Cancelled'),
        ('ina', 'Inactive'),
    )

    sponsor = models.ForeignKey( User, on_delete=models.CASCADE,related_name='sponsorships')

    enrollment = models.ForeignKey(Enrollment,on_delete=models.CASCADE,related_name='sponsorships')

    amount = models.DecimalField(max_digits=9,decimal_places=2)

    sponsored_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default='ina'
    )

    class Meta:
        unique_together = ('sponsor', 'enrollment')

    def __str__(self):
        return f"{self.sponsor.username} -> {self.enrollment.course.title}"


class CourseSponsor(models.Model):

    STATUS_CHOICES = (
        ('act', 'Active'),
        ('com', 'Complete'),
        ('can', 'Cancelled'),
        ('ina', 'Inactive'),
    )

    sponsor = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='course_sponsorships')

    course = models.ForeignKey(Course,on_delete=models.CASCADE,
        related_name='course_sponsorships')

    amount = models.DecimalField(max_digits=10,decimal_places=2)

    sponsored_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default='act'
    )

    def __str__(self):
        return f"{self.sponsor.username} sponsored {self.course.title}"
    
