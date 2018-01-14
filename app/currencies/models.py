import datetime

from django.db import models
from django.utils import timezone


class Currency(models.Model):
    name = models.CharField(max_length=16)
    rate = models.DecimalField(decimal_places=6, max_digits=16)
    last_update = models.DateTimeField('last updated at')

    def __str__(self):
        return self.name

    def was_updated_recently(self):
        now = timezone.now()
        return now.day == self.last_update.day
