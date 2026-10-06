from django import forms
from .models import Student, Staff

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'grade', 'roll_number', 'date_of_birth', 'guardian_name', 'contact_number', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'staff_type', 'designation', 'department', 'email', 'contact_number', 'date_of_joining', 'is_active']
        widgets = {
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
        }
