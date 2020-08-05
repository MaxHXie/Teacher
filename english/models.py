from django.db import models
from django.utils import timezone
import uuid

class Essay(models.Model):
    essay_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    essay_text = models.TextField(max_length=200000) #About 1 MB in Unicode, #80 pages of text
    email = models.EmailField(null=True)
    upload_datetime = models.DateTimeField('date uploaded', default=timezone.now())
    characters = models.IntegerField(null=True)
    price = models.FloatField(null=True)
    currency = models.CharField(max_length=32, default="SEK")
    paid = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.essay_id)
