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
    'essay_text',
    ]
    list_display = ('essay_id', 'email', 'upload_datetime', 'characters', 'price', 'currency', 'paid', 'completed', 'essay_text')
    readonly_fields = ['essay_id']

admin.site.register(Essay, EssayAdmin)
