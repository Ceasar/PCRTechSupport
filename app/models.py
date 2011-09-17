from django.db import models


class User(models.Model):
  username = models.CharField(max_length=64);
  graduation_date = models.DateField()
  

class Course(models.Model):
  name = models.CharField(max_length=200)
  

