from django.contrib import admin

from .models import Essay

class EssayAdmin(admin.ModelAdmin):
    fields = [
    'upload_datetime',
    'words',
    'price',
    'currency',
    'paid',
    'completed',
    ]
    list_display = ('upload_datetime', 'words', 'price', 'currency', 'paid', 'completed')

admin.site.register(Essay, EssayAdmin)
