from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import SiteSettings, AcademicProgram

class AcademicProgramDeletionTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Users
        self.staff_user = User.objects.create_superuser('staff', 'staff@example.com', 'password')
        self.normal_user = User.objects.create_user('normal', 'normal@example.com', 'password')
        
        # SiteSettings
        self.settings = SiteSettings.get_settings()
        
        # Other settings obj (for the cross-site check)
        self.other_settings = SiteSettings.objects.create(school_name="Other")
        
        # Programs
        self.prog1 = AcademicProgram.objects.create(site_settings=self.settings, title='Prog 1')
        self.prog2 = AcademicProgram.objects.create(site_settings=self.settings, title='Prog 2')
        self.other_prog = AcademicProgram.objects.create(site_settings=self.other_settings, title='Other Prog')
        
        self.remove_url = reverse('program-remove', args=[self.prog1.id])

    def test_anonymous_user_redirected(self):
        # GET
        response = self.client.get(self.remove_url)
        self.assertRedirects(response, f"/admin/login/?next={self.remove_url}")
        
        # POST
        response = self.client.post(self.remove_url)
        self.assertRedirects(response, f"/admin/login/?next={self.remove_url}")
        self.assertTrue(AcademicProgram.objects.filter(id=self.prog1.id).exists())

    def test_non_staff_user_forbidden(self):
        self.client.login(username='normal', password='password')
        
        # GET
        response = self.client.get(self.remove_url)
        self.assertEqual(response.status_code, 403)
        
        # POST
        response = self.client.post(self.remove_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(AcademicProgram.objects.filter(id=self.prog1.id).exists())

    def test_get_does_not_delete(self):
        self.client.login(username='staff', password='password')
        response = self.client.get(self.remove_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/confirm_remove_program.html')
        self.assertTrue(AcademicProgram.objects.filter(id=self.prog1.id).exists())

    def test_post_deletes_program(self):
        self.client.login(username='staff', password='password')
        response = self.client.post(self.remove_url)
        
        self.assertRedirects(response, reverse('dashboard-settings') + '?tab=programs')
        self.assertFalse(AcademicProgram.objects.filter(id=self.prog1.id).exists())
        # Does not affect other programs
        self.assertTrue(AcademicProgram.objects.filter(id=self.prog2.id).exists())

    def test_cannot_delete_other_sites_program(self):
        self.client.login(username='staff', password='password')
        url = reverse('program-remove', args=[self.other_prog.id])
        
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(AcademicProgram.objects.filter(id=self.other_prog.id).exists())
