with open('core/models.py', 'r', encoding='utf-8') as f:
    text = f.read()

append_text = '''
from django.core.exceptions import ValidationError

def validate_image_size(image):
    file_size = image.file.size
    limit_mb = 2
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(f"Max size of file is {limit_mb} MB")

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="e.g. Student (Grade 10)")
    quote = models.TextField(help_text="Max 300 characters")
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True, validators=[validate_image_size])
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def clean(self):
        super().clean()
        if self.quote and len(self.quote) > 300:
            raise ValidationError({'quote': 'Quote cannot exceed 300 characters.'})

    def __str__(self):
        return f"{self.name} - {self.role}"
'''

if 'class Testimonial' not in text:
    with open('core/models.py', 'a', encoding='utf-8') as f:
        f.write(append_text)
    print('Added Testimonial model')
else:
    print('Testimonial already in models.py')
