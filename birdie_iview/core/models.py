from django.db import models
from django.db.models import F
from django.contrib.auth import get_user_model
from django.urls import reverse
from math import radians, sin, cos, sqrt, atan2
from users.models import Clubs

User = get_user_model()

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    rating = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ['latitude', 'longitude'] 

    def __str__(self):
        return self.name

class Round(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    round_date = models.DateField(auto_now_add=True)


    def __str__(self):
        self.round_date

class Hole(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    hole_num = models.IntegerField(null=True, blank=True)
    hole_par = models.IntegerField(null=True, blank=True)
    hole_distance = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.course} - Hole {self.hole_num}'

class Shot(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    hole = models.ForeignKey(Hole, on_delete=models.CASCADE)
    hole_num = models.IntegerField(null=True, blank=True)
    hole_par = models.IntegerField(null=True, blank=True)
    shot_num_per_hole = models.IntegerField(null=True, blank=True, default=1)  
    latitude = models.DecimalField(max_digits=9, decimal_places=7, blank=True, null=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=7 , blank=True, null=False)
    end_latitude = models.DecimalField(max_digits=9, decimal_places=7, blank=True, null=True)
    end_longitude = models.DecimalField(max_digits=9, decimal_places=7, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    shot_distance = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('scorecard-create')
    
    def ShotNumber(self):
        if self.shot_num_per_hole:
            return 1
        # incresase the shot number by 1
        self.shot_num_per_hole = F('shot_num_per_hole') + 1

    def save(self, *args, **kwargs):
        if not self.pk:  # If this is a new entry, calculate shot distance
            previous_shot = Shot.objects.filter(user=self.user).order_by('-created_at').first()
            if previous_shot:
                # Calculate distance between previous shot and current shot
                previous_lat = radians(float(previous_shot.latitude))
                previous_lon = radians(float(previous_shot.longitude))
                current_lat = radians(float(self.latitude))
                current_lon = radians(float(self.longitude))

                # Difference in coordinates
                dlon = current_lon - previous_lon
                dlat = current_lat - previous_lat

                # Haversine formula
                a = sin(dlat / 2)**2 + cos(previous_lat) * cos(current_lat) * sin(dlon / 2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))

                # Radius of the Earth in kilometers * c *1000 to get metres
                distance = 6371 * c 

                # Update previous shot's distance
                previous_shot.shot_distance = distance
                previous_shot.save(update_fields=['shot_distance'])  # Update shot_distance field

        super().save(*args, **kwargs)
    



