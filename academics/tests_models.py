from datetime import date
from django.test import TestCase
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import AcademicSession, Term

User = get_user_model()


class AcademicModelTests(TestCase):
    def setUp(self):
        self.session1 = AcademicSession.objects.create(
            name="2083",
            start_date=date(2026, 4, 14),
            end_date=date(2027, 4, 13),
            is_current=True,
        )

    def test_two_current_sessions_rejected_by_db(self):
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                AcademicSession.objects.create(
                    name="2084",
                    start_date=date(2027, 4, 14),
                    end_date=date(2028, 4, 13),
                    is_current=True,
                )

    def test_session_end_before_start_rejected_by_db(self):
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                AcademicSession.objects.create(
                    name="2085",
                    start_date=date(2028, 4, 14),
                    end_date=date(2027, 4, 14),
                    is_current=False,
                )

    def test_overlapping_session_fails_clean(self):
        overlap = AcademicSession(
            name="2083-Overlap",
            start_date=date(2026, 10, 1),
            end_date=date(2027, 10, 1),
            is_current=False,
        )
        with self.assertRaises(ValidationError):
            overlap.clean()

        # Clean on valid non-overlapping session passes
        non_overlap = AcademicSession(
            name="2084",
            start_date=date(2027, 4, 14),
            end_date=date(2028, 4, 13),
            is_current=False,
        )
        non_overlap.clean()

        # Clean on self passes
        self.session1.clean()

    def test_term_outside_session_dates_fails_clean(self):
        term = Term(
            session=self.session1,
            name="First Term",
            start_date=date(2026, 1, 1),  # Before session start
            end_date=date(2026, 6, 1),
            order=1,
        )
        with self.assertRaises(ValidationError):
            term.clean()

        term_after = Term(
            session=self.session1,
            name="Late Term",
            start_date=date(2027, 1, 1),
            end_date=date(2027, 5, 1),  # After session end
            order=2,
        )
        with self.assertRaises(ValidationError):
            term_after.clean()

    def test_duplicate_term_order_or_name_rejected_by_db(self):
        Term.objects.create(
            session=self.session1,
            name="First Term",
            start_date=date(2026, 4, 15),
            end_date=date(2026, 7, 15),
            order=1,
        )

        # Duplicate name
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Term.objects.create(
                    session=self.session1,
                    name="First Term",
                    start_date=date(2026, 7, 16),
                    end_date=date(2026, 10, 15),
                    order=2,
                )

        # Duplicate order
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Term.objects.create(
                    session=self.session1,
                    name="Second Term",
                    start_date=date(2026, 7, 16),
                    end_date=date(2026, 10, 15),
                    order=1,
                )

    def test_term_end_before_start_rejected_by_db(self):
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Term.objects.create(
                    session=self.session1,
                    name="Bad Term",
                    start_date=date(2026, 7, 15),
                    end_date=date(2026, 6, 15),
                    order=5,
                )

    def test_admin_change_list_loads_for_superuser(self):
        User.objects.create_superuser(
            username='adminuser',
            password='Password123!',
            email='admin@example.com'
        )
        self.client.login(username='adminuser', password='Password123!')
        url = reverse('admin:academics_academicsession_changelist')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "2083")
