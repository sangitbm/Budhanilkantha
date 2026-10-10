from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import timedelta
from news.models import Event

class EventsPageTests(TestCase):
    def test_undated_events_last(self):
        today = timezone.localdate()
        dated_event = Event.objects.create(title="Dated Event", description="D", event_date=today)
        undated_event = Event.objects.create(title="Undated Event", description="U", event_date=None)
        
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)
        events = list(response.context['events'])
        self.assertEqual(events[0], dated_event)
        self.assertEqual(events[1], undated_event)

    def test_dated_and_undated_cards(self):
        today = timezone.localdate()
        Event.objects.create(title="Dated Event", description="D", event_date=today)
        Event.objects.create(title="Undated Event", description="U", event_date=None)
        
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)
        
        month_abbr = today.strftime('%b').upper()
        day_str = str(today.day)
        
        self.assertContains(response, month_abbr)
        self.assertContains(response, day_str)
        self.assertContains(response, "TBA")
        self.assertContains(response, "Date to be announced")

    def test_attachment_link_and_extension(self):
        today = timezone.localdate()
        dummy_file = SimpleUploadedFile("schedule.pdf", b"file_content", content_type="application/pdf")
        Event.objects.create(title="Upcoming PDF", description="D", event_date=today, file_attachment=dummy_file)
        past_file = SimpleUploadedFile("old.pdf", b"file_content", content_type="application/pdf")
        Event.objects.create(title="Past PDF", description="D", event_date=today - timedelta(days=1), file_attachment=past_file)
        
        response = self.client.get(reverse('events'))
        self.assertContains(response, "Download attachment")
        self.assertContains(response, "PDF")
        
        self.assertNotContains(response, "old.pdf")

    def test_past_events_limit_and_opacity(self):
        today = timezone.localdate()
        for i in range(15):
            Event.objects.create(title=f"Past {i}", description="D", event_date=today - timedelta(days=i+1))
            
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)
        past_events = response.context['past_events']
        self.assertEqual(len(past_events), 10)
        
        self.assertNotContains(response, "opacity:")

    def test_empty_state(self):
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No upcoming events right now")
        self.assertEqual(response.content.decode().count("No upcoming events right now"), 1)

    def test_no_inline_styles_and_emojis(self):
        today = timezone.localdate()
        Event.objects.create(title="Test Event", description="Test", event_date=today, location="Hall")
        response = self.client.get(reverse('events'))
        content = response.content.decode('utf-8')
        
        self.assertNotIn("🗓", content)
        self.assertNotIn("📎", content)
        self.assertNotIn("📍", content)
        
        events_section = content.split('<section class="events')[1]
        self.assertNotIn('style="', events_section)
