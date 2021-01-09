from django.db import models
from django.template.defaultfilters import truncatechars  # or truncatewords
from django.conf import settings
from datetime import datetime
import uuid

class Essay(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null=True)
    title = models.TextField(max_length=64, default="")
    essay_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    language = models.TextField(max_length=32)
    subject = models.TextField(max_length=64)
    essay_text = models.TextField(max_length=6000) #About 1 MB in Unicode, #80 pages of text
    has_ended = models.BooleanField(default=False)
    email = models.EmailField(null=True, blank=True)
    upload_datetime = models.DateTimeField('date uploaded', auto_now_add=True)
    characters = models.IntegerField(null=True, blank=True)
    essay_correction_json = models.TextField(default= "", max_length=500000, null=True, blank=True)
    errors = models.TextField(default= "", max_length=100000, null=True, blank=True)
    bounty = models.IntegerField(default=0)
    is_valid = models.BooleanField(default=False)

    def get_date(self):
        time = datetime.now()
        if self.upload_datetime.day == time.day:
            return str(time.hour - self.upload_datetime.hour) + " hours ago"
        else:
            if self.upload_datetime.month == time.month:
                return str(time.day - self.upload_datetime.day) + " days ago"
            else:
                if self.upload_datetime.year == time.year:
                    return str(time.month - self.upload_datetime.month) + " months ago"
        return self.upload_datetime

    def __str__(self):
        return str(self.essay_id)

    @property
    def shorter_essay_text(self):
        return truncatechars(self.essay_text, 100)

class Answer(models.Model):
    answer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    essay = models.ForeignKey(Essay, on_delete=models.CASCADE, null=True)
    answer_text = models.TextField(max_length=2000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null=True)
    upload_datetime = models.DateTimeField('date uploaded', auto_now_add=True)
    winner = models.BooleanField(default=False)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    def get_date(self):
        time = datetime.now()
        if self.upload_datetime.day == time.day:
            return str(time.hour - self.upload_datetime.hour) + " hours ago"
        else:
            if self.upload_datetime.month == time.month:
                return str(time.day - self.upload_datetime.day) + " days ago"
            else:
                if self.upload_datetime.year == time.year:
                    return str(time.month - self.upload_datetime.month) + " months ago"
        return self.upload_datetime

    def __str__(self):
        return str(self.answer_id)

    @property
    def shorter_answer_text(self):
        return truncatechars(self.answer_text, 100)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null=True)
    biography = models.TextField(max_length=200000, null=True, blank=True)
    coins = models.IntegerField(default=30)

    def __str__(self):
        return str(self.user.username)

    def default_profile_picture(self):
        return str(int(self.user.id) % 100)
