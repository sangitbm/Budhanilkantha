from django.db import migrations


def migrate_students_to_classes(apps, schema_editor):
    SchoolClass = apps.get_model('academics', 'SchoolClass')
    Student = apps.get_model('records', 'Student')

    DEFAULT_CLASSES = [
        ('ECD', 'early', '', 10, True, 'Class 1'),
        ('Nursery', 'early', '', 20, False, 'LKG'),
        ('LKG', 'early', '', 30, False, 'UKG'),
        ('UKG', 'early', '', 40, False, 'Class 1'),
        ('Class 1', 'primary', '', 50, True, 'Class 2'),
        ('Class 2', 'primary', '', 60, True, 'Class 3'),
        ('Class 3', 'primary', '', 70, True, 'Class 4'),
        ('Class 4', 'primary', '', 80, True, 'Class 5'),
        ('Class 5', 'primary', '', 90, True, 'Class 6'),
        ('Class 6', 'lower_secondary', '', 100, True, 'Class 7'),
        ('Class 7', 'lower_secondary', '', 110, True, 'Class 8'),
        ('Class 8', 'lower_secondary', '', 120, True, 'Class 9'),
        ('Class 9', 'secondary', '', 130, True, 'Class 10 (SEE)'),
        ('Class 10 (SEE)', 'secondary', '', 140, True, None),
        ('Class 11 - Science', 'higher_secondary', 'Science', 150, True, 'Class 12 - Science'),
        ('Class 11 - Management', 'higher_secondary', 'Management', 150, True, 'Class 12 - Management'),
        ('Class 11 - Humanities', 'higher_secondary', 'Humanities', 150, True, 'Class 12 - Humanities'),
        ('Class 12 - Science', 'higher_secondary', 'Science', 160, True, None),
        ('Class 12 - Management', 'higher_secondary', 'Management', 160, True, None),
        ('Class 12 - Humanities', 'higher_secondary', 'Humanities', 160, True, None),
        ('Cambridge A-Level (AS)', 'other', '', 170, False, 'Cambridge A-Level (A2)'),
        ('Cambridge A-Level (A2)', 'other', '', 180, False, None),
    ]

    classes_by_name = {}
    for name, level, stream, order, is_active, _ in DEFAULT_CLASSES:
        cls_obj, _ = SchoolClass.objects.get_or_create(
            name=name,
            defaults={
                'level': level,
                'stream': stream,
                'order': order,
                'is_active': is_active,
            }
        )
        classes_by_name[name] = cls_obj

    for name, _, _, _, _, next_name in DEFAULT_CLASSES:
        if next_name:
            cls_obj = classes_by_name.get(name) or SchoolClass.objects.get(name=name)
            if not cls_obj.next_class_id:
                next_obj = classes_by_name.get(next_name) or SchoolClass.objects.get(name=next_name)
                cls_obj.next_class = next_obj
                cls_obj.save(update_fields=['next_class'])

    GRADE_MAP = {
        'Class 1': 'Class 1',
        'Class 2': 'Class 2',
        'Class 3': 'Class 3',
        'Class 4': 'Class 4',
        'Class 5': 'Class 5',
        'Class 6': 'Class 6',
        'Class 7': 'Class 7',
        'Class 8': 'Class 8',
        'Class 9': 'Class 9',
        'Class 10': 'Class 10 (SEE)',
        'Class 11 Science': 'Class 11 - Science',
        'Class 11 Management': 'Class 11 - Management',
        'Class 11 Humanities': 'Class 11 - Humanities',
        'Class 12 Science': 'Class 12 - Science',
        'Class 12 Management': 'Class 12 - Management',
        'Class 12 Humanities': 'Class 12 - Humanities',
        'A-Level (AS)': 'Cambridge A-Level (AS)',
        'A-Level (A2)': 'Cambridge A-Level (A2)',
        'Grade 1': 'Class 1',
    }

    for student in Student.objects.all():
        old_grade = student.grade.strip() if student.grade else ""
        if not old_grade:
            continue

        if old_grade in GRADE_MAP:
            target_class_name = GRADE_MAP[old_grade]
            cls_obj = SchoolClass.objects.get(name=target_class_name)
            if not cls_obj.is_active:
                cls_obj.is_active = True
                cls_obj.save(update_fields=['is_active'])
            student.school_class = cls_obj
            student.grade = cls_obj.name
            student.save(update_fields=['school_class', 'grade'])
        elif old_grade in classes_by_name or SchoolClass.objects.filter(name=old_grade).exists():
            existing = classes_by_name.get(old_grade) or SchoolClass.objects.get(name=old_grade)
            if not existing.is_active and not existing.name.startswith("Unmapped: "):
                existing.is_active = True
                existing.save(update_fields=['is_active'])
            student.school_class = existing
            student.grade = existing.name
            student.save(update_fields=['school_class', 'grade'])
        else:
            unmapped_name = f"Unmapped: {old_grade}"
            unmapped_cls, _ = SchoolClass.objects.get_or_create(
                name=unmapped_name,
                defaults={
                    'level': 'other',
                    'stream': '',
                    'order': 999,
                    'is_active': False,
                }
            )
            student.school_class = unmapped_cls
            student.grade = unmapped_cls.name
            student.save(update_fields=['school_class', 'grade'])


def backwards_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0002_schoolclass_section'),
        ('records', '0004_student_school_class_student_section_and_more'),
    ]

    operations = [
        migrations.RunPython(migrate_students_to_classes, backwards_func),
    ]
