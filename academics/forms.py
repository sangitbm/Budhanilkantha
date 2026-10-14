from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.db.models import F
from .models import AcademicSession, Term
from .services import find_overlapping_session


class AcademicSessionForm(forms.ModelForm):
    make_current = forms.BooleanField(
        required=False,
        label="Make this the current academic year"
    )

    class Meta:
        model = AcademicSession
        fields = ['name', 'start_date', 'end_date']
        labels = {
            'name': 'Year name',
            'start_date': 'Start date',
            'end_date': 'End date',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2083'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.is_current:
                self.fields['make_current'].initial = True
                self.fields['make_current'].disabled = True
            else:
                self.fields['make_current'].initial = False
        else:
            self.fields['make_current'].initial = False

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date <= start_date:
                self.add_error('end_date', 'End date must be after start date.')
            else:
                exclude_pk = self.instance.pk if self.instance and self.instance.pk else None
                overlapping = find_overlapping_session(start_date, end_date, exclude_pk=exclude_pk)
                if overlapping:
                    raise ValidationError(f"Session dates overlap with an existing academic year: {overlapping.name}.")

        return cleaned_data


class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ['name', 'start_date', 'end_date', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. First Terminal'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control acd-order-input', 'min': 1}),
        }

    def validate_unique(self):
        # Cross-row uniqueness for ('session', 'order') and ('session', 'name')
        # is validated across the whole formset in BaseTermFormSet.clean() to allow
        # order swaps and replacements in a single save.
        pass

    def validate_constraints(self):
        # UniqueConstraints are checked by BaseTermFormSet.clean() across all
        # rows, not per-form against the current DB state (which would block
        # order swaps before the +1000 shift in save()).
        pass

    def has_changed(self):
        if not self.instance.pk and self.data:
            name = (self.data.get(f'{self.prefix}-name') or '').strip()
            start = (self.data.get(f'{self.prefix}-start_date') or '').strip()
            end = (self.data.get(f'{self.prefix}-end_date') or '').strip()
            order = (self.data.get(f'{self.prefix}-order') or '').strip()
            if not any([name, start, end, order]):
                return False
        return super().has_changed()


class BaseTermFormSet(BaseInlineFormSet):
    def validate_unique(self):
        # Uniqueness of name and order within the formset is validated in clean()
        pass

    def clean(self):
        super().clean()
        session_start = None
        session_end = None
        if hasattr(self, 'session_form') and self.session_form and self.session_form.is_valid():
            session_start = self.session_form.cleaned_data.get('start_date')
            session_end = self.session_form.cleaned_data.get('end_date')
        elif self.instance and self.instance.pk:
            session_start = self.instance.start_date
            session_end = self.instance.end_date

        active_forms = []
        orders_seen = set()
        names_seen = set()

        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            if not form.has_changed() and not form.instance.pk:
                continue

            name = form.cleaned_data.get('name')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            order = form.cleaned_data.get('order')

            if not (name or start_date or end_date or order is not None):
                continue

            if not (name and start_date and end_date and order is not None):
                continue

            if end_date <= start_date:
                form.add_error('end_date', 'Term end date must be after start date.')

            if session_start and session_end:
                if start_date < session_start or end_date > session_end:
                    form.add_error('start_date', 'Term dates must lie inside the academic year.')

            name_lower = name.strip().lower()
            if name_lower in names_seen:
                form.add_error('name', f'Term with name "{name}" is duplicated.')
            else:
                names_seen.add(name_lower)

            if order in orders_seen:
                form.add_error('order', f'Term order {order} is duplicated.')
            else:
                orders_seen.add(order)

            active_forms.append((form, start_date, end_date))

        # Check overlapping terms
        for i in range(len(active_forms)):
            form_i, start_i, end_i = active_forms[i]
            for j in range(i + 1, len(active_forms)):
                form_j, start_j, end_j = active_forms[j]
                if start_i <= end_j and end_i >= start_j:
                    form_j.add_error('start_date', 'Term dates overlap with another term.')
                    if 'start_date' not in form_i.errors:
                        form_i.add_error('start_date', 'Term dates overlap with another term.')

        # Check collision with existing terms in database not in this formset
        if self.instance and self.instance.pk:
            deleted_pks = {f.instance.pk for f in self.forms if f.instance and f.instance.pk and self.can_delete and self._should_delete_form(f)}
            kept_pks = {f.instance.pk for f in self.forms if f.instance and f.instance.pk and f.instance.pk not in deleted_pks}
            other_terms = self.instance.terms.exclude(pk__in=kept_pks | deleted_pks)
            other_orders = set(other_terms.values_list('order', flat=True))
            for form in self.forms:
                if self.can_delete and self._should_delete_form(form):
                    continue
                ord_val = form.cleaned_data.get('order') if form.cleaned_data else None
                if ord_val is not None and ord_val in other_orders:
                    form.add_error('order', f"Term order {ord_val} is already used by another term.")

    def save(self, commit=True):
        if not commit:
            return super().save(commit=False)

        with transaction.atomic():
            # 1. Process deletions
            if self.can_delete:
                for form in self.forms:
                    if self._should_delete_form(form) and form.instance.pk:
                        form.instance.delete()

            # 2. Shift order of all existing terms of that session by +1000
            if self.instance and self.instance.pk:
                self.instance.terms.all().update(order=F('order') + 1000)

            # 3. Write final values for every kept term (including unchanged ones)
            saved_instances = []
            for form in self.forms:
                if self.can_delete and self._should_delete_form(form):
                    continue
                if not form.has_changed() and not form.instance.pk:
                    continue
                if not form.cleaned_data or not form.cleaned_data.get('name'):
                    continue

                term = form.save(commit=False)
                term.session = self.instance
                term.order = form.cleaned_data['order']
                try:
                    term.save()
                except IntegrityError:
                    form.add_error('order', f"Term order {term.order} is already used by another term.")
                    raise
                saved_instances.append(term)

            return saved_instances


def make_term_formset(extra=0):
    return inlineformset_factory(
        AcademicSession,
        Term,
        form=TermForm,
        formset=BaseTermFormSet,
        extra=extra,
        can_delete=True,
        max_num=8,
    )


TermFormSet = make_term_formset(extra=0)
