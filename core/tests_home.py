from django.test import TestCase
from django.urls import reverse
from core.models import SiteSettings

class HomeHeroTestCase(TestCase):
    def test_hero_h1_shows_tagline(self):
        settings = SiteSettings.get_settings()
        settings.tagline = "Test Custom Tagline"
        settings.save()
        
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test")
        self.assertContains(response, "Custom Tagline")

    def test_principal_card_renders(self):
        settings = SiteSettings.get_settings()
        settings.principal_name = 'Test Principal Name'
        settings.principal_message = 'Test Principal Message'
        settings.save()
        
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Principal Name')
        self.assertContains(response, 'Test Principal Message')

    def test_programs_section_shows(self):
        from core.models import AcademicProgram
        settings = SiteSettings.get_settings()
        AcademicProgram.objects.create(site_settings=settings, title='Prog1', description='Desc1')
        AcademicProgram.objects.create(site_settings=settings, title='Prog2', description='Desc2')
        
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Prog1')
        self.assertContains(response, 'Desc1')
        self.assertContains(response, 'Prog2')
        self.assertContains(response, 'Desc2')
        
    def test_programs_section_hidden_when_empty(self):
        from core.models import AcademicProgram
        AcademicProgram.objects.all().delete()
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, 'Academic Programs We Offer')

    def test_footer_shows_phone_and_email(self):
        settings = SiteSettings.get_settings()
        settings.phone_primary = '+977-9876543210'
        settings.email_general = 'testfooter@example.com'
        settings.save()
        
        response = self.client.get(reverse('home'))
        self.assertContains(response, '+977-9876543210')
        self.assertContains(response, 'testfooter@example.com')

    def test_footer_shows_info_officer(self):
        settings = SiteSettings.get_settings()
        settings.info_officer_name = 'Test Officer'
        settings.info_officer_phone = '9800000000'
        settings.save()
        
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Test Officer')
        self.assertContains(response, '9800000000')

    def test_footer_hides_social_links_when_empty(self):
        settings = SiteSettings.get_settings()
        settings.facebook_url = ''
        settings.youtube_url = ''
        settings.save()
        
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, 'aria-label="Facebook"')
        self.assertNotContains(response, 'aria-label="YouTube"')

    def test_title_and_testimonials_section(self):
        from core.models import Testimonial
        import re
        Testimonial.objects.create(name='John Doe', quote='Great school!', is_published=True)
        response = self.client.get(reverse('home'))
        
        # Check title
        content = response.content.decode('utf-8')
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        self.assertIsNotNone(title_match)
        title_text = title_match.group(1).strip()
        self.assertNotIn('<', title_text)
        self.assertLess(len(title_text), 100)
        
        # Check tst-section appears exactly once
        self.assertEqual(content.count('class="tst-section"'), 1)
