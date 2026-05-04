from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator , MaxValueValidator

User = get_user_model()

# Create your models here.
class Course(models.Model):

  DIFFICULTY_CHOICES = (
    ('beg','Beginner'),
    ('int','Intermediate'),
    ('adv','Advanced'),
  )

  title = models.CharField(max_length=100)
  description = models.TextField()
  instructor = models.ForeignKey(User , on_delete=models.SET_NULL,null=True,blank=True,related_name='courses')
  difficulty = models.CharField(max_length=3 , choices=DIFFICULTY_CHOICES , default='beg')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now = True)
  is_published = models.BooleanField(default=True)
  course_duration = models.IntegerField(default=0)

  def __str__(self):
    return self.title
  

class Enrollment(models.Model):
    
    STATUS = (
      ('act','Active'),
      ('com','Complete'),
      ('dro','Dropped'),
    )

    student = models.ForeignKey(User,on_delete=models.CASCADE,related_name='enrollments')
    course = models.ForeignKey(Course , on_delete=models.CASCADE,related_name='enrollments')
    progress = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(100)])
    status = models.CharField(max_length=3,choices=STATUS,default='act')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
     unique_together = ('student','course')
     ordering = ['-enrolled_at']

     def __str__(self):
        return f"{self.student} - {self.course}"