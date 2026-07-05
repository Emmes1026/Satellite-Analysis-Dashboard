from django.shortcuts import render


from rest_framework import generics
from .models import SatelliteImage, DetectionResult
from .serializers import SatelliteImageSerializer, DetectionResultSerializer

class SatelliteImageListCreate(generics.ListCreateAPIView):
    serializer_class = SatelliteImageSerializer

    def get_queryset(self):
        queryset = SatelliteImage.objects.all().order_by('-id')
        status = self.request.query_params.get('status')
        
        mapping = {
            "pending": False,
            "analyzed": True
        }
        
        if status in mapping:
            return queryset.filter(is_analyzed=mapping[status])
            
        return queryset

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


class DetectionResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DetectionResult.objects.all()
    serializer_class = DetectionResultSerializer
    lookup_field = 'satellite_image_source'

    