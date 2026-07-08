from django.shortcuts import render

import os
from core.celery import app
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import SatelliteImage, DetectionResult
from .serializers import SatelliteImageSerializer, DetectionResultSerializer

class GalleryPagination(PageNumberPagination):
    page_size = 15

    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "total_pages": self.page.paginator.num_pages,
            "results": data,
        })
        

class SatelliteImageListCreate(generics.ListCreateAPIView):
    queryset = SatelliteImage.objects.filter(is_analyzed=True).order_by("-id")
    serializer_class = SatelliteImageSerializer
    pagination_class = GalleryPagination

    def perform_create(self, serializer):
        new_task = serializer.save()
        image_path = "http://web:8000" + new_task.image.url
        image_id = new_task.id
        app.send_task(
            "process_satellite_image", 
            args=[image_id, image_path]
        )
        

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

    