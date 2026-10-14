from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from records.models import Student
from academics.models import SchoolClass
from datetime import date
import csv
from io import StringIO

class StudentDashboardTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staff', password='pwd', is_staff=True)
        self.normal_user = User.objects.create_user(username='norm', password='pwd')
        self.class1, _ = SchoolClass.objects.get_or_create(name="Class 1", defaults={"level": "primary", "order": 50})
        self.class2, _ = SchoolClass.objects.get_or_create(name="Class 2", defaults={"level": "primary", "order": 60})
        self.class10, _ = SchoolClass.objects.get_or_create(name="Class 10 (SEE)", defaults={"level": "secondary", "order": 140})
        
    def test_access_permissions(self):
        url = reverse('dashboard-students')
        
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        
        self.client.login(username='norm', password='pwd')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)
        
        self.client.login(username='staff', password='pwd')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        url_csv = reverse('students-export')
        self.client.logout()
        resp_csv = self.client.get(url_csv)
        self.assertEqual(resp_csv.status_code, 302)
        self.client.login(username='staff', password='pwd')
        resp_csv = self.client.get(url_csv)
        self.assertEqual(resp_csv.status_code, 200)

    def test_ordering(self):
        Student.objects.create(first_name="Z", last_name="A", roll_number="1", school_class=self.class2, date_of_birth=date(2010, 1, 1))
        Student.objects.create(first_name="A", last_name="B", roll_number="2", school_class=self.class10, date_of_birth=date(2010, 1, 1))
        Student.objects.create(first_name="M", last_name="C", roll_number="3", school_class=self.class1, date_of_birth=date(2010, 1, 1))
        
        self.client.login(username='staff', password='pwd')
        resp = self.client.get(reverse('dashboard-students'))
        
        students = list(resp.context['students'])
        self.assertEqual(students[0].school_class, self.class1)
        self.assertEqual(students[1].school_class, self.class2)
        self.assertEqual(students[2].school_class, self.class10)

    def test_search_and_filter(self):
        Student.objects.create(first_name="Ram", last_name="Thapa", roll_number="100", guardian_name="Hari", contact_number="123", school_class=self.class1, date_of_birth=date(2010, 1, 1))
        Student.objects.create(first_name="Sita", last_name="Sharma", roll_number="200", guardian_name="Gita", contact_number="999", school_class=self.class2, date_of_birth=date(2010, 1, 1))
        
        self.client.login(username='staff', password='pwd')
        url = reverse('dashboard-students')
        
        resp = self.client.get(url, {'q': 'ram thapa'})
        self.assertContains(resp, "Ram")
        self.assertNotContains(resp, "Sita")
        
        resp = self.client.get(url, {'q': '999'})
        self.assertContains(resp, "Sita")
        self.assertNotContains(resp, "Ram")
        
        resp = self.client.get(url, {'class': str(self.class1.pk)})
        self.assertContains(resp, "Ram")
        self.assertNotContains(resp, "Sita")
        
        resp = self.client.get(url, {'class': 'Invalid'})
        self.assertEqual(len(resp.context['students']), 2)

    def test_pagination(self):
        for i in range(26):
            Student.objects.create(first_name=f"F{i}", last_name="L", roll_number=str(i), school_class=self.class1, date_of_birth=date(2010, 1, 1))
            
        self.client.login(username='staff', password='pwd')
        url = reverse('dashboard-students')
        
        resp = self.client.get(url)
        self.assertEqual(len(resp.context['students']), 25)
        
        resp2 = self.client.get(url, {'page': '2'})
        self.assertEqual(len(resp2.context['students']), 1)

    def test_empty_state_and_no_sensitive_data(self):
        self.client.login(username='staff', password='pwd')
        url = reverse('dashboard-students')
        
        resp = self.client.get(url)
        self.assertContains(resp, "No students yet")
        self.assertContains(resp, "Add your first student")
        self.assertNotContains(resp, "<table")
        
        Student.objects.create(first_name="Secret", last_name="Student", roll_number="1", school_class=self.class1, date_of_birth=date(2005, 5, 5), address="123 Hidden St")
        resp2 = self.client.get(url)
        self.assertNotContains(resp2, "2005")
        self.assertNotContains(resp2, "Hidden St")

    def test_no_inline_styles_or_emojis(self):
        Student.objects.create(first_name="Style", last_name="Test", roll_number="1", school_class=self.class1, date_of_birth=date(2010, 1, 1))
        self.client.login(username='staff', password='pwd')
        resp = self.client.get(reverse('dashboard-students'))
        content = resp.content.decode('utf-8')
        
        main_content = content.split('<main class="main-content">')[1]
        self.assertNotIn('style="', main_content)
        self.assertNotIn("📁", main_content)
        self.assertNotIn("🎓", main_content)

    def test_csv_export(self):
        Student.objects.create(first_name="=Attack", last_name="Name", roll_number="100", guardian_name="Guard", contact_number="123", school_class=self.class1, date_of_birth=date(2010, 1, 1))
        
        self.client.login(username='staff', password='pwd')
        resp = self.client.get(reverse('students-export'))
        self.assertEqual(resp['Content-Type'], 'text/csv')
        
        content = resp.content.decode('utf-8')
        reader = csv.reader(StringIO(content))
        rows = list(reader)
        
        self.assertEqual(rows[0], ['Roll no', 'First name', 'Last name', 'Gender', 'Class', 'Section', 'Guardian', 'Contact'])
        self.assertEqual(rows[1][1], "'=Attack")
        self.assertEqual(rows[1][4], "Class 1")
        self.assertEqual(rows[1][5], "")
        self.assertNotIn("2010", content)
