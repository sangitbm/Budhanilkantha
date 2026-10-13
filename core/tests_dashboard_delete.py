from django.test import TransactionTestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile

from news.models import Notice, Event
from gallery.models import Photo
from records.models import Student, Staff
from core.models import Testimonial, AcademicProgram, SiteSettings
from core.signals import get_file_fields
import os
import unittest.mock

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
        
        self.assertEqual(content.count("autofocus"), 1)
        self.assertRegex(content, r'<a[^>]*href="[^"]*"[^>]*class="del-btn del-btn-cancel"[^>]*autofocus[^>]*>')
        self.assertContains(resp, 'href="/dashboard/"')

        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        
    def test_notice_delete(self):
        n = Notice.objects.create(title="Test Notice")
        self.check_delete_view(reverse('delete-notice', args=[n.pk]), "notice", "Test Notice")
        
    def test_event_delete(self):
        e = Event.objects.create(title="Test Event")
        url = reverse('delete-event', args=[e.pk])
        self.client.login(username='staff', password='pwd')
        resp = self.client.get(url)
        self.assertNotContains(resp, 'The attached file will also be deleted.')
        self.check_delete_view(url, "event", "Test Event")
        
        e_with_file = Event.objects.create(title="Test Event 2", file_attachment=self.get_test_file("doc.pdf"))
        self.client.login(username='staff', password='pwd')
        resp2 = self.client.get(reverse('delete-event', args=[e_with_file.pk]))
        self.assertContains(resp2, 'The attached file will also be deleted.')

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

    def test_get_file_fields(self):
        n_with_file = Notice(title="Notice With File", file_attachment=self.get_test_file("notice.pdf"))
        self.assertEqual(get_file_fields(n_with_file), ['file_attachment'])

        n_without_file = Notice(title="Notice Without File")
        self.assertEqual(get_file_fields(n_without_file), [])

        s_with_photo = Student(first_name="Alice", photo=self.get_test_file("student.jpg"))
        self.assertEqual(get_file_fields(s_with_photo), ['photo'])

        staff = Staff(first_name="Bob")
        self.assertEqual(get_file_fields(staff), [])

        with unittest.mock.patch.dict('core.signals.FILE_FIELDS', {Staff: ['custom_file']}, clear=False):
            staff.custom_file = self.get_test_file("custom.pdf")
            self.assertEqual(get_file_fields(staff), ['custom_file'])
            staff.custom_file = None
            self.assertEqual(get_file_fields(staff), [])
