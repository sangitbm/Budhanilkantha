import re

file_path = r'c:\Users\sangi\Desktop\budhanilkantha_school\core\views.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "from .models import AdmissionInquiry, SiteSettings, HeroImage",
    "from .models import AdmissionInquiry, SiteSettings, HeroImage, AcademicProgram"
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Import fixed.")
