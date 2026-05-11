from rest_framework import serializers
from .models import Enrollment , Course


class CourseSerializer(serializers.ModelSerializer):
  class Meta:
    model = Course
    fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
  

  class Meta:
    model = Enrollment
    fields = ['id', 'student', 'course', 'progress', 'status', 'enrolled_at']
    read_only_fields = ['student','progress','status']

  def validate(self, data):
    student = self.context['request'].user
    course =  data.get('course')

    if not course:
      raise serializers.ValidationError("Course is Required")

    if Enrollment.objects.filter(student=student,course=course).exists():
      raise serializers.ValidationError('You are already enrolled in this course')
   
    

    return data