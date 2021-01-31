from django.contrib import admin

from .models import Essay, Answer, Profile
from notifications.models import Notification

class EssayAdmin(admin.ModelAdmin):
    fields = [
    'author',
    'essay_id',
    'title',
    'has_ended',
    'bounty',
    'email',
    'upload_datetime',
    'subject',
    'language',
    'essay_text',
    'essay_correction_json',
    'errors',
    'is_valid'
    ]

    list_display = ('author', 'has_ended', 'subject', 'essay_id', 'upload_datetime', 'is_valid', 'shorter_essay_text', 'language', 'characters')
    readonly_fields = ['essay_id', 'upload_datetime']
    ordering = ('-upload_datetime',)

class AnswerAdmin(admin.ModelAdmin):
    fields = [
    'author',
    'answer_id',
    'essay',
    'answer_text',
    'upload_datetime',
    'winner',
    'upvotes',
    'downvotes'
    ]

    list_display = ('author', 'answer_id', 'essay', 'answer_text', 'winner', 'upvotes', 'downvotes', 'upload_datetime', 'shorter_answer_text')
    readonly_fields = ['answer_id', 'upload_datetime']
    ordering = ('-upload_datetime',)

class ProfileAdmin(admin.ModelAdmin):
    fields = [
    'user',
    'biography',
    'coins'
    ]
    list_display = ('user', 'coins')

class NotificationAdmin(admin.ModelAdmin):
    fields = [
    'recipient',
    'sender',
    'verb',
    'timestamp',
    'unread',
    ]
    list_display = ('recipient', 'sender', 'verb', 'timestamp', 'unread')
    ordering = ('-timestamp')

admin.site.register(Essay, EssayAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Profile, ProfileAdmin)
