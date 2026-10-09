from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import SiteSettings, AcademicProgram, Testimonial, AdmissionInquiry
from news.models import Notice
from gallery.models import Photo
from records.models import Student, Staff
from django.core.files.uploadedfile import SimpleUploadedFile

class AccessControlTests(TestCase):
    def setUp(self):
        # Create Users
        self.staff_user = User.objects.create_user(username='staff', password='pwd', is_staff=True, is_active=True)
        self.non_staff = User.objects.create_user(username='normal', password='pwd', is_staff=False, is_active=True)

        # Create Objects for parameterized views
        settings = SiteSettings.get_settings()
        self.program = AcademicProgram.objects.create(site_settings=settings, title="Program")
        self.testimonial = Testimonial.objects.create(name="T", quote="Q")
        self.notice = Notice.objects.create(title="N", description="C")
        self.photo = Photo.objects.create(title="P", image=SimpleUploadedFile("t.jpg", b"000"))
        self.student = Student.objects.create(first_name="F", last_name="L", grade="Grade 1", date_of_birth="2015-01-01", guardian_name="G", address="A")
        self.staff = Staff.objects.create(first_name="F", last_name="L", staff_type="TEACHER", date_of_joining="2020-01-01")

        self.dashboard_urls = [
            reverse('dashboard'),
            reverse('dashboard-admissions'),
            reverse('dashboard-settings'),
            reverse('program-remove', kwargs={'pk': self.program.pk}),
            reverse('dashboard-testimonials'),
            reverse('testimonial-add'),
            reverse('testimonial-edit', kwargs={'pk': self.testimonial.pk}),
            reverse('testimonial-delete', kwargs={'pk': self.testimonial.pk}),
            reverse('dashboard-notices'),
            reverse('add-notice'),
            reverse('edit-notice', kwargs={'pk': self.notice.pk}),
            reverse('delete-notice', kwargs={'pk': self.notice.pk}),
            reverse('dashboard-gallery'),
            reverse('add-photo'),
            reverse('edit-photo', kwargs={'pk': self.photo.pk}),
            reverse('delete-photo', kwargs={'pk': self.photo.pk}),
            reverse('dashboard-students'),
            reverse('add-student'),
            reverse('edit-student', kwargs={'pk': self.student.pk}),
            reverse('delete-student', kwargs={'pk': self.student.pk}),
            reverse('dashboard-staff'),
            reverse('add-staff'),
            reverse('edit-staff', kwargs={'pk': self.staff.pk}),
            reverse('delete-staff', kwargs={'pk': self.staff.pk}),
        ]

        self.public_urls = [
            reverse('home'),
            reverse('about'),
            reverse('contact'),
            reverse('events'),
            reverse('admissions'),
            reverse('teachers'),
            reverse('staff-directory'),
            reverse('public-notices'),
            reverse('gallery'),
            reverse('login'),
        ]

    def test_anonymous_user_redirected(self):
        for url in self.dashboard_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302, f"Expected 302 for {url}, got {response.status_code}")
            self.assertTrue(response.url.startswith(reverse('login')), f"Redirect for {url} should go to login")

    def test_non_staff_forbidden(self):
        self.client.login(username='normal', password='pwd')
        for url in self.dashboard_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403, f"Expected 403 for {url}, got {response.status_code}")
        
        # Test POST returns 403 and nothing is changed
        initial_notice_count = Notice.objects.count()
        response = self.client.post(reverse('delete-notice', kwargs={'pk': self.notice.pk}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Notice.objects.count(), initial_notice_count)

    def test_staff_allowed(self):
        self.client.login(username='staff', password='pwd')
        for url in self.dashboard_urls:
            if 'delete' not in url and 'remove' not in url:
                response = self.client.get(url)
                self.assertIn(response.status_code, [200, 302], f"Expected 200/302 for {url}")
        
        # Test POST success (redirects)
        response = self.client.post(reverse('delete-notice', kwargs={'pk': self.notice.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Notice.objects.filter(pk=self.notice.pk).exists())

    def test_public_urls_open(self):
        for url in self.public_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Expected 200 for {url}")

    def test_staff_directory_privacy(self):
        self.staff.show_contact_publicly = False
        self.staff.contact_number = "9998887776"
        self.staff.email = "hidden@school.com"
        self.staff.save()

        response = self.client.get(reverse('staff-directory'))
        self.assertNotContains(response, "9998887776")
        self.assertNotContains(response, "hidden@school.com")

        self.staff.show_contact_publicly = True
        self.staff.save()

        response = self.client.get(reverse('staff-directory'))
        self.assertContains(response, "9998887776")
        self.assertContains(response, "hidden@school.com")

    def test_migration_default_false(self):
        staff = Staff.objects.create(first_name="T", last_name="S", staff_type="SUPPORT", date_of_joining="2020-01-01")
        self.assertFalse(staff.show_contact_publicly)
