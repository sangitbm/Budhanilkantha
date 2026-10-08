from django.db import models

class AdmissionInquiry(models.Model):
    student_name = models.CharField(max_length=100)
    parent_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    grade_applying_for = models.CharField(max_length=20)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - Grade {self.grade_applying_for}"


class SiteSettings(models.Model):
    """
    Singleton model - only ONE row should ever exist in this table.
    It stores all the configurable settings for the school website.
    """

    # --- School Info ---
    school_name = models.CharField(max_length=200, default='Budhanilkantha Secondary School')
    school_short_name = models.CharField(max_length=20, default='BSS', help_text="Short name shown in navbar, e.g. BSS")
    marquee_text = models.CharField(max_length=500, blank=True, help_text="Scrolling announcement text above the navbar. Leave blank to hide.")
    ticker_enabled = models.BooleanField(default=True)
    tagline = models.CharField(max_length=255, default='Excellence in Education', help_text="Shown in the hero section and footer")
    established_year = models.CharField(max_length=10, default='1990', help_text="Year the school was established")
    principal_name = models.CharField(max_length=100, blank=True, help_text="Name of the current principal")
    principal_photo = models.ImageField(upload_to='site/', blank=True, null=True, help_text="Photo of the principal")
    principal_message = models.TextField(blank=True, help_text="Short welcoming message from the principal")
    about_short = models.TextField(blank=True, help_text="Short description used in About section and meta tags")
    logo = models.ImageField(upload_to='site/', blank=True, null=True, help_text="School logo (optional). Shown in navbar.")
    favicon = models.ImageField(upload_to='site/', blank=True, null=True, help_text="Site favicon (.ico or .png)")

    # --- About Section (Homepage) ---
    about_image = models.ImageField(upload_to='site/', blank=True, null=True, help_text="Image for the About Us section on the homepage")
    about_text = models.TextField(blank=True, default="Budhanilkantha Secondary School has been a beacon of academic excellence, committed to developing the next generation of leaders. Our holistic approach to education ensures that students grow intellectually, socially, and emotionally.", help_text="First paragraph of the About section")
    curriculum_text = models.TextField(blank=True, default="We offer a comprehensive curriculum that blends rigorous academics with diverse extracurricular activities, preparing students for success in a rapidly changing world.", help_text="Second paragraph of the About section")
    
    value_1 = models.CharField(max_length=50, default="Academic Excellence")
    value_2 = models.CharField(max_length=50, default="Discipline & Values")
    value_3 = models.CharField(max_length=50, default="Community Spirit")
    
    stat_students = models.CharField(max_length=20, default="1000+", help_text="e.g. 1000+")
    stat_faculty = models.CharField(max_length=20, default="50+", help_text="e.g. 50+")
    stat_support = models.CharField(max_length=20, default="20+", help_text="e.g. 20+")

    # --- Programs Section ---
    # (Migrated to AcademicProgram model)

    # --- Contact Info ---
    phone_primary = models.CharField(max_length=20, default='+977-1-4371637', help_text="Main phone number shown in header and footer")
    phone_secondary = models.CharField(max_length=20, blank=True, help_text="Secondary phone number (optional)")
    email_general = models.EmailField(default='info@bnks.edu.np', help_text="General contact email")
    email_admissions = models.EmailField(blank=True, help_text="Admissions-specific email (optional)")
    address = models.CharField(max_length=255, default='Narayanthan, Kathmandu, Nepal')
    google_maps_url = models.URLField(blank=True, help_text="Paste your Google Maps embed or share link here")
    office_hours = models.CharField(max_length=100, blank=True, help_text="e.g. Sun-Fri, 9AM - 5PM")

    # --- Information Officer ---
    info_officer_name = models.CharField(max_length=200, blank=True)
    info_officer_title = models.CharField(max_length=200, blank=True, default='Information Officer')
    info_officer_phone = models.CharField(max_length=50, blank=True)
    info_officer_email = models.EmailField(blank=True)

    # --- Social Media ---
    facebook_url = models.URLField(blank=True, help_text="Full Facebook page URL")
    youtube_url = models.URLField(blank=True, help_text="Full YouTube channel URL")
    twitter_url = models.URLField(blank=True, help_text="Full Twitter/X profile URL")
    instagram_url = models.URLField(blank=True, help_text="Full Instagram profile URL")
    whatsapp_url = models.CharField(max_length=20, blank=True, help_text="WhatsApp number (e.g. +977...)")

    # --- Admissions ---
    admissions_open = models.BooleanField(default=True, help_text="Toggle admissions banner visibility on the homepage")
    admissions_btn_label = models.CharField(max_length=50, default='Apply Now', blank=True)
    admissions_btn_link = models.CharField(max_length=200, default='/admissions', blank=True)
    admissions_badge = models.CharField(max_length=100, blank=True, help_text="Banner badge text above hero")
    admissions_start = models.DateField(blank=True, null=True)
    admissions_end = models.DateField(blank=True, null=True)
    
    # Old field kept for backward compatibility if needed, or removed if safe. I'll keep it to prevent data loss.
    admissions_message = models.CharField(max_length=255, blank=True, default='Admissions Open for 2026-27')

    # --- SEO ---
    meta_description = models.TextField(max_length=160, blank=True, help_text="Used by Google for search result description.")
    og_title = models.CharField(max_length=200, blank=True, help_text="Open Graph Title for social media sharing")
    og_image = models.ImageField(upload_to='site/', blank=True, null=True, help_text="1200x630 image for social sharing")

    # --- Advanced ---
    maintenance_mode = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Site Settings'

    @classmethod
    def get_settings(cls):
        """Always returns the single settings object, creating it if it doesn't exist."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
        
    @property
    def is_admission_active(self):
        from django.utils import timezone
        if not self.admissions_open:
            return False
        today = timezone.now().date()
        if self.admissions_start and today < self.admissions_start:
            return False
        if self.admissions_end and today > self.admissions_end:
            return False
        return True

class HeroImage(models.Model):
    site_settings = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='hero_images')
    image = models.ImageField(upload_to='site/hero/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Hero Image {self.id}"


class AcademicProgram(models.Model):
    site_settings = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='academic_programs')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

from django.core.exceptions import ValidationError

def validate_image_size(image):
    file_size = image.file.size
    limit_mb = 2
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(f"Max size of file is {limit_mb} MB")

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="e.g. Student (Grade 10)")
    quote = models.TextField(help_text="Max 300 characters")
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True, validators=[validate_image_size])
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def clean(self):
        super().clean()
        if self.quote and len(self.quote) > 300:
            raise ValidationError({'quote': 'Quote cannot exceed 300 characters.'})

    def __str__(self):
        return f"{self.name} - {self.role}"
