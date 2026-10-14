from itertools import groupby
from django import forms
from django.forms.models import ModelChoiceIterator
from django.db.models import Q
from academics.models import SchoolClass, Section
from .models import Student, Staff


class GroupedSectionModelChoiceIterator(ModelChoiceIterator):
    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        queryset = self.queryset.select_related('school_class').order_by(
            'school_class__order', 'school_class__name', 'name'
        )
        for school_class_name, sections in groupby(queryset, key=lambda s: s.school_class.name):
            yield (school_class_name, [(s.pk, s.name) for s in sections])


class GroupedSectionChoiceField(forms.ModelChoiceField):
    iterator = GroupedSectionModelChoiceIterator


class StudentForm(forms.ModelForm):
    school_class = forms.ModelChoiceField(
        queryset=SchoolClass.objects.none(),
        required=True,
        widget=forms.Select(attrs={'class': 'ef-input'}),
        label="Class",
        empty_label="Select Class",
    )
    section = GroupedSectionChoiceField(
        queryset=Section.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'ef-input'}),
        label="Section",
        empty_label="Select Section (optional)",
    )

    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'gender', 'photo',
            'school_class', 'section', 'roll_number', 'date_of_birth',
            'guardian_name', 'contact_number', 'address'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'ef-input', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'ef-input', 'placeholder': 'Last Name'}),
            'gender': forms.Select(attrs={'class': 'ef-input'}),
            'photo': forms.FileInput(attrs={'class': 'ef-file-input', 'accept': 'image/*'}),
            'roll_number': forms.TextInput(attrs={'class': 'ef-input', 'placeholder': 'e.g. 2024-042'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'ef-input'}),
            'guardian_name': forms.TextInput(attrs={'class': 'ef-input', 'placeholder': "Parent or Guardian Full Name"}),
            'contact_number': forms.TextInput(attrs={'class': 'ef-input', 'placeholder': '+977 98XXXXXXXX'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'ef-input ef-textarea-compact', 'placeholder': 'Permanent / Residential address'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_qs = SchoolClass.objects.filter(is_active=True).order_by('order', 'name')
        if self.instance and self.instance.pk and self.instance.school_class_id:
            if not self.instance.school_class.is_active:
                class_qs = SchoolClass.objects.filter(
                    Q(is_active=True) | Q(pk=self.instance.school_class_id)
                ).order_by('order', 'name')
        self.fields['school_class'].queryset = class_qs

        section_qs = Section.objects.filter(is_active=True).select_related('school_class').order_by(
            'school_class__order', 'school_class__name', 'name'
        )
        if self.instance and self.instance.pk and self.instance.section_id:
            if not self.instance.section.is_active:
                section_qs = Section.objects.filter(
                    Q(is_active=True) | Q(pk=self.instance.section_id)
                ).select_related('school_class').order_by(
                    'school_class__order', 'school_class__name', 'name'
                )
        self.fields['section'].queryset = section_qs

    def clean(self):
        cleaned_data = super().clean()
        school_class = cleaned_data.get('school_class')
        section = cleaned_data.get('section')
        if section and school_class:
            if section.school_class_id != school_class.pk:
                self.add_error('section', f"This section belongs to {section.school_class.name}.")
        return cleaned_data


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'staff_type', 'designation', 'department', 'email', 'contact_number', 'date_of_joining', 'is_active', 'show_contact_publicly']
        widgets = {
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
        }
