from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
  
  ROLE_CHOICES = (
    ('admin','Admin'),
    ('instructor','Instructor'),
    ('student','Student'),
    ('sponsor','Sponsor')
  )
  
  role = models.CharField(max_length=10,choices=ROLE_CHOICES,default = 'student')
  
