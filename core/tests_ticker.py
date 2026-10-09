from django.test import TestCase
from django.urls import reverse
from news.models import Notice
from core.models import SiteSettings

class TickerTestCase(TestCase):
    def setUp(self):
        from django.core.cache import cache
        cache.clear()
        # Create site settings
        self.site_settings = SiteSettings.get_settings()
        self.site_settings.marquee_text = "Test Marquee"
        self.site_settings.ticker_enabled = True
        self.site_settings.save()
        
        # Create notices
        self.notices = []
        for i in range(6):
            notice = Notice.objects.create(
                title=f"Test Notice {i}",
                description=f"Content {i}", show_in_ticker=True
            )
            self.notices.append(notice)
            
    def test_ticker_renders_latest_notices(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Ticker should be in the HTML
        self.assertContains(response, '<div class="ticker"')
        
        # Latest 5 notices should be present (notices[5] to notices[1])
        for i in range(1, 6):
            self.assertContains(response, f"Test Notice {i}")
            
        # The 6th oldest notice (notices[0]) should NOT be in the ticker
        self.assertNotContains(response, "Test Notice 0")
        
        # Marquee text should be present
        self.assertContains(response, "Test Marquee")
        
        # Check no dismiss/close button exists in the ticker
        # (Since we removed dismissAnnouncement script and button)
        self.assertNotContains(response, "dismissAnnouncement")

    def test_ticker_not_rendered_when_empty(self):
        # Clear marquee and notices
        self.site_settings.marquee_text = ""
        self.site_settings.save()
        Notice.objects.all().delete()
        
        # Clear cache since it caches notices
        from django.core.cache import cache
        cache.delete('ticker_notices')
        
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Ticker should NOT be rendered
        self.assertNotContains(response, '<div class="ticker"')
