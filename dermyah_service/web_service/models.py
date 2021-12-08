

from django.db import models

class Dermyah(models.Model):
    wifi_mode = models.CharField(max_length=100)

    def __str__(self):
        return self.wifi_mode
