from django.db import models

# Create your models here.
class Photo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='photos/')
    date_taken = models.DateField(null=True, blank=True, help_text="Optional date when the photo was taken")
    is_featured = models.BooleanField(default=False, help_text="Show this photo in featured galleries")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title