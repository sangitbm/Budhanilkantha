import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import SiteSettings, AcademicProgram

settings = SiteSettings.get_settings()
if AcademicProgram.objects.filter(site_settings=settings).count() == 0:
    AcademicProgram.objects.create(
        site_settings=settings,
        title="Day Shift (ECD - Grade 10)",
        description="Strong foundation for future success. We provide a robust curriculum, co-curricular activities, and essential skill development.",
        order=0
    )
    AcademicProgram.objects.create(
        site_settings=settings,
        title="Morning Shift (Grades 11-12)",
        description="Preparing students for higher education. Offering +2 programs with expert faculty to prepare students for their careers.",
        order=1
    )
    print("Seeded AcademicPrograms.")
else:
    print("AcademicPrograms already exist.")
