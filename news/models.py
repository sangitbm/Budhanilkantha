from django.db import models

class Notice(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file_attachment = models.FileField(upload_to='notices/', blank=True, null=True)
    show_in_ticker = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file_attachment = models.FileField(upload_to='notices/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title