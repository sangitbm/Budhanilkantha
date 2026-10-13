from datetime import date, timedelta
from unittest.mock import patch
from django.test import TestCase, RequestFactory
from django.core.cache import cache
import nepali_datetime

from core.templatetags.ui import bs_date
from .models import AcademicSession, Term
from .services import (
    set_current_session,
    next_session_name,
    duplicate_session,
    default_session_dates,
    get_current_session,
)
from .context_processors import current_session


class AcademicServicesTests(TestCase):
    def setUp(self):
        cache.clear()
        self.session = AcademicSession.objects.create(
            name="2083",
            start_date=date(2026, 4, 14),
            end_date=date(2027, 4, 13),
            is_current=True,
        )
        self.term1 = Term.objects.create(
            session=self.session,
            name="First Term",
            start_date=date(2026, 4, 15),
            end_date=date(2026, 8, 15),
            order=1,
        )
        self.term2 = Term.objects.create(
            session=self.session,
            name="Second Term",
            start_date=date(2026, 8, 16),
            end_date=date(2026, 12, 15),
            order=2,
        )

    def tearDown(self):
        cache.clear()

    def test_set_current_session(self):
        session2 = AcademicSession.objects.create(
            name="2084",
            start_date=date(2027, 4, 14),
            end_date=date(2028, 4, 13),
            is_current=False,
        )
        set_current_session(session2)

        self.session.refresh_from_db()
        session2.refresh_from_db()
        self.assertFalse(self.session.is_current)
        self.assertTrue(session2.is_current)
        self.assertEqual(AcademicSession.objects.filter(is_current=True).count(), 1)

        # Setting the same session again preserves single current session
        set_current_session(session2)
        self.assertEqual(AcademicSession.objects.filter(is_current=True).count(), 1)

    def test_next_session_name(self):
        self.assertEqual(next_session_name("2083"), "2084")
        self.assertEqual(next_session_name("2083/84"), "2084/85")
        self.assertEqual(next_session_name("Spring"), "Spring (copy)")

        # Uniqueness suffix
        AcademicSession.objects.create(
            name="2084",
            start_date=date(2027, 4, 14),
            end_date=date(2028, 4, 13),
            is_current=False,
        )
        self.assertEqual(next_session_name("2083"), "2084 (2)")

        AcademicSession.objects.create(
            name="2084 (2)",
            start_date=date(2028, 4, 14),
            end_date=date(2029, 4, 13),
            is_current=False,
        )
        self.assertEqual(next_session_name("2083"), "2084 (3)")

        AcademicSession.objects.create(
            name="Spring (copy)",
            start_date=date(2029, 4, 14),
            end_date=date(2030, 4, 13),
            is_current=False,
        )
        self.assertEqual(next_session_name("Spring"), "Spring (copy) (2)")

    def test_duplicate_session_and_fallback(self):
        copy = duplicate_session(self.session)
        self.assertEqual(copy.name, "2084")
        self.assertFalse(copy.is_current)

        # BS month and day match, BS year is one higher
        bs_old = nepali_datetime.date.from_datetime_date(self.session.start_date)
        bs_new = nepali_datetime.date.from_datetime_date(copy.start_date)
        self.assertEqual(bs_new.year, bs_old.year + 1)
        self.assertEqual(bs_new.month, bs_old.month)
        self.assertEqual(bs_new.day, bs_old.day)

        delta = copy.start_date - self.session.start_date
        self.assertEqual(copy.end_date, self.session.end_date + delta)

        # Terms copied with same names, orders, and shifted dates
        self.assertEqual(copy.terms.count(), 2)
        for orig_t, copy_t in zip(self.session.terms.order_by('order'), copy.terms.order_by('order')):
            self.assertEqual(copy_t.name, orig_t.name)
            self.assertEqual(copy_t.order, orig_t.order)
            self.assertEqual(copy_t.start_date, orig_t.start_date + delta)
            self.assertEqual(copy_t.end_date, orig_t.end_date + delta)

        # Original remains unchanged
        self.session.refresh_from_db()
        self.assertTrue(self.session.is_current)
        self.assertEqual(self.session.name, "2083")

        # 365-day fallback test
        copy.delete()
        with patch('nepali_datetime.date.from_datetime_date', side_effect=ValueError('BS failed')):
            fallback_copy = duplicate_session(self.session)
            self.assertEqual(fallback_copy.name, "2084")
            self.assertEqual(fallback_copy.start_date, self.session.start_date + timedelta(days=365))
            self.assertEqual(fallback_copy.end_date, self.session.end_date + timedelta(days=365))

    def test_duplicate_session_overlap_error(self):
        copy = duplicate_session(self.session)
        from .services import SessionOverlapError
        with self.assertRaises(SessionOverlapError) as cm:
            duplicate_session(self.session)
        self.assertIn(f"An academic year already covers these dates: {copy.name}.", str(cm.exception))
        # Ensure nothing extra was created
        self.assertEqual(AcademicSession.objects.count(), 2)

    def test_default_session_dates(self):
        name1, start1, end1 = default_session_dates(date(2026, 4, 14))
        self.assertEqual(name1, "2083")
        self.assertEqual(start1, date(2026, 4, 14))
        next_bs_start = nepali_datetime.date(2084, 1, 1).to_datetime_date()
        self.assertEqual(end1, next_bs_start - timedelta(days=1))

        name2, start2, end2 = default_session_dates(date(2026, 12, 1))
        self.assertEqual(name2, "2083")
        self.assertEqual(start2, date(2026, 4, 14))
        self.assertEqual(end2, next_bs_start - timedelta(days=1))

        # Fallback when BS conversion fails
        with patch('nepali_datetime.date.from_datetime_date', side_effect=ValueError('BS failed')):
            name_fb, start_fb, end_fb = default_session_dates(date(2026, 4, 14))
            self.assertEqual(name_fb, "2026")
            self.assertEqual(start_fb, date(2026, 1, 1))
            self.assertEqual(end_fb, date(2026, 12, 31))

    def test_bs_date_filter(self):
        self.assertEqual(bs_date(date(2026, 4, 14)), "2083 Baishakh 1")
        self.assertEqual(bs_date(date(2026, 4, 14), "iso"), "2083-01-01")
        self.assertEqual(bs_date(None), "")
        self.assertEqual(bs_date(date(1900, 1, 1)), "")
        self.assertEqual(bs_date("not-a-date"), "")

    def test_get_current_session_cache_and_signals(self):
        # With current session
        current = get_current_session()
        self.assertEqual(current, self.session)

        # Uses cache on second call (0 queries)
        with self.assertNumQueries(0):
            cached_session = get_current_session()
            self.assertEqual(cached_session, self.session)

        # Saving session clears cache
        self.session.name = "2083-Edited"
        self.session.save()
        self.assertIsNone(cache.get('current_session'))

        # Re-cache and delete clears cache
        get_current_session()
        self.assertIsNotNone(cache.get('current_session'))
        self.session.delete()
        self.assertIsNone(cache.get('current_session'))

        # No current session returns None and caches None (0 queries on second call)
        self.assertIsNone(get_current_session())
        with self.assertNumQueries(0):
            self.assertIsNone(get_current_session())

        # Creating/saving term also clears cache
        new_session = AcademicSession.objects.create(
            name="2085",
            start_date=date(2028, 4, 14),
            end_date=date(2029, 4, 13),
            is_current=True,
        )
        get_current_session()
        self.assertIsNotNone(cache.get('current_session'))
        Term.objects.create(
            session=new_session,
            name="Term X",
            start_date=date(2028, 4, 15),
            end_date=date(2028, 7, 15),
            order=1,
        )
        self.assertIsNone(cache.get('current_session'))

    def test_context_processor(self):
        request = RequestFactory().get('/')
        ctx = current_session(request)
        self.assertIn('current_session', ctx)
        self.assertEqual(ctx['current_session'], self.session)

    def test_suggest_terms(self):
        from .services import suggest_terms
        start = date(2026, 4, 14)
        end = date(2027, 4, 13)
        terms = suggest_terms(start, end)
        self.assertEqual(len(terms), 3)
        self.assertEqual(terms[0]['start_date'], start)
        self.assertEqual(terms[-1]['end_date'], end)
        # Check consecutive with no gaps or overlaps
        for i in range(len(terms) - 1):
            self.assertEqual(terms[i + 1]['start_date'], terms[i]['end_date'] + timedelta(days=1))
            self.assertLess(terms[i]['start_date'], terms[i]['end_date'])
        self.assertEqual([t['order'] for t in terms], [1, 2, 3])
        self.assertEqual([t['name'] for t in terms], ["First Terminal", "Second Terminal", "Final Terminal"])

    def test_get_current_term(self):
        from .services import get_current_term
        # Within term 1
        t1 = get_current_term(self.session, today=date(2026, 5, 1))
        self.assertEqual(t1, self.term1)

        # Within term 2
        t2 = get_current_term(self.session, today=date(2026, 9, 1))
        self.assertEqual(t2, self.term2)

        # Between or outside terms
        t_none = get_current_term(self.session, today=date(2027, 1, 1))
        self.assertIsNone(t_none)

        # No session
        self.assertIsNone(get_current_term(None))

    def test_days_left(self):
        from .services import days_left
        end = date(2026, 4, 20)
        self.assertEqual(days_left(end, today=date(2026, 4, 10)), 10)
        self.assertEqual(days_left(end, today=date(2026, 4, 20)), 0)
        self.assertEqual(days_left(end, today=date(2026, 4, 25)), 0)

