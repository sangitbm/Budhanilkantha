from django.test import TestCase
from django.urls import reverse
from gallery.models import Photo
from django.core.files.uploadedfile import SimpleUploadedFile

class GalleryListTestCase(TestCase):
    def setUp(self):
        # Create a dummy image for testing
        self.dummy_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\\x47\\x49\\x46\\x38\\x39\\x61\\x01\\x00\\x01\\x00\\x80\\x00\\x00\\x00\\x00\\x00\\xff\\xff\\xff\\x21\\xf9\\x04\\x01\\x00\\x00\\x00\\x00\\x2c\\x00\\x00\\x00\\x00\\x01\\x00\\x01\\x00\\x00\\x02\\x02\\x44\\x01\\x00\\x3b',
            content_type='image/jpeg'
        )

    def test_empty_gallery(self):
        response = self.client.get(reverse('gallery'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No photos have been uploaded yet')
        self.assertNotContains(response, 'class="gal-card"')

    def test_one_photo(self):
        Photo.objects.create(title='Photo 1', image=self.dummy_image)
        response = self.client.get(reverse('gallery'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Photo 1')
        self.assertEqual(response.context['paginator'].count, 1)

    def test_five_photos(self):
        for i in range(5):
            Photo.objects.create(title=f'Photo {i}', image=self.dummy_image)
        response = self.client.get(reverse('gallery'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['paginator'].count, 5)
        self.assertEqual(len(response.context['photos']), 5)

    def test_thirteen_photos_pagination(self):
        for i in range(13):
            Photo.objects.create(title=f'Photo {i}', image=self.dummy_image)
            
        # Page 1
        response = self.client.get(reverse('gallery'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['paginator'].count, 13)
        self.assertEqual(len(response.context['photos']), 12)
        
        # Page 2
        response2 = self.client.get(reverse('gallery') + '?page=2')
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(response2.context['photos']), 1)
