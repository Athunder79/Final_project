from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from math import radians, sin, cos, sqrt, atan2

User = get_user_model()

class Coordinates(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=7, blank=True, null=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=7 , blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    shot_distance = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)



    def get_absolute_url(self):
        return reverse('scorecard-create')
    


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    par = models.IntegerField()
    # Other relevant course information

class Club(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    club_name = models.CharField(max_length=100)
    club_type = models.CharField(max_length=100)
    # Other relevant club information

class Round(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    round_date = models.DateField()
    score = models.IntegerField()
    weather_conditions = models.CharField(max_length=100)
    # Other relevant round information

class Shot(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    hole_number = models.IntegerField()
    start_longitude = models.FloatField()
    start_latitude = models.FloatField()
    end_longitude = models.FloatField()
    end_latitude = models.FloatField()
    total_distance = models.FloatField()
    taken_at = models.DateTimeField(auto_now_add=True)
# Create your models here.
