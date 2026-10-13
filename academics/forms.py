from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import AcademicSession, Term


class AcademicSessionForm(forms.ModelForm):
    make_current = forms.BooleanField(
        required=False,
        label="Make this the current academic year"
    )

    class Meta:
        model = AcademicSession
        fields = ['name', 'start_date', 'end_date']
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
                overlapping = AcademicSession.objects.filter(
                    start_date__lte=end_date,
                    end_date__gte=start_date
                )
                if self.instance and self.instance.pk:
                    overlapping = overlapping.exclude(pk=self.instance.pk)
                if overlapping.exists():
                    overlap_name = overlapping.first().name
                    raise ValidationError(f"Session dates overlap with an existing academic year: {overlap_name}.")

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk and 'order' not in self.initial:
            self.fields['order'].initial = None


class BaseTermFormSet(BaseInlineFormSet):
    def validate_unique(self):
        # Uniqueness of name and order per session is validated in clean() to attach errors to fields
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


TermFormSet = inlineformset_factory(
    AcademicSession,
    Term,
    form=TermForm,
    formset=BaseTermFormSet,
    extra=0,
    can_delete=True,
    max_num=8,
)
