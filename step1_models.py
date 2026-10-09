import re

file_path = r'c:\Users\sangi\Desktop\budhanilkantha_school\core\models.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add open_grades
content = re.sub(
    r"(admissions_open = models\.BooleanField\(default=False\))",
    r"\1\n    open_grades = models.JSONField(default=list, blank=True, help_text=\"List of grades open for admission\")",
    content
)

# Remove program_X fields
programs_section_pattern = r'    # --- Programs Section ---.*?program_2_desc = models\.TextField\(blank=True, default=".*?"\)'
content = re.sub(programs_section_pattern, '    # --- Programs Section ---\n    # (Migrated to AcademicProgram model)', content, flags=re.DOTALL)

# Add AcademicProgram
academic_program_model = """
class AcademicProgram(models.Model):
    site_settings = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='academic_programs')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
"""
content = content + "\n" + academic_program_model

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("models.py updated.")
