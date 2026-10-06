from django import forms

from .models import AdmissionInquiry, SiteSettings

class AdmissionForm(forms.ModelForm):
    class Meta:
        model = AdmissionInquiry
        fields = ['student_name', 'parent_name', 'email', 'phone_number', 'grade_applying_for']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student Full Name'}),
            'parent_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parent Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'grade_applying_for': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Grade 11'}),
        }


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            # School Info
            'school_name', 'school_short_name', 'marquee_text', 'tagline',
            'established_year', 'principal_name', 'principal_photo', 'principal_message',
            'about_short', 'logo', 'favicon',
            # About Section
            'about_image', 'about_text', 'curriculum_text',
            'value_1', 'value_2', 'value_3',
            'stat_students', 'stat_faculty', 'stat_support',
            # Programs Section
            'program_1_title', 'program_1_desc',
            'program_2_title', 'program_2_desc',
            # Contact
            'phone_primary', 'phone_secondary',
            'email_general', 'email_admissions',
            'address', 'google_maps_url', 'office_hours',
            # Social Media
            'facebook_url', 'youtube_url', 'twitter_url', 'instagram_url', 'whatsapp_url',
            # Admissions
            'admissions_open', 'admissions_btn_label', 'admissions_btn_link',
            'admissions_badge', 'admissions_start', 'admissions_end', 'admissions_message',
            # SEO & Advanced
            'meta_description', 'og_title', 'og_image', 'maintenance_mode'
        ]
        widgets = {
            'school_name': forms.TextInput(attrs={'placeholder': 'Budhanilkantha Secondary School'}),
            'school_short_name': forms.TextInput(attrs={'placeholder': 'BSS'}),
            'tagline': forms.TextInput(attrs={'placeholder': 'Excellence in Education'}),
            'established_year': forms.TextInput(attrs={'placeholder': '1990'}),
            'principal_name': forms.TextInput(attrs={'placeholder': 'Mr. Ram Sharma'}),
            'about_short': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Short description about the school...'}),
            'phone_primary': forms.TextInput(attrs={'placeholder': '+977-1-4371637'}),
            'phone_secondary': forms.TextInput(attrs={'placeholder': '+977-1-XXXXXXX (optional)'}),
            'email_general': forms.EmailInput(attrs={'placeholder': 'info@bnks.edu.np'}),
            'email_admissions': forms.EmailInput(attrs={'placeholder': 'admissions@bnks.edu.np (optional)'}),
            'address': forms.TextInput(attrs={'placeholder': 'Narayanthan, Kathmandu, Nepal'}),
            'google_maps_url': forms.URLInput(attrs={'placeholder': 'https://maps.google.com/...'}),
            'facebook_url': forms.URLInput(attrs={'placeholder': 'https://facebook.com/yourpage'}),
            'youtube_url': forms.URLInput(attrs={'placeholder': 'https://youtube.com/yourchannel'}),
            'twitter_url': forms.URLInput(attrs={'placeholder': 'https://twitter.com/yourhandle'}),
            'instagram_url': forms.URLInput(attrs={'placeholder': 'https://instagram.com/yourprofile'}),
            'admissions_message': forms.TextInput(attrs={'placeholder': 'Admissions Open for 2026-27'}),
            'meta_description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Brief description for search engines (max 160 characters)...'}),
            'meta_keywords': forms.TextInput(attrs={'placeholder': 'school, nepal, education, kathmandu'}),
        }