from datetime import date, time, timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from academics.models import AcademicSession, Term
from academics.forms import make_term_formset
from academics.services import find_overlapping_session
from news.models import Event

User = get_user_model()


class Part0Tests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username='staff_part0',
            password='password123',
            is_staff=True
        )
        self.client.login(username='staff_part0', password='password123')
        self.session = AcademicSession.objects.create(
            name="2083",
            start_date=date(2026, 4, 14),
            end_date=date(2027, 4, 13),
            is_current=True,
        )
        self.term1 = Term.objects.create(
            session=self.session,
            name="First Terminal",
            start_date=date(2026, 4, 15),
            end_date=date(2026, 8, 15),
            order=1,
        )
        self.term2 = Term.objects.create(
            session=self.session,
            name="Second Terminal",
            start_date=date(2026, 8, 16),
            end_date=date(2026, 12, 15),
            order=2,
        )

    def test_dashboard_overview_events_display_and_ordering(self):
        from django.utils import timezone
        today = timezone.localdate()
        # Event with event_date and start_time
        e1 = Event.objects.create(
            title="Science Fair",
            event_date=today + timedelta(days=2),
            start_time=time(10, 30),
        )
        # Event with event_date but no start_time
        e2 = Event.objects.create(
            title="Sports Meet",
            event_date=today + timedelta(days=5),
            start_time=None,
        )
        # Event with no event_date
        e3 = Event.objects.create(
            title="Annual Gala",
            event_date=None,
            start_time=None,
        )

        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()

        # Date and time formatting
        d1_str = (today + timedelta(days=2)).strftime("%b %d, %Y")
        d2_str = (today + timedelta(days=5)).strftime("%b %d, %Y")
        self.assertIn(f"{d1_str} 10:30 AM", content)
        self.assertIn(d2_str, content)
        self.assertIn("Date to be announced", content)

        # Overview events query ordering check
        events = list(resp.context['upcoming_events'])
        self.assertEqual(events[0], e1)
        self.assertEqual(events[1], e2)
        self.assertEqual(events[2], e3)

    def test_term_order_swap_in_one_save(self):
        # Swap term1 (1 -> 2) and term2 (2 -> 1)
        post_data = {
            'name': '2083',
            'start_date': '2026-04-14',
            'end_date': '2027-04-13',
            'terms-TOTAL_FORMS': '2',
            'terms-INITIAL_FORMS': '2',
            'terms-MIN_NUM_FORMS': '0',
            'terms-MAX_NUM_FORMS': '8',
            'terms-0-id': str(self.term1.pk),
            'terms-0-name': 'First Terminal',
            'terms-0-start_date': '2026-04-15',
            'terms-0-end_date': '2026-08-15',
            'terms-0-order': '2',  # was 1
            'terms-1-id': str(self.term2.pk),
            'terms-1-name': 'Second Terminal',
            'terms-1-start_date': '2026-08-16',
            'terms-1-end_date': '2026-12-15',
            'terms-1-order': '1',  # was 2
        }
        resp = self.client.post(reverse('edit-session', kwargs={'pk': self.session.pk}), post_data)
        self.assertRedirects(resp, reverse('dashboard-sessions'))

        self.term1.refresh_from_db()
        self.term2.refresh_from_db()
        self.assertEqual(self.term1.order, 2)
        self.assertEqual(self.term2.order, 1)

    def test_term_delete_and_reuse_order(self):
        # Delete term1 (order 1) and add new term with order 1
        post_data = {
            'name': '2083',
            'start_date': '2026-04-14',
            'end_date': '2027-04-13',
            'terms-TOTAL_FORMS': '3',
            'terms-INITIAL_FORMS': '2',
            'terms-MIN_NUM_FORMS': '0',
            'terms-MAX_NUM_FORMS': '8',
            'terms-0-id': str(self.term1.pk),
            'terms-0-name': 'First Terminal',
            'terms-0-start_date': '2026-04-15',
            'terms-0-end_date': '2026-08-15',
            'terms-0-order': '1',
            'terms-0-DELETE': 'on',
            'terms-1-id': str(self.term2.pk),
            'terms-1-name': 'Second Terminal',
            'terms-1-start_date': '2026-08-16',
            'terms-1-end_date': '2026-12-15',
            'terms-1-order': '2',
            'terms-2-name': 'New Replacement Term',
            'terms-2-start_date': '2026-04-15',
            'terms-2-end_date': '2026-08-15',
            'terms-2-order': '1',
        }
        resp = self.client.post(reverse('edit-session', kwargs={'pk': self.session.pk}), post_data)
        self.assertRedirects(resp, reverse('dashboard-sessions'))

        self.assertFalse(Term.objects.filter(pk=self.term1.pk).exists())
        new_term = Term.objects.get(name='New Replacement Term')
        self.assertEqual(new_term.order, 1)

    def test_template_tidy_sentence_case_and_error_summary_labels(self):
        resp = self.client.get(reverse('add-session'))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()

        # No duplicate h1 in content area
        main_content = content.split('<main class="main-content">')[1]
        self.assertEqual(main_content.count('<h1'), 1)

        # Sentence case labels
        self.assertIn('Year name', content)
        self.assertIn('Start date', content)
        self.assertIn('End date', content)

        # BS hint present on create page for prefilled defaults
        self.assertIn('in Bikram Sambat', content)

        # Test error summary uses field labels, not "Start_date"
        post_data = {
            'name': '',
            'start_date': '2026-10-10',
            'end_date': '2026-10-01',  # invalid: before start
            'terms-TOTAL_FORMS': '0',
            'terms-INITIAL_FORMS': '0',
            'terms-MIN_NUM_FORMS': '0',
            'terms-MAX_NUM_FORMS': '8',
        }
        resp_err = self.client.post(reverse('add-session'), post_data)
        self.assertEqual(resp_err.status_code, 200)
        err_content = resp_err.content.decode()
        self.assertNotIn('Start_date', err_content)
        self.assertIn('End date', err_content)

    def test_overview_card_pluralize_and_shell_css(self):
        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()

        # Shell CSS linked
        self.assertIn('dashboard_shell.css', content)
        # Renamed classes present
        self.assertIn('dash-header-chip', content)
        self.assertIn('dash-sidebar-section-label', content)

        # Pluralize in overview card
        self.assertTrue('days left in the year' in content or 'day left in the year' in content)

    def test_find_overlapping_session_helper(self):
        # Overlaps with 2083
        overlap = find_overlapping_session(date(2026, 6, 1), date(2026, 9, 1))
        self.assertEqual(overlap, self.session)

        # Exclude 2083
        no_overlap = find_overlapping_session(date(2026, 6, 1), date(2026, 9, 1), exclude_pk=self.session.pk)
        self.assertIsNone(no_overlap)

    def test_make_term_formset_helper(self):
        FormSetCls = make_term_formset(extra=5)
        fs = FormSetCls(queryset=Term.objects.none())
        self.assertEqual(fs.extra, 5)
