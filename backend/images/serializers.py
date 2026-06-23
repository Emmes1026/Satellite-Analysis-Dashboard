from rest_framework import serializers
from .models import SatelliteImage,AnnotatedSatelliteImage

class SatelliteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SatelliteImage
        fields = '__all__'

class AnnotatedSatelliteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotatedSatelliteImage
        fields = '__all__'