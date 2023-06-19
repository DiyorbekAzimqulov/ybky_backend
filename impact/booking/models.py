from django.db import models

# Create your models here.


class Room(models.Model):
    types = [('focus', 'focus'), ('conference', 'conference'),
             ('team', 'team')]
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    type = models.CharField(choices=types, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Booking(models.Model):

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    resident = models.JSONField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
