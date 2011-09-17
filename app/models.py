from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
  user = models.OneToOneField(User)
  graduation_date = models.DateField()

class Course(models.Model):
  #technically, this is all we need since we can just query
  #for the rest
  course_id = models.IntegerField()

class Semester(models.Model):
  owner = models.ForeignKey(User)
  courses = models.ManyToManyField(Course)

  year = models.IntegerField(max_length=4)
  SEMESTER_CHOICES = (
      ('F', 'Fall'),
      ('S', 'Spring'),
      ('U', 'Summer'),
  )
  semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)
