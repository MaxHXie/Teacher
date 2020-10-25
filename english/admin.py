from django.contrib import admin

from .models import Essay

class EssayAdmin(admin.ModelAdmin):
    fields = [
    'essay_id',
    'email',
    'upload_datetime',
    'characters',
    'price',
    'currency',
    'paid',
    'completed',
    'were_limited',
    'essay_text',
    'essay_correction_json',
    'errors',
    'corrections'
    ]

    list_display = ('essay_id', 'email', 'upload_datetime', 'characters', 'price', 'currency', 'paid', 'completed', 'were_limited', 'shorter_essay_text')
    readonly_fields = ['essay_id', 'upload_datetime']
    ordering = ('-upload_datetime',)

admin.site.register(Essay, EssayAdmin)
