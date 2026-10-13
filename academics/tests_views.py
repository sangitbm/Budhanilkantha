from datetime import date
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache

from academics.models import AcademicSession, Term


class AcademicViewsTests(TestCase):
    def setUp(self):
        cache.clear()
        self.staff_user = User.objects.create_user(
            username='staff',
            password='password123',
            is_staff=True,
        )
        self.regular_user = User.objects.create_user(
            username='regular',
            password='password123',
            is_staff=False,
        )
        self.client_staff = Client()
        self.client_staff.login(username='staff', password='password123')

        self.client_regular = Client()
        self.client_regular.login(username='regular', password='password123')

        self.client_anon = Client()

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

    def tearDown(self):
        cache.clear()

    # --- 1. Access Control ---
    def test_access_anonymous(self):
        urls = [
            reverse('dashboard-sessions'),
            reverse('add-session'),
            reverse('edit-session', kwargs={'pk': self.session.pk}),
            reverse('delete-session', kwargs={'pk': self.session.pk}),
            reverse('set-current-session', kwargs={'pk': self.session.pk}),
            reverse('duplicate-session', kwargs={'pk': self.session.pk}),
        ]
        for url in urls:
            resp = self.client_anon.get(url)
            self.assertEqual(resp.status_code, 302)

    def test_access_non_staff(self):
        urls = [
            ('GET', reverse('dashboard-sessions')),
            ('GET', reverse('add-session')),
            ('GET', reverse('edit-session', kwargs={'pk': self.session.pk})),
            ('GET', reverse('delete-session', kwargs={'pk': self.session.pk})),
            ('GET', reverse('set-current-session', kwargs={'pk': self.session.pk})),
            ('GET', reverse('duplicate-session', kwargs={'pk': self.session.pk})),
            ('POST', reverse('set-current-session', kwargs={'pk': self.session.pk})),
            ('POST', reverse('duplicate-session', kwargs={'pk': self.session.pk})),
        ]
        for method, url in urls:
            if method == 'GET':
                resp = self.client_regular.get(url)
            else:
                resp = self.client_regular.post(url)
            self.assertEqual(resp.status_code, 403, f"Failed for {method} {url}")

    def test_post_only_views_return_405_for_get(self):
        resp_set = self.client_staff.get(reverse('set-current-session', kwargs={'pk': self.session.pk}))
        self.assertEqual(resp_set.status_code, 405)

        resp_dup = self.client_staff.get(reverse('duplicate-session', kwargs={'pk': self.session.pk}))
        self.assertEqual(resp_dup.status_code, 405)

    # --- 2. List Page ---
    def test_list_view_with_sessions(self):
        resp = self.client_staff.get(reverse('dashboard-sessions'))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()
        self.assertIn("2083", content)
        self.assertIn("Current", content)
        self.assertIn("Apr 14, 2026", content)
        self.assertIn("2083 Baishakh 1", content)
        self.assertIn("2 terms", content)
        self.assertIn("First Terminal", content)
        self.assertIn("Second Terminal", content)
        self.assertIn("<table", content)

    def test_list_view_empty_state_no_table(self):
        Term.objects.all().delete()
        AcademicSession.objects.all().delete()
        cache.clear()

        resp = self.client_staff.get(reverse('dashboard-sessions'))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()
        self.assertIn("No academic years yet", content)
        self.assertIn("Create your first academic year to start adding classes, attendance, exams and fees.", content)
        self.assertIn("Create academic year", content)
        self.assertNotIn("<table", content)

    # --- 3. Create Page ---
    def test_create_get_prefills_default_dates_and_three_terms(self):
        resp = self.client_staff.get(reverse('add-session'))
        self.assertEqual(resp.status_code, 200)
        formset = resp.context['formset']
        self.assertEqual(len(formset.forms), 3)
        self.assertEqual(formset.forms[0].initial['name'], "First Terminal")
        self.assertEqual(formset.forms[1].initial['name'], "Second Terminal")
        self.assertEqual(formset.forms[2].initial['name'], "Final Terminal")

    def test_create_valid_post(self):
        post_data = {
            'name': '2084',
            'start_date': '2027-04-14',
            'end_date': '2028-04-13',
            'make_current': 'on',
            'terms-TOTAL_FORMS': '3',
            'terms-INITIAL_FORMS': '0',
            'terms-MIN_NUM_FORMS': '0',
            'terms-MAX_NUM_FORMS': '8',
            'terms-0-name': 'First Term',
            'terms-0-start_date': '2027-04-14',
            'terms-0-end_date': '2027-08-14',
            'terms-0-order': '1',
            'terms-1-name': 'Second Term',
            'terms-1-start_date': '2027-08-15',
            'terms-1-end_date': '2027-12-14',
            'terms-1-order': '2',
            'terms-2-name': 'Final Term',
            'terms-2-start_date': '2027-12-15',
            'terms-2-end_date': '2028-04-13',
            'terms-2-order': '3',
        }
        resp = self.client_staff.post(reverse('add-session'), post_data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, reverse('dashboard-sessions'))

        new_session = AcademicSession.objects.get(name='2084')
        self.assertTrue(new_session.is_current)
        self.assertEqual(new_session.terms.count(), 3)
        # Old session is no longer current
        self.session.refresh_from_db()
        self.assertFalse(self.session.is_current)

    def test_create_invalid_end_before_start(self):
        post_data = {
            'name': '2085',
            'start_date': '2028-04-14',
            'end_date': '2028-04-10',
            'terms-TOTAL_FORMS': '0',
            'terms-INITIAL_FORMS': '0',
            'terms-MIN_NUM_FORMS': '0',
            'terms-MAX_NUM_FORMS': '8',
        }
        resp = self.client_staff.post(reverse('add-session'), post_data)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(AcademicSession.objects.filter(name='2085').exists())
        self.assertContains(resp, "End date must be after start date.")

    def test_create_invalid_overlapping_session(self):
        post_data = {
            'name': '2083-Overlap',
            'start_date': '2026-05-01',
            'end_date': '2027-05-01',
            'terms-TOTAL_FORMS': '0',
            'terms-INITIAL_FORMS': '0',
            'terms-MIN_NUM_FORMS': '0',
            'terms-MAX_NUM_FORMS': '8',
        }
        resp = self.client_staff.post(reverse('add-session'), post_data)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(AcademicSession.objects.filter(name='2083-Overlap').exists())
        self.assertContains(resp, "Session dates overlap with an existing academic year")

    def test_create_invalid_term_outside_session(self):
        post_data = {
            'name': '2085',
            'start_date': '2028-04-14',
            'end_date': '2029-04-13',
            'terms-TOTAL_FORMS': '1',
            'terms-INITIAL_FORMS': '0',
            'terms-MIN_NUM_FORMS': '0',
            'terms-MAX_NUM_FORMS': '8',
            'terms-0-name': 'Out of Bounds',
            'terms-0-start_date': '2028-01-01',
            'terms-0-end_date': '2028-06-01',
            'terms-0-order': '1',
        }
        resp = self.client_staff.post(reverse('add-session'), post_data)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(AcademicSession.objects.filter(name='2085').exists())
        self.assertContains(resp, "Term dates must lie inside the academic year.")

    def test_create_invalid_overlapping_terms(self):
        post_data = {
            'name': '2085',
            'start_date': '2028-04-14',
            'end_date': '2029-04-13',
            'terms-TOTAL_FORMS': '2',
            'terms-INITIAL_FORMS': '0',
            'terms-MIN_NUM_FORMS': '0',
            'terms-MAX_NUM_FORMS': '8',
            'terms-0-name': 'Term A',
            'terms-0-start_date': '2028-04-15',
            'terms-0-end_date': '2028-08-15',
            'terms-0-order': '1',
            'terms-1-name': 'Term B',
            'terms-1-start_date': '2028-08-01',
            'terms-1-end_date': '2028-12-15',
            'terms-1-order': '2',
        }
        resp = self.client_staff.post(reverse('add-session'), post_data)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(AcademicSession.objects.filter(name='2085').exists())
        self.assertContains(resp, "Term dates overlap with another term.")

    def test_create_invalid_duplicate_term_name(self):
        post_data = {
            'name': '2085',
            'start_date': '2028-04-14',
            'end_date': '2029-04-13',
            'terms-TOTAL_FORMS': '2',
            'terms-INITIAL_FORMS': '0',
            'terms-MIN_NUM_FORMS': '0',
            'terms-MAX_NUM_FORMS': '8',
            'terms-0-name': 'Same Name',
            'terms-0-start_date': '2028-04-15',
            'terms-0-end_date': '2028-08-15',
            'terms-0-order': '1',
            'terms-1-name': 'Same Name',
            'terms-1-start_date': '2028-08-16',
            'terms-1-end_date': '2028-12-15',
            'terms-1-order': '2',
        }
        resp = self.client_staff.post(reverse('add-session'), post_data)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(AcademicSession.objects.filter(name='2085').exists())
        self.assertContains(resp, "is duplicated.")

    def test_create_invalid_duplicate_term_order(self):
        post_data = {
            'name': '2085',
            'start_date': '2028-04-14',
            'end_date': '2029-04-13',
            'terms-TOTAL_FORMS': '2',
            'terms-INITIAL_FORMS': '0',
            'terms-MIN_NUM_FORMS': '0',
            'terms-MAX_NUM_FORMS': '8',
            'terms-0-name': 'Term A',
            'terms-0-start_date': '2028-04-15',
            'terms-0-end_date': '2028-08-15',
            'terms-0-order': '1',
            'terms-1-name': 'Term B',
            'terms-1-start_date': '2028-08-16',
            'terms-1-end_date': '2028-12-15',
            'terms-1-order': '1',
        }
        resp = self.client_staff.post(reverse('add-session'), post_data)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(AcademicSession.objects.filter(name='2085').exists())
        self.assertContains(resp, "is duplicated.")

    # --- 4. Edit Page ---
    def test_edit_get_current_session_disabled_checkbox(self):
        resp = self.client_staff.get(reverse('edit-session', kwargs={'pk': self.session.pk}))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()
        self.assertIn("To change the current year, set another year as current.", content)
        self.assertTrue(resp.context['form'].fields['make_current'].disabled)

    def test_edit_valid_post_and_delete_term_and_ignore_empty_row(self):
        post_data = {
            'name': '2083-Renamed',
            'start_date': '2026-04-14',
            'end_date': '2027-04-13',
            'terms-TOTAL_FORMS': '3',
            'terms-INITIAL_FORMS': '2',
            'terms-MIN_NUM_FORMS': '0',
            'terms-MAX_NUM_FORMS': '8',
            # Keep term 1
            'terms-0-id': str(self.term1.pk),
            'terms-0-name': 'First Terminal Renamed',
            'terms-0-start_date': '2026-04-15',
            'terms-0-end_date': '2026-08-15',
            'terms-0-order': '1',
            # Delete term 2
            'terms-1-id': str(self.term2.pk),
            'terms-1-name': 'Second Terminal',
            'terms-1-start_date': '2026-08-16',
            'terms-1-end_date': '2026-12-15',
            'terms-1-order': '2',
            'terms-1-DELETE': 'on',
            # Extra empty untouched row
            'terms-2-name': '',
            'terms-2-start_date': '',
            'terms-2-end_date': '',
            'terms-2-order': '',
        }
        resp = self.client_staff.post(reverse('edit-session', kwargs={'pk': self.session.pk}), post_data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, reverse('dashboard-sessions'))

        self.session.refresh_from_db()
        self.assertEqual(self.session.name, '2083-Renamed')
        self.assertEqual(self.session.terms.count(), 1)
        self.term1.refresh_from_db()
        self.assertEqual(self.term1.name, 'First Terminal Renamed')
        self.assertFalse(Term.objects.filter(pk=self.term2.pk).exists())

    # --- 5. Set-current and Duplicate ---
    def test_set_current_session(self):
        session2 = AcademicSession.objects.create(
            name="2084",
            start_date=date(2027, 4, 14),
            end_date=date(2028, 4, 13),
            is_current=False,
        )
        resp = self.client_staff.post(reverse('set-current-session', kwargs={'pk': session2.pk}), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, reverse('dashboard-sessions'))
        self.assertContains(resp, "2084 is now the current academic year.")

        session2.refresh_from_db()
        self.session.refresh_from_db()
        self.assertTrue(session2.is_current)
        self.assertFalse(self.session.is_current)

    def test_duplicate_session_success_and_overlap_error(self):
        resp = self.client_staff.post(reverse('duplicate-session', kwargs={'pk': self.session.pk}), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, reverse('dashboard-sessions'))
        self.assertContains(resp, "Created 2084 with 2 terms. Dates moved forward by one Nepali year.")

        # Trying duplicate again triggers SessionOverlapError
        resp2 = self.client_staff.post(reverse('duplicate-session', kwargs={'pk': self.session.pk}), follow=True)
        self.assertEqual(resp2.status_code, 200)
        self.assertRedirects(resp2, reverse('dashboard-sessions'))
        self.assertContains(resp2, "An academic year already covers these dates: 2084.")
        self.assertEqual(AcademicSession.objects.count(), 2)

    # --- 6. Delete ---
    def test_delete_current_session_blocked(self):
        resp_get = self.client_staff.get(reverse('delete-session', kwargs={'pk': self.session.pk}), follow=True)
        self.assertEqual(resp_get.status_code, 200)
        self.assertRedirects(resp_get, reverse('dashboard-sessions'))
        self.assertContains(resp_get, "Set another year as current before deleting 2083.")

        resp_post = self.client_staff.post(reverse('delete-session', kwargs={'pk': self.session.pk}), follow=True)
        self.assertEqual(resp_post.status_code, 200)
        self.assertRedirects(resp_post, reverse('dashboard-sessions'))
        self.assertContains(resp_post, "Set another year as current before deleting 2083.")
        self.assertTrue(AcademicSession.objects.filter(pk=self.session.pk).exists())

    def test_delete_non_current_session(self):
        session2 = AcademicSession.objects.create(
            name="2084",
            start_date=date(2027, 4, 14),
            end_date=date(2028, 4, 13),
            is_current=False,
        )
        term2 = Term.objects.create(
            session=session2,
            name="Term 1",
            start_date=date(2027, 4, 15),
            end_date=date(2027, 8, 15),
            order=1,
        )
        # GET confirmation page
        resp_get = self.client_staff.get(reverse('delete-session', kwargs={'pk': session2.pk}))
        self.assertEqual(resp_get.status_code, 200)
        content = resp_get.content.decode()
        self.assertIn("Dates (AD)", content)
        self.assertIn("Dates (BS)", content)
        self.assertIn("1 terms", content)
        self.assertIn("All of its terms are deleted too.", content)

        # POST delete
        resp_post = self.client_staff.post(reverse('delete-session', kwargs={'pk': session2.pk}), follow=True)
        self.assertEqual(resp_post.status_code, 200)
        self.assertRedirects(resp_post, reverse('dashboard-sessions'))
        self.assertFalse(AcademicSession.objects.filter(pk=session2.pk).exists())
        self.assertFalse(Term.objects.filter(pk=term2.pk).exists())
        self.assertContains(resp_post, "was deleted.")

    # --- 7. Header chip, overview card, active sidebar link ---
    def test_header_chip_and_overview_with_current_session(self):
        resp = self.client_staff.get(reverse('dashboard'))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()
        # Header chip
        self.assertIn("Academic year 2083", content)
        self.assertIn(reverse('dashboard-sessions'), content)
        # Overview card
        self.assertIn("Current academic year", content)
        self.assertIn("2083", content)
        self.assertIn("days left in the year", content)

    def test_header_chip_and_overview_without_current_session(self):
        AcademicSession.objects.all().delete()
        cache.clear()

        resp = self.client_staff.get(reverse('dashboard'))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()
        # Header chip amber
        self.assertIn("No current academic year", content)
        self.assertIn("Set one", content)
        # Overview card empty
        self.assertIn("Set up academic year", content)

    def test_sidebar_active_link(self):
        for url_name in ['dashboard-sessions', 'add-session']:
            resp = self.client_staff.get(reverse(url_name))
            content = resp.content.decode()
            self.assertIn('Academic Years', content)
            self.assertIn('class="active"', content)

    # --- 8. HTML Cleanliness Check ---
    def test_html_cleanliness(self):
        pages_to_check = [
            reverse('dashboard-sessions'),
            reverse('add-session'),
            reverse('edit-session', kwargs={'pk': self.session.pk}),
        ]
        forbidden_chars = ['🗓', '📅', '✓']
        for url in pages_to_check:
            resp = self.client_staff.get(url)
            self.assertEqual(resp.status_code, 200)
            content = resp.content.decode()
            self.assertNotIn('style="', content, f"Inline style found in {url}")
            self.assertNotIn('<script', content, f"Script tag found in {url}")
            for char in forbidden_chars:
                self.assertNotIn(char, content, f"Forbidden char {char} found in {url}")
