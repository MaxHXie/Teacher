from django.db import models

class Essay(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField()
    upload_datetime = models.DateTimeField('date uploaded')
    words = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    paid = models.BooleanField()

    def __str__(self):
        return self.title
