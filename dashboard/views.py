from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum

from accounts.permissions import IsAdmin
from django.contrib.auth import get_user_model
from courses.models import Course, Enrollment
from assesments.models import Assignment, Submission
from sponsorship.models import Sponsorship, CourseSponsor
# Create your views here.

User = get_user_model()

class AdminDashboardView(APIView):

  permission_classes = [IsAuthenticated,IsAdmin]

  def get(self,request):

# Users 

    total_users = User.objects.count()
    total_students = User.objects.filter(role = 'student').count()
    total_instructor = User.objects.filter(role = 'instructor').count()
    total_sponsor = User.objects.filter(role = 'sponsor').count()

#Courses

    total_courses = Course.objects.count()
    active_courses = Course.objects.filter(is_published = True).count()

#Enrollment

    total_enrollment = Enrollment.objects.count()
    active_enrollment = Enrollment.objects.filter(status = 'act').count()
    completed_enrollments = Enrollment.objects.filter(status='com').count()

#Assignment

    total_assignment = Assignment.objects.count()
    total_Submission = Submission.objects.count()

#Sponsorships

    total_student_sponsorships = Sponsorship.objects.count()
    total_course_sponsorships = CourseSponsor.objects.count()
    total_student_sponsorships_amount = Sponsorship.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_course_sponsorships_amount = CourseSponsor.objects.aggregate(total=Sum('amount'))['total'] or 0



    data = {
        "users": {
          
          "total_users":total_users,
          "students":total_students,
          "instructors":total_instructor,
          "sponsors":total_sponsor,
        },


        "courses":{
          
            "total_courses":total_courses,
            "active_courses":active_courses,
        },

        "enrollment":{
          
          "total_enrollment":total_enrollment,
          "active_enrollment":active_enrollment,
          "completed_enrollment":completed_enrollments,
        },
        
        "assignment":{
          
          "total_assignment":total_assignment,
          "total_submission":total_Submission,
        },

        "sponsorship":{
          
          "student_sponsorships":total_student_sponsorships,
          "course_sponsorships":total_course_sponsorships,
          "student_sponsorship_amount":total_student_sponsorships_amount,
          "course_sponsorship_amount":total_course_sponsorships_amount,

        }

    }

    return Response(data)

