from django.shortcuts import render


from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import SatelliteImage, DetectionResult
from .serializers import SatelliteImageSerializer, DetectionResultSerializer

class GalleryPagination(PageNumberPagination):
    page_size = 15

class SatelliteImageListCreate(generics.ListCreateAPIView):
    queryset = SatelliteImage.objects.filter(is_analyzed=True).order_by("-id")
    serializer_class = SatelliteImageSerializer
    pagination_class = GalleryPagination

class SatelliteImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SatelliteImage.objects.all()
    serializer_class = SatelliteImageSerializer

class WorkerAnalysisImageDetail(generics.ListAPIView):
    queryset = SatelliteImage.objects.filter(is_analyzed=False)
    serializer_class = SatelliteImageSerializer
    pagination_class = None


class DetectionResultListCreate(generics.ListCreateAPIView):
    queryset = DetectionResult.objects.all()
    serializer_class = DetectionResultSerializer

    def perform_create(self, serializer):
        detection = serializer.save()
        image_instance = detection.satellite_image_source
        image_instance.is_analyzed = True
        image_instance.save()


class DetectionResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DetectionResult.objects.all()
    serializer_class = DetectionResultSerializer
    lookup_field = 'satellite_image_source'

    