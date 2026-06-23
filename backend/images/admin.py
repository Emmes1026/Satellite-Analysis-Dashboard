from django.contrib import admin
from .models import SatelliteImage, AnnotatedSatelliteImage

admin.site.register(SatelliteImage)
admin.site.register(AnnotatedSatelliteImage)

# Register your models here.
