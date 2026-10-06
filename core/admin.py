from django.contrib import admin
from .models import AdmissionInquiry, SiteSettings

@admin.register(AdmissionInquiry)
class AdmissionInquiryAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'grade_applying_for', 'phone_number', 'submitted_at')
    search_fields = ('student_name', 'parent_name')
    ordering = ('-submitted_at',)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Prevents creating more than one settings row."""
    def has_add_permission(self, request):
        # If a settings object already exists, disable the Add button
        return not SiteSettings.objects.exists()
