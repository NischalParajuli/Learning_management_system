from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator , MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import timedelta

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
  start_date = models.DateTimeField()
  duration_days = models.IntegerField()
  end_date = models.DateTimeField(null=True, blank=True)

  def save(self, *args, **kwargs):
    if self.start_date and self.duration_days:
        self.end_date = self.start_date + timedelta(days=self.duration_days)
    super().save(*args, **kwargs)


  def clean(self):
    if self.start_date and self.duration_days is not None:
        if self.duration_days < 0:
            raise ValidationError("Duration cannot be negative")



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
     
