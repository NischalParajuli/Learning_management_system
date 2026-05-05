from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()
# Create your models here.
class Assignment(models.Model):
  
  course = models.ForeignKey(Course ,on_delete=models.SET_NULL,null=True,blank=True,related_name='assignments')
  instructor = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='assignments')
  title = models.CharField(max_length=100)
  description = models.TextField()
  due_date = models.DateTimeField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title


class Submission(models.Model):
  
  SUBMISSION_STATUS = (
    ('sub','submitted'),
    ('grd','graded'),
    ('late','late'),
  )

  assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE,related_name='submissions')
  student = models.ForeignKey(User,on_delete=models.CASCADE,related_name='assignment_submissions')
  content = models.TextField()
  submitted_at = models.DateTimeField(auto_now_add=True)
  feedback = models.CharField(max_length=200,blank=True)
  grade = models.FloatField(default=0)
  status = models.CharField(max_length=4,choices=SUBMISSION_STATUS,default='sub')


  class Meta:
    unique_together = ('assignment', 'student')

  def __str__(self):
    return self.title


class Quiz(models.Model):

  course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='quizzes') 
  title = models.CharField(max_length=150)
  instructor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='quizzes') 
  created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
  CORRECT = (
     ('A','Option1'),
     ('B','Option2'),
     ('C','Option3'),
     ('D','Option4'),

  )

  quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name='questions')
  question = models.CharField(max_length=200)
  opt1 = models.TextField()
  opt2 = models.TextField()
  opt3 = models.TextField()
  opt4 = models.TextField()
  correct_answer = models.CharField(max_length=1,choices=CORRECT)

  def __str__(self):
    return f"Question {self.id}"


class QuizSubmission(models.Model):

  quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name='submissions')
  student = models.ForeignKey(User,on_delete=models.CASCADE,related_name='quiz_submissions')
  score = models.IntegerField(default=0)
  submitted_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ('quiz','student')


  def __str__(self):
    return f"Question {self.id}"