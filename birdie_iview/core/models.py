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
    round_completed = models.BooleanField(default=False)


    def __str__(self):
        self.round_date

class Hole(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    hole_num = models.IntegerField(null=False, blank=False)
    hole_par = models.IntegerField(null=False, blank=False)
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
    shot_distance = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('scorecard-create')
    
    def ShotNumber(self):
        if self.shot_num_per_hole:
            return 1
        # incresase the shot number by 1
        self.shot_num_per_hole = F('shot_num_per_hole') + 1

    def save(self, *args, **kwargs):
        if not self.pk: 
            if self.shot_num_per_hole > 0:  # If not the first shot of the hole

            # update the end coordinates of the previous shot and calculate the distance
                self._update_previous_shot_end_coordinates()
                self._calculate_distance()
            else:
                # Only calculate distance between start coordinates and end coordinates of the previous shot
                self._calculate_distance()

        super().save(*args, **kwargs)

    def _update_previous_shot_end_coordinates(self):
        previous_shot = Shot.objects.filter(user=self.user).order_by('-created_at').first()

        if previous_shot and previous_shot.shot_num_per_hole >= 0: # If there is a previous shot and meets the condition
            previous_shot.end_latitude = self.latitude
            previous_shot.end_longitude = self.longitude
            previous_shot.save(update_fields=['end_latitude', 'end_longitude'])

    def _calculate_distance(self):
        previous_shot = Shot.objects.filter(user=self.user).order_by('-created_at').first()

        if previous_shot and all(getattr(previous_shot, attr) is not None for attr in ['latitude', 'longitude', 'end_latitude', 'end_longitude']):
            start_lat = radians(float(previous_shot.latitude))
            start_lon = radians(float(previous_shot.longitude))
            end_lat = radians(float(previous_shot.end_latitude))
            end_lon = radians(float(previous_shot.end_longitude))

            # Difference in coordinates
            dlon = end_lon - start_lon
            dlat = end_lat - start_lat

            # Haversine formula
            a = sin(dlat / 2)**2 + cos(start_lat) * cos(end_lat) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            # Radius of the Earth in kilometers * c *1000 to get meters
            distance = 6371 * c * 1093.61
            distance_rounded = round(distance,1)

            # Update previous shot's distance
            previous_shot.shot_distance = distance_rounded
            previous_shot.save(update_fields=['shot_distance'])