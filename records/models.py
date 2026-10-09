from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    grade = models.CharField(max_length=50, help_text="e.g. Class 10, Class 12 Science")
    roll_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    guardian_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    address = models.TextField()
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.roll_number}"

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
