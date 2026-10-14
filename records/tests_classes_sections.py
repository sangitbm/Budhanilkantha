from datetime import date
import csv
from io import StringIO
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from academics.models import SchoolClass, Section
from records.models import Student
from records.forms import StudentForm

User = get_user_model()


class SchoolClassAndSectionModelTests(TestCase):
    def setUp(self):
        SchoolClass.objects.all().delete()

    def test_school_class_creation_and_unique_name(self):
        c1 = SchoolClass.objects.create(name="Class 1", level="primary", order=50)
        self.assertEqual(str(c1), "Class 1")

        with self.assertRaises(Exception):
            SchoolClass.objects.create(name="Class 1", level="primary", order=55)

    def test_next_class_cannot_point_to_itself(self):
        c1 = SchoolClass.objects.create(name="Class 1", level="primary", order=50)
        c1.next_class = c1
        with self.assertRaises(ValidationError) as ctx:
            c1.clean()
        self.assertIn('next_class', ctx.exception.message_dict)

    def test_next_class_cannot_loop(self):
        c1 = SchoolClass.objects.create(name="Class 1", level="primary", order=50)
        c2 = SchoolClass.objects.create(name="Class 2", level="primary", order=60)
        c3 = SchoolClass.objects.create(name="Class 3", level="primary", order=70)

        c1.next_class = c2
        c1.save()
        c2.next_class = c3
        c2.save()
        c3.next_class = c1  # loop: 1 -> 2 -> 3 -> 1

        with self.assertRaises(ValidationError) as ctx:
            c3.clean()
        self.assertIn('next_class', ctx.exception.message_dict)

    def test_section_unique_per_class(self):
        c1 = SchoolClass.objects.create(name="Class 1", level="primary", order=50)
        c2 = SchoolClass.objects.create(name="Class 2", level="primary", order=60)

        s1 = Section.objects.create(school_class=c1, name="A")
        self.assertEqual(str(s1), "Class 1 - A")

        # Same section name in different class is allowed
        s2 = Section.objects.create(school_class=c2, name="A")
        self.assertEqual(str(s2), "Class 2 - A")

        # Same section name in same class raises error
        with self.assertRaises(Exception):
            Section.objects.create(school_class=c1, name="A")

    def test_student_clean_rejects_section_of_another_class(self):
        c1 = SchoolClass.objects.create(name="Class 1", level="primary", order=50)
        c2 = SchoolClass.objects.create(name="Class 2", level="primary", order=60)
        s2 = Section.objects.create(school_class=c2, name="B")

        student = Student(
            first_name="Hari",
            last_name="Bahadur",
            school_class=c1,
            section=s2,
            roll_number="101",
            date_of_birth=date(2012, 1, 1),
            guardian_name="Ram",
            contact_number="9841000000",
            address="Kathmandu",
        )
        with self.assertRaises(ValidationError) as ctx:
            student.clean()
        self.assertIn('section', ctx.exception.message_dict)
        self.assertEqual(ctx.exception.message_dict['section'][0], "This section belongs to Class 2.")

    def test_student_save_syncs_grade(self):
        c10 = SchoolClass.objects.create(name="Class 10 (SEE)", level="secondary", order=140)
        student = Student.objects.create(
            first_name="Gita",
            last_name="Kumari",
            school_class=c10,
            roll_number="102",
            date_of_birth=date(2010, 2, 2),
            guardian_name="Sita",
            contact_number="9841000001",
            address="Kathmandu",
        )
        self.assertEqual(student.grade, "Class 10 (SEE)")


class StudentFormTests(TestCase):
    def setUp(self):
        SchoolClass.objects.all().delete()
        self.c1 = SchoolClass.objects.create(name="Class 1", level="primary", order=50, is_active=True)
        self.c2 = SchoolClass.objects.create(name="Class 2", level="primary", order=60, is_active=True)
        self.c_inactive = SchoolClass.objects.create(name="Old Class", level="other", order=200, is_active=False)

        self.s1_a = Section.objects.create(school_class=self.c1, name="A", is_active=True)
        self.s2_a = Section.objects.create(school_class=self.c2, name="A", is_active=True)

    def test_form_lists_active_classes_and_shows_grouped_sections(self):
        form = StudentForm()
        class_choices = [c[1] for c in form.fields['school_class'].choices]
        self.assertIn("Class 1", class_choices)
        self.assertIn("Class 2", class_choices)
        self.assertNotIn("Old Class", class_choices)

        # Check section grouped options rendered
        html = form.as_p()
        self.assertIn('<optgroup label="Class 1">', html)
        self.assertIn('<optgroup label="Class 2">', html)

    def test_form_keeps_inactive_current_class_selectable_on_edit(self):
        student = Student.objects.create(
            first_name="Inactive",
            last_name="ClassUser",
            school_class=self.c_inactive,
            roll_number="999",
            date_of_birth=date(2010, 1, 1),
            guardian_name="Parent",
            contact_number="9800000000",
            address="Kathmandu",
        )
        form = StudentForm(instance=student)
        class_choices = [c[1] for c in form.fields['school_class'].choices]
        self.assertIn("Old Class", class_choices)

    def test_form_accepts_matching_section_and_rejects_mismatch(self):
        data = {
            'first_name': 'Kiran',
            'last_name': 'KC',
            'gender': 'Male',
            'school_class': str(self.c1.pk),
            'section': str(self.s1_a.pk),
            'roll_number': '103',
            'date_of_birth': '2012-05-05',
            'guardian_name': 'Madan',
            'contact_number': '9841222222',
            'address': 'Kathmandu',
        }
        form = StudentForm(data=data)
        self.assertTrue(form.is_valid())

        # Mismatch section
        data['section'] = str(self.s2_a.pk)
        form_mismatch = StudentForm(data=data)
        self.assertFalse(form_mismatch.is_valid())
        self.assertIn('section', form_mismatch.errors)
        self.assertEqual(form_mismatch.errors['section'][0], "This section belongs to Class 2.")


class StudentDashboardViewsTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username='staff_records',
            password='password123',
            is_staff=True
        )
        self.client.login(username='staff_records', password='password123')
        SchoolClass.objects.all().delete()

        self.c1 = SchoolClass.objects.create(name="Class 1", level="primary", order=50, is_active=True)
        self.c10 = SchoolClass.objects.create(name="Class 10 (SEE)", level="secondary", order=140, is_active=True)
        self.sec1_a = Section.objects.create(school_class=self.c1, name="A")
        self.sec1_b = Section.objects.create(school_class=self.c1, name="B")

        self.st1 = Student.objects.create(
            first_name="Aarav",
            last_name="Shrestha",
            school_class=self.c1,
            section=self.sec1_a,
            roll_number="1",
            date_of_birth=date(2015, 1, 1),
            guardian_name="Guardian 1",
            contact_number="9800000001",
            address="Kathmandu",
        )
        self.st2 = Student.objects.create(
            first_name="Bibek",
            last_name="Thapa",
            school_class=self.c1,
            section=self.sec1_b,
            roll_number="2",
            date_of_birth=date(2015, 1, 2),
            guardian_name="Guardian 2",
            contact_number="9800000002",
            address="Kathmandu",
        )
        self.st3 = Student.objects.create(
            first_name="Chandra",
            last_name="Adhikari",
            school_class=self.c10,
            section=None,
            roll_number="3",
            date_of_birth=date(2009, 1, 3),
            guardian_name="Guardian 3",
            contact_number="9800000003",
            address="Kathmandu",
        )

    def test_student_list_ordering_and_class_column(self):
        resp = self.client.get(reverse('dashboard-students'))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()

        # Class column shows "<class name> - <section>" or just class
        self.assertIn("Class 1 - A", content)
        self.assertIn("Class 1 - B", content)
        self.assertIn("Class 10 (SEE)", content)

        students = list(resp.context['students'])
        self.assertEqual(students[0], self.st1)
        self.assertEqual(students[1], self.st2)
        self.assertEqual(students[2], self.st3)

    def test_student_list_class_and_section_filters(self):
        # Filter by class 1
        resp = self.client.get(reverse('dashboard-students'), {'class': str(self.c1.pk)})
        self.assertEqual(len(resp.context['students']), 2)

        # Filter by class 1 and section A
        resp = self.client.get(reverse('dashboard-students'), {'class': str(self.c1.pk), 'section': str(self.sec1_a.pk)})
        self.assertEqual(len(resp.context['students']), 1)
        self.assertEqual(resp.context['students'][0], self.st1)

        # Invalid class filter is ignored
        resp_inv = self.client.get(reverse('dashboard-students'), {'class': 'invalid-id'})
        self.assertEqual(len(resp_inv.context['students']), 3)

    def test_student_csv_export_columns_and_filters(self):
        resp = self.client.get(reverse('students-export'), {'class': str(self.c1.pk), 'section': str(self.sec1_a.pk)})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'text/csv')

        reader = csv.reader(StringIO(resp.content.decode('utf-8')))
        rows = list(reader)

        self.assertEqual(rows[0], ['Roll no', 'First name', 'Last name', 'Gender', 'Class', 'Section', 'Guardian', 'Contact'])
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1][4], "Class 1")
        self.assertEqual(rows[1][5], "A")
        # Ensure no date of birth or address in export
        self.assertNotIn("2015", resp.content.decode('utf-8'))
        self.assertNotIn("Kathmandu", resp.content.decode('utf-8'))

    def test_student_delete_confirmation_details(self):
        resp = self.client.get(reverse('delete-student', kwargs={'pk': self.st1.pk}))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()
        self.assertIn("Class 1 - A", content)
        self.assertIn("Roll Number: 1", content)


class MigrationDataTests(TransactionTestCase):
    def test_data_migration_mapping_and_idempotency(self):
        executor = MigrationExecutor(connection)
        app = 'records'
        migrate_from = [(app, '0003_student_gender_student_photo_alter_student_grade'), ('academics', '0001_initial')]
        migrate_to = [(app, '0005_data_migrate_student_classes'), ('academics', '0002_schoolclass_section')]

        # Roll back to before the new migrations
        executor.migrate(migrate_from)
        executor.loader.build_graph()

        old_apps = executor.loader.project_state(migrate_from).apps
        OldStudent = old_apps.get_model('records', 'Student')

        # Create students with the test grades
        grades_to_test = [
            ('Class 3', '301'),
            ('Class 10', '302'),
            ('Class 11 Science', '303'),
            ('A-Level (AS)', '304'),
            ('Grade 1', '305'),
            ('Mystery Unknown', '306'),
        ]
        for grade_val, roll in grades_to_test:
            OldStudent.objects.create(
                first_name=f"Student_{roll}",
                last_name="Test",
                grade=grade_val,
                roll_number=roll,
                date_of_birth=date(2010, 1, 1),
                guardian_name="Guardian",
                contact_number="9800000000",
                address="Address",
            )

        # Migrate forward
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()
        executor.migrate(migrate_to)

        new_apps = executor.loader.project_state(migrate_to).apps
        NewSchoolClass = new_apps.get_model('academics', 'SchoolClass')
        NewStudent = new_apps.get_model('records', 'Student')

        # Assert default classes exist
        self.assertTrue(NewSchoolClass.objects.filter(name="ECD").exists())
        self.assertTrue(NewSchoolClass.objects.filter(name="Class 1").exists())
        self.assertTrue(NewSchoolClass.objects.filter(name="Class 10 (SEE)").exists())
        self.assertTrue(NewSchoolClass.objects.filter(name="Class 11 - Science").exists())
        self.assertTrue(NewSchoolClass.objects.filter(name="Cambridge A-Level (AS)").exists())

        # Assert each student mapped properly
        s301 = NewStudent.objects.get(roll_number='301')
        self.assertEqual(s301.school_class.name, 'Class 3')
        self.assertEqual(s301.grade, 'Class 3')

        s302 = NewStudent.objects.get(roll_number='302')
        self.assertEqual(s302.school_class.name, 'Class 10 (SEE)')
        self.assertEqual(s302.grade, 'Class 10 (SEE)')

        s303 = NewStudent.objects.get(roll_number='303')
        self.assertEqual(s303.school_class.name, 'Class 11 - Science')
        self.assertEqual(s303.grade, 'Class 11 - Science')

        s304 = NewStudent.objects.get(roll_number='304')
        self.assertEqual(s304.school_class.name, 'Cambridge A-Level (AS)')
        self.assertEqual(s304.grade, 'Cambridge A-Level (AS)')
        # Classes used by students must end up is_active=True
        self.assertTrue(s304.school_class.is_active)

        s305 = NewStudent.objects.get(roll_number='305')
        self.assertEqual(s305.school_class.name, 'Class 1')
        self.assertEqual(s305.grade, 'Class 1')

        s306 = NewStudent.objects.get(roll_number='306')
        self.assertEqual(s306.school_class.name, 'Unmapped: Mystery Unknown')
        self.assertEqual(s306.grade, 'Unmapped: Mystery Unknown')
        self.assertFalse(s306.school_class.is_active)

        # Running the data migration function twice creates no duplicates
        import importlib
        migrate_mod = importlib.import_module("records.migrations.0005_data_migrate_student_classes")
        migrate_students_to_classes = migrate_mod.migrate_students_to_classes
        class_count_before = NewSchoolClass.objects.count()
        migrate_students_to_classes(new_apps, None)
        class_count_after = NewSchoolClass.objects.count()
        self.assertEqual(class_count_before, class_count_after)
