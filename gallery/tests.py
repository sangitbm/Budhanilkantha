from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Photo
from django.core.files.uploadedfile import SimpleUploadedFile

class GalleryTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staff', password='pwd', is_staff=True, is_active=True)
        self.client.login(username='staff', password='pwd')
        
    def test_photo_upload_page_rendering(self):
        """Test that the photo upload page renders correctly using the gallery/photo_form.html template."""
        response = self.client.get(reverse('add-photo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gallery/photo_form.html')
        
    def test_successful_photo_submission(self):
        """Test that a photo can be successfully uploaded."""
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b',
            content_type='image/jpeg'
        )
        data = {
            'title': 'My Test Photo',
            'image': image
        }
        response = self.client.post(reverse('add-photo'), data)
        # Should redirect to dashboard-gallery on success
        self.assertRedirects(response, reverse('dashboard-gallery'))
        self.assertTrue(Photo.objects.filter(title='My Test Photo').exists())
