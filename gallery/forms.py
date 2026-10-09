from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'ef-input', 'placeholder': 'e.g. Annual Sports Meet (or auto-named from file)'})
    )

    class Meta:
        model = Photo
        fields = ['image', 'title', 'description', 'date_taken', 'is_featured']
        widgets = {
            'image': forms.FileInput(attrs={'id': 'id_image', 'accept': 'image/*', 'class': 'ef-file-input'}),
            'description': forms.Textarea(attrs={'class': 'ef-input ef-textarea-compact', 'rows': 2, 'placeholder': 'Brief caption or context for this photo (optional)...'}),
            'date_taken': forms.DateInput(attrs={'type': 'date', 'class': 'ef-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'ef-checkbox', 'id': 'id_is_featured'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        image = cleaned_data.get('image')
        if not title:
            if image and hasattr(image, 'name'):
                cleaned_data['title'] = image.name.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ').title()
            else:
                cleaned_data['title'] = 'Gallery Photo'
        return cleaned_data