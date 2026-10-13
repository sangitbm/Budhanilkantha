from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache
from datetime import timedelta, date, time

from core.models import SiteSettings, Testimonial
from news.models import Notice, Event
from gallery.models import Photo

User = get_user_model()

class DashboardToHomepageIntegrationTests(TestCase):
    def setUp(self):
        cache.clear()
        self.staff_user = User.objects.create_user(
            username='admin_staff',
            password='Password123!',
            is_staff=True
        )
        self.client.login(username='admin_staff', password='Password123!')
        self.settings = SiteSettings.get_settings()
        self.settings.school_name = "Budhanilkantha Academy"
        self.settings.tagline = "Empowering Future Leaders"
        self.settings.ticker_enabled = True
        self.settings.save()

    def test_homepage_loads_settings_and_branding(self):
        """Verify homepage dynamically displays site settings from dashboard."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Budhanilkantha Academy")
        self.assertContains(response, "Empowering")

    def test_notice_dashboard_creation_reflected_in_ticker_and_homepage(self):
        """Creating a notice with show_in_ticker=True reflects on public homepage ticker."""
        Notice.objects.create(
            title="Winter Vacation Announced",
            description="School remains closed next week.",
            show_in_ticker=True
        )
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Winter Vacation Announced")

    def test_testimonial_dashboard_creation_reflected_on_homepage(self):
        """Published testimonials created in dashboard appear in homepage Student Voices section."""
        Testimonial.objects.create(
            name="Suman Thapa",
            role="Alumnus 2024",
            quote="Budhanilkantha shaped my career in engineering.",
            is_published=True,
            order=1
        )
        Testimonial.objects.create(
            name="Hidden Reviewer",
            role="Parent",
            quote="This should not be displayed on homepage.",
            is_published=False,
            order=2
        )
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Suman Thapa")
        self.assertContains(response, "Budhanilkantha shaped my career in engineering.")
        self.assertNotContains(response, "Hidden Reviewer")

    def test_event_dashboard_creation_reflected_in_events_page(self):
        """Upcoming events scheduled in dashboard appear with proper date/time on /events/."""
        tomorrow = date.today() + timedelta(days=1)
        Event.objects.create(
            title="Annual Sports Gala",
            description="Track and field competitions.",
            event_date=tomorrow,
            start_time=time(9, 30),
            end_time=time(16, 0),
            location="Main Sports Arena"
        )
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Annual Sports Gala")
        self.assertContains(response, "Main Sports Arena")

    def test_gallery_photo_dashboard_creation_reflected_in_public_gallery(self):
        """Photos added via dashboard appear on public gallery page."""
        dummy_img = SimpleUploadedFile("test.jpg", b"\x47\x49\x46\x38\x39\x61\x01\x00\x01", content_type="image/jpeg")
        Photo.objects.create(
            title="Robotics Exhibition",
            description="Students demonstrating AI models.",
            image=dummy_img,
            is_featured=True
        )
        response = self.client.get(reverse('gallery'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Robotics Exhibition")

    def test_contact_form_submission_reflected_in_dashboard_messages(self):
        """Messages sent from public contact page show up in Dashboard Messages."""
        client_guest = self.client_class()
        contact_data = {
            'name': 'Bikram Karki',
            'email': 'bikram@example.com',
            'subject': 'Inquiry regarding admission fees',
            'message': 'Could you please send the detailed fee breakdown?',
        }
        post_response = client_guest.post(reverse('contact'), contact_data)
        self.assertEqual(post_response.status_code, 302)
        
        # Verify in dashboard as staff
        dash_response = self.client.get(reverse('dashboard-messages'))
        self.assertEqual(dash_response.status_code, 200)
        self.assertContains(dash_response, "Bikram Karki")
        self.assertContains(dash_response, "Inquiry regarding admission fees")

    def test_admissions_submission_reflected_in_dashboard_admissions(self):
        """Public admission inquiries appear in Dashboard Admissions."""
        client_guest = self.client_class()
        admission_data = {
            'student_name': 'Rohan Shrestha',
            'parent_name': 'Govinda Shrestha',
            'email': 'rohan@example.com',
            'phone_number': '9841000000',
            'grade_applying_for': 'Class 11 Science'
        }
        post_response = client_guest.post(reverse('admissions'), admission_data)
        self.assertEqual(post_response.status_code, 302)

        dash_response = self.client.get(reverse('dashboard-admissions'))
        self.assertEqual(dash_response.status_code, 200)
        self.assertContains(dash_response, "Rohan Shrestha")
        self.assertContains(dash_response, "Class 11 Science")

    def test_all_dashboard_views_accessible_for_staff(self):
        """Verify all admin dashboard endpoints return HTTP 200 for staff."""
        urls = [
            reverse('dashboard'),
            reverse('dashboard-notices'),
            reverse('dashboard-events'),
            reverse('dashboard-gallery'),
            reverse('dashboard-students'),
            reverse('dashboard-staff'),
            reverse('dashboard-admissions'),
            reverse('dashboard-testimonials'),
            reverse('dashboard-settings'),
            reverse('dashboard-messages'),
            reverse('add-notice'),
            reverse('add-event'),
            reverse('add-photo'),
            reverse('add-student'),
            reverse('add-staff'),
            reverse('testimonial-add'),
        ]
        for url in urls:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200, f"Failed accessing dashboard URL: {url}")
