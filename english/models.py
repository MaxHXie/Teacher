from django.db import models
from django.utils import timezone
from django.template.defaultfilters import truncatechars  # or truncatewords
import uuid

class Essay(models.Model):
    essay_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    essay_text = models.TextField(max_length=200000) #About 1 MB in Unicode, #80 pages of text
    email = models.EmailField(null=True)
    upload_datetime = models.DateTimeField('date uploaded', auto_now_add=True)
    characters = models.IntegerField(null=True)
    price = models.FloatField(null=True)
    currency = models.CharField(max_length=32, default="EUR")
    paid = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    were_limited = models.BooleanField(default=False)

    def __str__(self):
        return str(self.essay_id)

    @property
    def shorter_essay_text(self):
        return truncatechars(self.essay_text, 100)
