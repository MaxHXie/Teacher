from django.db import models
from django.template.defaultfilters import truncatechars  # or truncatewords
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import User
from notifications.signals import notify
import uuid

#notification system
from django.db.models.signals import post_save, post_delete
from notifications.models import Notification

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
    views = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    is_valid = models.BooleanField(default=False)

    def get_date(self):
        time = datetime.now()
        if self.upload_datetime.day == time.day:
            if self.upload_datetime.hour == time.hour or abs(self.upload_datetime.hour - time.hour) == 1:
                time_ago = time.minute - self.upload_datetime.minute
                if time_ago == 1:
                    return str(time_ago) + " minute ago"
                else:
                    return str(time_ago) + " minutes ago"
            else:
                time_ago = time.hour - self.upload_datetime.hour
                if time_ago == 1:
                    return str(time_ago) + " hour ago"
                else:
                    return str(time_ago) + " hours ago"

        else:
            if self.upload_datetime.month == time.month:
                time_ago = time.day - self.upload_datetime.day
                if time_ago == 1:
                    return str(time_ago) + " day ago"
                else:
                    return str(time_ago) + " days ago"
            else:
                if self.upload_datetime.year == time.year:
                    time_ago = time.month - self.upload_datetime.month
                    if time_ago == 1:
                        return str(time_ago) + " month ago"
                    else:
                        return str(time_ago) + " months ago"
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

    #try using signals
    def user_answered_question(sender, instance, created, *args, **kwargs):
        if created is True:
            answer = instance
            post = answer.essay
            sender = answer.author
            notify = Notification(action_object=post, actor=sender, recipient=post.author, target_object_id=answer.answer_id, verb="answered question")
            notify.save()

    def user_also_answered_question(sender, instance, created, *args, **kwargs):
        if created is True:
            answer = instance
            post = answer.essay
            sender = answer.author
            # inform users that previously have answered this question that somebody else also have answered this question
            recipients = User.objects.filter(pk__in=(post.answer_set.all().exclude(author=sender).exclude(author=post.author).values_list('author', flat=True)))
            notify.send(action_object=post, sender=sender, recipient=recipients, target_object_id=answer.answer_id, verb="also answered question")

    def user_won_question(sender, instance, created, update_fields, *args, **kwargs):
        try:
            if next(iter(update_fields)) == 'winner' and created is False:
                answer = instance
                post = answer.essay
                recipient = answer.author
                notify = Notification(action_object=post, actor=post.author, recipient=recipient, target_object_id=answer.answer_id, verb="won question")
                notify.save()
        except:
            pass

    def get_date(self):
        time = datetime.now()
        if self.upload_datetime.day == time.day:
            if self.upload_datetime.hour == time.hour or abs(self.upload_datetime.hour - time.hour) == 1:
                time_ago = time.minute - self.upload_datetime.minute
                if time_ago == 1:
                    return str(time_ago) + " minute ago"
                else:
                    return str(time_ago) + " minutes ago"
            else:
                time_ago = time.hour - self.upload_datetime.hour
                if time_ago == 1:
                    return str(time_ago) + " hour ago"
                else:
                    return str(time_ago) + " hours ago"

        else:
            if self.upload_datetime.month == time.month:
                time_ago = time.day - self.upload_datetime.day
                if time_ago == 1:
                    return str(time_ago) + " day ago"
                else:
                    return str(time_ago) + " days ago"
            else:
                if self.upload_datetime.year == time.year:
                    time_ago = time.month - self.upload_datetime.month
                    if time_ago == 1:
                        return str(time_ago) + " month ago"
                    else:
                        return str(time_ago) + " months ago"
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

class UserAction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null=True)
    datetime = models.DateTimeField('datetime', auto_now_add=True)
    action = models.TextField(max_length=32)

#notification system
post_save.connect(Answer.user_answered_question, sender=Answer)
post_save.connect(Answer.user_also_answered_question, sender=Answer)
post_save.connect(Answer.user_won_question, sender=Answer)
