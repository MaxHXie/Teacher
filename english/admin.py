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
    ]
    list_display = ('essay_id', 'email', 'upload_datetime', 'characters', 'price', 'currency', 'paid', 'completed', 'were_limited', 'shorter_essay_text')
    readonly_fields = ['essay_id']

    ordering = ('-upload_datetime',)

admin.site.register(Essay, EssayAdmin)
