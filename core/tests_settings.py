from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import SiteSettings
from core.forms import SiteSettingsForm

class SiteSettingsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        self.client.login(username='admin', password='adminpass')
        self.settings = SiteSettings.get_settings()

    def test_all_form_fields_rendered(self):
        response = self.client.get(reverse('dashboard-settings'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        
        form_fields = SiteSettingsForm.Meta.fields
        for field in form_fields:
            # check if name="field" or id="id_field" exists in HTML
            expected_name = f'name="{field}"'
            self.assertIn(expected_name, content, f"Field {field} is missing from dashboard-settings.html")
