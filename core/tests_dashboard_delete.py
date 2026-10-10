from django.test import TransactionTestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
import shutil

from news.models import Notice, Event
from gallery.models import Photo
from records.models import Student, Staff
from core.models import Testimonial, AcademicProgram, SiteSettings, HeroImage
import os

TEMP_MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class DashboardDeleteTests(TransactionTestCase):
    def setUp(self):
        self.staff = User.objects.create_user(username='staff', password='pwd', is_staff=True)
        self.norm = User.objects.create_user(username='norm', password='pwd')
        
        self.settings = SiteSettings.get_settings()
        self.program = AcademicProgram.objects.create(site_settings=self.settings, title="Test Program")
        
    def tearDown(self):
        for root, dirs, files in os.walk(TEMP_MEDIA_ROOT, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def get_test_file(self, name):
        return SimpleUploadedFile(name, b"file_content", content_type="image/jpeg")

    def check_delete_view(self, url, expected_title, label, is_program=False):
        self.client.logout()
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        
        self.client.login(username='norm', password='pwd')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)
        
        self.client.login(username='staff', password='pwd')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, f"Delete {expected_title}?")
        self.assertContains(resp, label)
        
        content = resp.content.decode('utf-8')
        main_content = content.split('<main class="main-content">')[1] if '<main class="main-content">' in content else content
        self.assertNotIn("⚠", main_content)
        self.assertNotIn("🗑", main_content)
        self.assertNotIn('style="', main_content)
        self.assertNotIn("javascript:", main_content)
        
        self.assertContains(resp, "autofocus")

        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        
    def test_notice_delete(self):
        n = Notice.objects.create(title="Test Notice")
        self.check_delete_view(reverse('delete-notice', args=[n.pk]), "notice", "Test Notice")
        
    def test_event_delete(self):
        e = Event.objects.create(title="Test Event")
        self.check_delete_view(reverse('delete-event', args=[e.pk]), "event", "Test Event")

    def test_photo_delete(self):
        p = Photo.objects.create(title="Test Photo", image=self.get_test_file("photo.jpg"))
        self.check_delete_view(reverse('delete-photo', args=[p.pk]), "photo", "Test Photo")

    def test_student_delete(self):
        s = Student.objects.create(first_name="John", last_name="Doe", roll_number="123", date_of_birth="2010-01-01", address="Secret Addr")
        self.client.login(username='staff', password='pwd')
        resp = self.client.get(reverse('delete-student', args=[s.pk]))
        self.assertNotContains(resp, "2010")
        self.assertNotContains(resp, "Secret")
        self.check_delete_view(reverse('delete-student', args=[s.pk]), "student", "John Doe - 123")
        
    def test_staff_delete(self):
        s = Staff.objects.create(first_name="Jane", last_name="Smith", designation="Teacher", date_of_joining="2020-01-01")
        self.check_delete_view(reverse('delete-staff', args=[s.pk]), "staff", "Jane Smith")

    def test_testimonial_delete(self):
        t = Testimonial.objects.create(name="Person", quote="A quote")
        self.check_delete_view(reverse('testimonial-delete', args=[t.pk]), "testimonial", "Person")

    def test_program_delete(self):
        self.check_delete_view(reverse('program-remove', args=[self.program.pk]), "program", "Test Program", True)
        
    def test_staff_deactivate(self):
        s = Staff.objects.create(first_name="Jane", last_name="Smith", date_of_joining="2020-01-01")
        url = reverse('staff-deactivate', args=[s.pk])
        
        self.client.login(username='staff', password='pwd')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 405)
        
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        s.refresh_from_db()
        self.assertFalse(s.is_active)
        
        self.client.login(username='norm', password='pwd')
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 403)

    def test_file_deletion_signals(self):
        n = Notice.objects.create(title="Test", file_attachment=self.get_test_file("test.pdf"))
        file_path = n.file_attachment.path
        self.assertTrue(os.path.exists(file_path))
        n.delete()
        self.assertFalse(os.path.exists(file_path))
        
        n2 = Notice.objects.create(title="Test2", file_attachment=self.get_test_file("test2.pdf"))
        file_path2 = n2.file_attachment.path
        n2.file_attachment = self.get_test_file("test3.pdf")
        n2.save()
        self.assertFalse(os.path.exists(file_path2))
        self.assertTrue(os.path.exists(n2.file_attachment.path))
        
        n3 = Notice.objects.create(title="Test3")
        n3.delete()
