from django.db import models

class User(models.Model):
  graduation_date = models.DateField()


class Course(models.Model):
  name = models.CharField(max_lenght=200)
  
