"""Admin dashboard views for system statistics.

Provides endpoints for retrieving comprehensive system statistics including
user counts, course metrics, enrollment data, assignment tracking, and sponsorship totals.
"""

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum

from accounts.permissions import IsAdmin, IsSponsor
from django.contrib.auth import get_user_model
from courses.models import Course, Enrollment
from assesments.models import Assignment, Submission
from sponsorship.models import Sponsorship, CourseSponsor

User = get_user_model()


class AdminDashboardView(APIView):
    """Admin dashboard API endpoint for system statistics.
    
    Requires admin authentication. Returns aggregated statistics across
    the entire system including users, courses, enrollments, assignments,
    and sponsorships.
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        """Retrieve system statistics.
        
        Args:
            request: HTTP request object.
        
        Returns:
            Response: Dictionary containing all system statistics organized
                     by category (users, courses, enrollments, assignments, sponsorships).
        """
        # Count users by role
        total_users = User.objects.count()
        total_students = User.objects.filter(role='student').count()
        total_instructor = User.objects.filter(role='instructor').count()
        total_sponsor = User.objects.filter(role='sponsor').count()

        # Count courses
        total_courses = Course.objects.count()
        active_courses = Course.objects.filter(is_published=True).count()

        # Count enrollments by status
        total_enrollment = Enrollment.objects.count()
        active_enrollment = Enrollment.objects.filter(status='act').count()
        completed_enrollments = Enrollment.objects.filter(status='com').count()

        # Count assignments and submissions
        total_assignment = Assignment.objects.count()
        total_Submission = Submission.objects.count()

        # Sum sponsorship amounts
        total_student_sponsorships = Sponsorship.objects.count()
        total_course_sponsorships = CourseSponsor.objects.count()
        total_student_sponsorships_amount = Sponsorship.objects.aggregate(total=Sum('amount'))['total'] or 0
        total_course_sponsorships_amount = CourseSponsor.objects.aggregate(total=Sum('amount'))['total'] or 0

        # Organize statistics into response object
        data = {
            "users": {
                "total_users": total_users,
                "students": total_students,
                "instructors": total_instructor,
                "sponsors": total_sponsor,
            },

            "courses": {
                "total_courses": total_courses,
                "active_courses": active_courses,
            },

            "enrollment": {
                "total_enrollment": total_enrollment,
                "active_enrollment": active_enrollment,
                "completed_enrollment": completed_enrollments,
            },
            
            "assignment": {
                "total_assignment": total_assignment,
                "total_submission": total_Submission,
            },

            "sponsorship": {
                "student_sponsorships": total_student_sponsorships,
                "course_sponsorships": total_course_sponsorships,
                "student_sponsorship_amount": total_student_sponsorships_amount,
                "course_sponsorship_amount": total_course_sponsorships_amount,
            }
        }

        return Response(data)



class SponsorDashboardView(APIView):  
    permission_classes = [IsAuthenticated, IsSponsor]

    def get(self, request):
        sponsor = request.user

        # student sponsorships
        student_sponsorships = Sponsorship.objects.filter(sponsor=sponsor)
        total_student_sponsorships = student_sponsorships.count()
        active_student_sponsorships = student_sponsorships.filter(status='act').count()
        completed_student_sponsorships = student_sponsorships.filter(status='com').count()
        cancelled_student_sponsorships = student_sponsorships.filter(status='can').count()
        total_student_amount = student_sponsorships.aggregate(total=Sum('amount'))['total'] or 0

        # course sponsorships
        course_sponsorships = CourseSponsor.objects.filter(sponsor=sponsor)
        total_course_sponsorships = course_sponsorships.count()
        active_course_sponsorships = course_sponsorships.filter(status='act').count()
        completed_course_sponsorships = course_sponsorships.filter(status='com').count()
        cancelled_course_sponsorships = course_sponsorships.filter(status='can').count()
        total_course_amount = course_sponsorships.aggregate(total=Sum('amount'))['total'] or 0

        data = {
            "sponsor": sponsor.username,

            "student_sponsorships": {
                "total": total_student_sponsorships,
                "active": active_student_sponsorships,
                "completed": completed_student_sponsorships,
                "cancelled": cancelled_student_sponsorships,
                "total_amount": total_student_amount,
                "sponsored_students": [
                    {
                        "student": s.enrollment.student.username,
                        "course": s.enrollment.course.title,
                        "amount": s.amount,
                        "status": s.get_status_display(),
                        "sponsored_at": s.sponsored_at,
                    }
                    for s in student_sponsorships
                ]
            },

            "course_sponsorships": {
                "total": total_course_sponsorships,
                "active": active_course_sponsorships,
                "completed": completed_course_sponsorships,
                "cancelled": cancelled_course_sponsorships,
                "total_amount": total_course_amount,
                "sponsored_courses": [
                    {
                        "course": c.course.title,
                        "amount": c.amount,
                        "status": c.get_status_display(),
                        "sponsored_at": c.sponsored_at,
                    }
                    for c in course_sponsorships
                ]
            },

            "total_amount_contributed": total_student_amount + total_course_amount,
        }

        return Response(data)
