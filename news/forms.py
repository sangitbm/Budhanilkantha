from django import forms
from .models import Notice, Event

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'description', 'file_attachment', 'show_in_ticker']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', 'start_time', 'end_time', 'location', 'file_attachment']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'ef-input', 'placeholder': 'e.g., Annual Science Fair & STEM Expo'}),
            'description': forms.Textarea(attrs={'class': 'ef-input ef-textarea', 'rows': 4, 'placeholder': 'Provide event overview, requirements, agenda highlights, and contact information...'}),
            'event_date': forms.DateInput(attrs={'type': 'date', 'class': 'ef-input'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'ef-input'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'ef-input'}),
            'location': forms.TextInput(attrs={'class': 'ef-input', 'placeholder': 'e.g. Main Auditorium / Sports Ground'}),
        }
