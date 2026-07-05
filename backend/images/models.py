from django.db import models

class SatelliteImage(models.Model):
    name = models.CharField(max_length=255, verbose_name="Image name")
    image = models.ImageField(upload_to='satellitesImages/', verbose_name="Image file")
    latitude = models.FloatField(null=True, blank=True, verbose_name="Latitude")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Longitude")
    is_analyzed = models.BooleanField(default=False, verbose_name="Was AI analyzed?")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Upload date")

    def __str__(self):
        return self.name


class DetectionResult(models.Model):
    satellite_image_source = models.OneToOneField(SatelliteImage, on_delete=models.CASCADE)
    ship_number = models.IntegerField(verbose_name="Detected ships count")
    raw_detections = models.JSONField(default=list, verbose_name="Raw bounding boxes data")
    analyzed_at = models.DateTimeField(auto_now_add=True, verbose_name="Analysis date")

    def __str__(self):
        return f"Result for: {self.satellite_image_source.name}"