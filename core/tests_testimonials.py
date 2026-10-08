from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Testimonial
from django.core.exceptions import ValidationError

class TestimonialTestCase(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user('staff', 'staff@example.com', 'staffpass', is_staff=True)
        self.normal_user = User.objects.create_user('normal', 'normal@example.com', 'normalpass', is_staff=False)
        
        Testimonial.objects.create(name='T1', quote='Quote1', is_published=True, order=1)
        Testimonial.objects.create(name='T2', quote='Quote2', is_published=True, order=2)
        Testimonial.objects.create(name='T3', quote='Quote3', is_published=True, order=3)
        Testimonial.objects.create(name='T4', quote='Quote4', is_published=True, order=4)
        Testimonial.objects.create(name='T_Draft', quote='DraftQuote', is_published=False, order=5)

    def test_unpublished_never_appear(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'T_Draft')
        self.assertNotContains(response, 'DraftQuote')

    def test_max_3_on_homepage(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Quote1')
        self.assertContains(response, 'Quote2')
        self.assertContains(response, 'Quote3')
        # Since T4 is order 4, it should not appear (only top 3)
        self.assertNotContains(response, 'Quote4')

    def test_quote_over_300_chars_rejected(self):
        long_quote = 'A' * 301
        t = Testimonial(name='Too Long', quote=long_quote)
        with self.assertRaises(ValidationError):
            t.full_clean()

    def test_staff_only_access_dashboard(self):
        # Unauthenticated
        response = self.client.get(reverse('dashboard-testimonials'))
        self.assertEqual(response.status_code, 302) # redirect to login
        
        # Normal user
        self.client.login(username='normal', password='normalpass')
        response = self.client.get(reverse('dashboard-testimonials'))
        self.assertEqual(response.status_code, 403) # forbidden

        # Staff user
        self.client.login(username='staff', password='staffpass')
        response = self.client.get(reverse('dashboard-testimonials'))
        self.assertEqual(response.status_code, 200)
