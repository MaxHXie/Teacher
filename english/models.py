from django.db import models
from django.utils import timezone

class Essay(models.Model):
    upload_datetime = models.DateTimeField('date uploaded', default=timezone.now())
    words = models.IntegerField()
    price = models.FloatField(null=True)
    currency = models.CharField(max_length=32)
    paid = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
