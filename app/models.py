from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
  # At the moment, we aren't using this class (we're using User instead)
  user = models.OneToOneField(User)
  graduation_date = models.DateField()

  def __str__(self):
    return str(self.user)

class Course(models.Model):
  #technically, this is all we need since we can just query
  #for the rest
  course_id = models.IntegerField(max_length=10)
  name = models.CharField(max_length=100, primary_key=True)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return "/courses/%s/" % self.id

class Semester(models.Model):
  owner = models.ForeignKey(User, related_name="semesters")
  courses = models.ManyToManyField(Course)

  year = models.IntegerField(max_length=4)
  SEMESTER_CHOICES = (
      ('F', 'Fall'),
      ('S', 'Spring'),
      ('U', 'Summer'),
  )
  semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)

  def get_absolute_url(self):
    return "/semester/%s/%s/" % (self.year, self.semester)

  def __str__(self):
    return "%s: %s %s" % (str(self.owner), str(self.year), str(self.semester))
