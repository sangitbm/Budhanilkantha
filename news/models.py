from django.db import models
from django.core.cache import cache

class Notice(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file_attachment = models.FileField(upload_to='notices/', blank=True, null=True)
    show_in_ticker = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        cache.delete('ticker_notices')
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        cache.delete('ticker_notices')
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    file_attachment = models.FileField(upload_to='events/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title