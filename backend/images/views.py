from django.shortcuts import render


from rest_framework import generics
from .models import SatelliteImage, DetectionResult
from .serializers import SatelliteImageSerializer, DetectionResultSerializer

class SatelliteImageListCreate(generics.ListCreateAPIView):
    queryset = SatelliteImage.objects.filter(is_analyzed = False)
    serializer_class = SatelliteImageSerializer

class SatelliteImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SatelliteImage.objects.all()
    serializer_class = SatelliteImageSerializer


class DetectionResultListCreate(generics.ListCreateAPIView):
    queryset = DetectionResult.objects.all()
    serializer_class = DetectionResultSerializer

    def perform_create(self, serializer):
        detection = serializer.save()
        image_instance = detection.satellite_image_source
        image_instance.is_analyzed = True
        image_instance.save()

    