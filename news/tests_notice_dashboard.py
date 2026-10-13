from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from news.models import Notice

class NoticeDashboardTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staff', password='pwd', is_staff=True)
        self.normal_user = User.objects.create_user(username='norm', password='pwd')
        
    def test_access_permissions(self):
        url = reverse('dashboard-notices')
        
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith(reverse('login')))
        
        self.client.login(username='norm', password='pwd')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)
        
        self.client.login(username='staff', password='pwd')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_search_functionality(self):
        Notice.objects.create(title="Exam Schedule", description="Finals in March")
        Notice.objects.create(title="Holiday", description="No school tomorrow")
        
        self.client.login(username='staff', password='pwd')
        url = reverse('dashboard-notices')
        
        resp = self.client.get(url, {'q': 'eXam'})
        self.assertContains(resp, "Exam Schedule")
        self.assertNotContains(resp, "Holiday")
        
        resp = self.client.get(url, {'q': 'TOMORROW'})
        self.assertContains(resp, "Holiday")
        self.assertNotContains(resp, "Exam Schedule")

    def test_pagination(self):
        for i in range(16):
            Notice.objects.create(title=f"Notice {i}", description="Desc")
            
        self.client.login(username='staff', password='pwd')
        url = reverse('dashboard-notices')
        
        resp1 = self.client.get(url)
        self.assertEqual(len(resp1.context['notices']), 15)
        
        resp2 = self.client.get(url, {'page': '2'})
        self.assertEqual(len(resp2.context['notices']), 1)

    def test_toggle_ticker(self):
        notice = Notice.objects.create(title="Ticker Test", description="Desc", show_in_ticker=False)
        self.client.login(username='staff', password='pwd')
        
        url = reverse('toggle-notice-ticker', args=[notice.pk])
        
        resp_get = self.client.get(url)
        self.assertEqual(resp_get.status_code, 405)
        
        resp_post = self.client.post(url, {'next': '/dashboard/notices/?q=test'})
        self.assertEqual(resp_post.status_code, 302)
        self.assertEqual(resp_post.url, '/dashboard/notices/?q=test')
        
        notice.refresh_from_db()
        self.assertTrue(notice.show_in_ticker)
        
        resp_post2 = self.client.post(url, {'next': 'http://evil.com'})
        self.assertEqual(resp_post2.status_code, 302)
        self.assertEqual(resp_post2.url, reverse('dashboard-notices'))
        
        notice.refresh_from_db()
        self.assertFalse(notice.show_in_ticker)

    def test_empty_state_rendered(self):
        self.client.login(username='staff', password='pwd')
        url = reverse('dashboard-notices')
        resp = self.client.get(url)
        
        self.assertContains(resp, "No notices yet")
        self.assertContains(resp, "Add your first notice")
        self.assertNotContains(resp, "<table")

    def test_no_inline_styles_or_emojis(self):
        Notice.objects.create(title="Design Test", description="Check styles")
        self.client.login(username='staff', password='pwd')
        url = reverse('dashboard-notices')
        resp = self.client.get(url)
        
        content = resp.content.decode('utf-8')
        main_content = content.split('<main class="main-content">')[1]
        self.assertNotIn('style="', main_content)
        self.assertNotIn("📢", main_content)
        self.assertNotIn("📁", main_content)
        self.assertNotIn("📄", main_content)
        self.assertNotIn("✓", main_content)
        self.assertNotIn("✗", main_content)
