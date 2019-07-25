from datetime import datetime

from django.db import models


class PySensorData(models.Model):
    DateTime = models.DateTimeField(default=datetime.now, blank=True)
    Latitude = models.FloatField(null=True, blank=True, default=None)
    Longitude = models.FloatField(null=True, blank=True, default=None)
    Temperature_F = models.FloatField(null=True, blank=True, default=None)
    RelativeHumidity = models.FloatField(null=True, blank=True, default=None)
    LPG_PPM = models.FloatField(null=True, blank=True, default=None)
    CO_PPM = models.FloatField(null=True, blank=True, default=None)
    Smoke_PPM = models.FloatField(null=True, blank=True, default=None)
    Pressure_hPa = models.FloatField(null=True, blank=True, default=None)
    Altitude_m = models.FloatField(null=True, blank=True, default=None)
    PM_25 = models.FloatField(null=True, blank=True, default=None)