from rest_framework import serializers
from .models import *


class BirdSerializer(serializers.ModelSerializer):
    """
    Сериалайзер модели Bird
    """
    class Meta:
        model = Bird
        fields = ['id', 'name', 'color']


class BirdSeenSerializer(serializers.ModelSerializer):
    """
    Сериалайзер модели BirdSeen
    """
    class Meta:
        model = BirdSeen
        fields = ['user_id', 'bird_id', 'saw_at']