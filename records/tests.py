from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Student

User = get_user_model()

class StudentFormAndModelTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username='stafftest',
            password='password123',
            is_staff=True
        )
        self.client.login(username='stafftest', password='password123')

    def test_student_model_creation_with_gender_and_photo(self):
        test_image = SimpleUploadedFile("avatar.jpg", b"\x47\x49\x46\x38\x39\x61", content_type="image/jpeg")
        student = Student.objects.create(
            first_name="Aarav",
            last_name="Shrestha",
            gender="Male",
            grade="Class 10",
            roll_number="2026-001",
            date_of_birth="2010-05-15",
            guardian_name="Ramesh Shrestha",
            contact_number="9841234567",
            address="Budhanilkantha-3, Kathmandu",
            photo=test_image
        )
        self.assertEqual(student.gender, "Male")
        self.assertEqual(student.grade, "Class 10")
        self.assertTrue(bool(student.photo))
        self.assertIn("Aarav Shrestha", str(student))

    def test_student_create_view_get(self):
        url = reverse('add-student')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Complete Enrollment")
        self.assertContains(response, "Upload Photo")
        self.assertContains(response, "Male")
        self.assertContains(response, "Female")

    def test_student_create_view_post_success(self):
        url = reverse('add-student')
        post_data = {
            'first_name': 'Prashant',
            'last_name': 'Sharma',
            'gender': 'Male',
            'grade': 'Class 11 Science',
            'roll_number': '2026-002',
            'date_of_birth': '2008-01-10',
            'guardian_name': 'Bikash Sharma',
            'contact_number': '9800000000',
            'address': 'Chapali, Kathmandu',
        }
        response = self.client.post(url, post_data)
        self.assertRedirects(response, reverse('dashboard-students'))
        self.assertTrue(Student.objects.filter(roll_number='2026-002').exists())
