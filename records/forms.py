from django import forms
from .models import Student, Staff

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'gender', 'photo',
            'grade', 'roll_number', 'date_of_birth',
            'guardian_name', 'contact_number', 'address'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'ef-input', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'ef-input', 'placeholder': 'Last Name'}),
            'gender': forms.Select(attrs={'class': 'ef-input'}),
            'photo': forms.FileInput(attrs={'class': 'ef-file-input', 'accept': 'image/*'}),
            'grade': forms.Select(attrs={'class': 'ef-input'}),
            'roll_number': forms.TextInput(attrs={'class': 'ef-input', 'placeholder': 'e.g. 2024-042'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'ef-input'}),
            'guardian_name': forms.TextInput(attrs={'class': 'ef-input', 'placeholder': "Parent or Guardian Full Name"}),
            'contact_number': forms.TextInput(attrs={'class': 'ef-input', 'placeholder': '+977 98XXXXXXXX'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'ef-input ef-textarea-compact', 'placeholder': 'Permanent / Residential address'}),
        }

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'staff_type', 'designation', 'department', 'email', 'contact_number', 'date_of_joining', 'is_active', 'show_contact_publicly']
        widgets = {
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
        }
