from django.contrib import admin

from .models import Essay

class EssayAdmin(admin.ModelAdmin):
    fields = [
    'essay_id',
    'email',
    'upload_datetime',
    'characters',
    'language',
    'essay_text',
    'essay_correction_json',
    'errors',
    ]

    list_display = ('essay_id', 'email', 'upload_datetime', 'language', 'characters', 'shorter_essay_text')
    readonly_fields = ['essay_id', 'upload_datetime']
    ordering = ('-upload_datetime',)

admin.site.register(Essay, EssayAdmin)
