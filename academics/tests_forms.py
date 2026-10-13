from datetime import date
from django.test import TestCase
from academics.models import AcademicSession
from academics.forms import AcademicSessionForm, TermFormSet


class AcademicFormsTests(TestCase):
    def setUp(self):
        self.session = AcademicSession.objects.create(
            name="2083",
            start_date=date(2026, 4, 14),
            end_date=date(2027, 4, 13),
            is_current=True,
        )

    def test_session_form_valid(self):
        form = AcademicSessionForm(data={
            'name': '2084',
            'start_date': '2027-04-14',
            'end_date': '2028-04-13',
            'make_current': False,
        })
        self.assertTrue(form.is_valid())

    def test_session_form_end_before_start(self):
        form = AcademicSessionForm(data={
            'name': '2085',
            'start_date': '2028-04-14',
            'end_date': '2028-04-10',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('end_date', form.errors)
        self.assertIn('End date must be after start date.', form.errors['end_date'])

    def test_session_form_overlap(self):
        # Overlaps with 2083
        form = AcademicSessionForm(data={
            'name': '2083-Overlap',
            'start_date': '2026-10-01',
            'end_date': '2027-10-01',
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(any('overlap' in str(e).lower() for e in form.non_field_errors()))

    def test_session_form_edit_same_session_no_self_overlap(self):
        form = AcademicSessionForm(instance=self.session, data={
            'name': '2083-Updated',
            'start_date': '2026-04-14',
            'end_date': '2027-04-13',
        })
        self.assertTrue(form.is_valid())

    def test_session_form_current_session_disabled_checkbox(self):
        form = AcademicSessionForm(instance=self.session)
        self.assertTrue(form.fields['make_current'].disabled)
        self.assertTrue(form.fields['make_current'].initial)

    def test_term_formset_outside_session_dates(self):
        session_form = AcademicSessionForm(data={
            'name': '2085',
            'start_date': '2028-04-14',
            'end_date': '2029-04-13',
        })
        self.assertTrue(session_form.is_valid())

        data = {
            'terms-TOTAL_FORMS': '1',
            'terms-INITIAL_FORMS': '0',
            'terms-MIN_NUM_FORMS': '0',
            'terms-MAX_NUM_FORMS': '8',
            'terms-0-name': 'Out of Bounds Term',
            'terms-0-start_date': '2028-01-01',  # Before session start
            'terms-0-end_date': '2028-06-01',
            'terms-0-order': '1',
        }
        formset = TermFormSet(data=data, prefix='terms')
        formset.session_form = session_form
        self.assertFalse(formset.is_valid())
        self.assertIn('start_date', formset.forms[0].errors)

    def test_term_formset_duplicate_name(self):
        session_form = AcademicSessionForm(data={
            'name': '2085',
            'start_date': '2028-04-14',
            'end_date': '2029-04-13',
        })
        self.assertTrue(session_form.is_valid())

        data = {
            'terms-TOTAL_FORMS': '2',
            'terms-INITIAL_FORMS': '0',
            'terms-MIN_NUM_FORMS': '0',
            'terms-MAX_NUM_FORMS': '8',
            'terms-0-name': 'Term 1',
            'terms-0-start_date': '2028-04-15',
            'terms-0-end_date': '2028-08-15',
            'terms-0-order': '1',
            'terms-1-name': 'Term 1',  # Duplicate
            'terms-1-start_date': '2028-08-16',
            'terms-1-end_date': '2028-12-15',
            'terms-1-order': '2',
        }
        formset = TermFormSet(data=data, prefix='terms')
        formset.session_form = session_form
        self.assertFalse(formset.is_valid())
        self.assertIn('name', formset.forms[1].errors)

    def test_term_formset_duplicate_order(self):
        session_form = AcademicSessionForm(data={
            'name': '2085',
            'start_date': '2028-04-14',
            'end_date': '2029-04-13',
        })
        self.assertTrue(session_form.is_valid())

        data = {
            'terms-TOTAL_FORMS': '2',
            'terms-INITIAL_FORMS': '0',
            'terms-MIN_NUM_FORMS': '0',
            'terms-MAX_NUM_FORMS': '8',
            'terms-0-name': 'Term 1',
            'terms-0-start_date': '2028-04-15',
            'terms-0-end_date': '2028-08-15',
            'terms-0-order': '1',
            'terms-1-name': 'Term 2',
            'terms-1-start_date': '2028-08-16',
            'terms-1-end_date': '2028-12-15',
            'terms-1-order': '1',  # Duplicate order
        }
        formset = TermFormSet(data=data, prefix='terms')
        formset.session_form = session_form
        self.assertFalse(formset.is_valid())
        self.assertIn('order', formset.forms[1].errors)

    def test_term_formset_overlapping_terms(self):
        session_form = AcademicSessionForm(data={
            'name': '2085',
            'start_date': '2028-04-14',
            'end_date': '2029-04-13',
        })
        self.assertTrue(session_form.is_valid())

        data = {
            'terms-TOTAL_FORMS': '2',
            'terms-INITIAL_FORMS': '0',
            'terms-MIN_NUM_FORMS': '0',
            'terms-MAX_NUM_FORMS': '8',
            'terms-0-name': 'Term 1',
            'terms-0-start_date': '2028-04-15',
            'terms-0-end_date': '2028-08-15',
            'terms-0-order': '1',
            'terms-1-name': 'Term 2',
            'terms-1-start_date': '2028-08-01',  # Overlaps with Term 1
            'terms-1-end_date': '2028-12-15',
            'terms-1-order': '2',
        }
        formset = TermFormSet(data=data, prefix='terms')
        formset.session_form = session_form
        self.assertFalse(formset.is_valid())
        self.assertIn('start_date', formset.forms[1].errors)
