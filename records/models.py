from django.db import models

class Student(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    GRADE_CHOICES = (
        ('Class 1', 'Class 1'),
        ('Class 2', 'Class 2'),
        ('Class 3', 'Class 3'),
        ('Class 4', 'Class 4'),
        ('Class 5', 'Class 5'),
        ('Class 6', 'Class 6'),
        ('Class 7', 'Class 7'),
        ('Class 8', 'Class 8'),
        ('Class 9', 'Class 9'),
        ('Class 10', 'Class 10 (SEE)'),
        ('Class 11 Science', 'Class 11 - Science'),
        ('Class 11 Management', 'Class 11 - Management'),
        ('Class 11 Humanities', 'Class 11 - Humanities'),
        ('Class 12 Science', 'Class 12 - Science'),
        ('Class 12 Management', 'Class 12 - Management'),
        ('Class 12 Humanities', 'Class 12 - Humanities'),
        ('A-Level (AS)', 'Cambridge A-Level (AS)'),
        ('A-Level (A2)', 'Cambridge A-Level (A2)'),
        ('Grade 1', 'Grade 1'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    photo = models.ImageField(upload_to='students/', blank=True, null=True)
    grade = models.CharField(max_length=50, choices=GRADE_CHOICES, help_text="Select student grade/class")
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
