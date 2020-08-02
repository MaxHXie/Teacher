from django.contrib import admin

from .models import Essay

class EssayAdmin(admin.ModelAdmin):
    fields = [
    'title',
    'file',
    'upload_datetime',
    'words',
    'price',
    'paid',
    ]
    list_display = ('title', 'file', 'upload_datetime', 'words', 'price', 'paid')

admin.site.register(Essay, EssayAdmin)
