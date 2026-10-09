from django.core.management.base import BaseCommand
from core.models import SiteSettings, AcademicProgram

class Command(BaseCommand):
    help = 'Seeds initial AcademicProgram data if none exists.'

    def handle(self, *args, **options):
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
            self.stdout.write(self.style.SUCCESS("Seeded AcademicPrograms."))
        else:
            self.stdout.write(self.style.WARNING("AcademicPrograms already exist."))
