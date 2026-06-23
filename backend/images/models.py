from django.db import models

class SatelliteImage(models.Model):
    name = models.CharField(max_length=255, verbose_name="Image name")
    image = models.ImageField(upload_to='satellitesImages/', verbose_name="Image file")
    latitude = models.FloatField(null=True, blank=True, verbose_name="Latitude")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Longitude")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Upload date")

    def __str__(self):
        return self.name


class AnnotatedSatelliteImage(models.Model):
    name = models.CharField(max_length=255, verbose_name="Image name")
    image = models.ImageField(upload_to='annotated_images/', verbose_name="Image file")
    ship_number = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Upload date")
    satellite_image_source = models.ForeignKey(SatelliteImage, on_delete=models.CASCADE)

    def __str__(self):
        return self.name