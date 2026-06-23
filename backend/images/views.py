from django.shortcuts import render

from rest_framework import generics
from .models import SatelliteImage, AnnotatedSatelliteImage
from .serializers import SatelliteImageSerializer, AnnotatedSatelliteImageSerializer

class SatelliteImageListCreate(generics.ListCreateAPIView):
    queryset = SatelliteImage.objects.all()
    serializer_class = SatelliteImageSerializer

class SatelliteImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SatelliteImage.objects.all()
    serializer_class = SatelliteImageSerializer


class AnnotatedSatelliteImageListCreate(generics.ListCreateAPIView):
    queryset = AnnotatedSatelliteImage.objects.all()
    serializer_class = AnnotatedSatelliteImageSerializer

class AnnotatedSatelliteImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AnnotatedSatelliteImage.objects.all()
    serializer_class = AnnotatedSatelliteImageSerializer
