from rest_framework import serializers
from .models import Booking, Room


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['id', 'name', 'capacity', 'type']
