from django.db import models
from django.core.exceptions import ValidationError


class Student(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    photo = models.ImageField(upload_to='students/', blank=True, null=True)
    school_class = models.ForeignKey(
        'academics.SchoolClass',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='students',
    )
    section = models.ForeignKey(
        'academics.Section',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='students',
    )
    # Derived legacy field; Phase 2 removes this field.
    grade = models.CharField(max_length=60, blank=True, editable=False)
    roll_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    guardian_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    address = models.TextField()
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.roll_number}"

    def clean(self):
        super().clean()
        if self.section_id:
            if not self.school_class_id or self.section.school_class_id != self.school_class_id:
                raise ValidationError({'section': f"This section belongs to {self.section.school_class.name}."})

    def save(self, *args, **kwargs):
        if self.school_class:
            self.grade = self.school_class.name
        super().save(*args, **kwargs)


class Staff(models.Model):
    STAFF_TYPES = (
        ('TEACHER', 'Teacher'),
        ('SUPPORT', 'Support Staff'),
        ('ADMIN', 'Administration'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    staff_type = models.CharField(max_length=20, choices=STAFF_TYPES, default='TEACHER')
    designation = models.CharField(max_length=100, help_text="e.g. Math Teacher, Head of Science, Accountant")
    department = models.CharField(max_length=100, help_text="e.g. Science, Administration, IT")
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    date_of_joining = models.DateField()
    is_active = models.BooleanField(default=True)
    show_contact_publicly = models.BooleanField(default=False, help_text="Show phone number and email on the public staff directory")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.designation})"
