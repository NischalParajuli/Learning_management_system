from django.db import models
from django.utils import timezone
from rest_framework import serializers
from .models import Assignment , Submission



class AssignmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Assignment
    fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Submission
    fields = '__all__'
    read_only_fields = ['student','status']

  def create(self,validated_data):
    request = self.context['request']
    student = request.user
    assignment = validated_data.get('assignment')

    if timezone.now() > assignment.due_date:
        validated_data['status'] = 'late'

        validated_data['student'] = student

        return super().create(validated_data)

def update(self, instance, validated_data):
    request = self.context['request']
    user = request.user

 
    if user.role == 'student':

        if user != instance.student:
            raise serializers.ValidationError("You cannot edit this submission")

        if timezone.now() > instance.assignment.due_date:
            raise serializers.ValidationError("Deadline passed: You cannot edit this")

        # student can only edit content
        validated_data.pop('grade', None)
        validated_data.pop('feedback', None)
        validated_data.pop('status', None)

   
    elif user.role == 'instructor':

        if instance.assignment.course.instructor != user:
            raise serializers.ValidationError("You cannot grade this submission")

        # instructor cannot edit content
        validated_data.pop('content', None)

        # mark as graded
        validated_data['status'] = 'grd'

  
    elif user.role == 'admin':
        pass

    return super().update(instance, validated_data)  


def validate(self,data):
  if not data.get('assignment'):
     raise serializers.ValidationError({"assignment":"Required"})
  return data


  


    

      

      

      


  