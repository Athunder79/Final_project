from django.db import models

class Coordinates(models.Model):
    id = models.AutoField(primary_key=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6 , blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


# Create your models here.
