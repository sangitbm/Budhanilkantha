import re

file_path = r'c:\Users\sangi\Desktop\budhanilkantha_school\core\views.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "from django.urls import reverse_lazy",
    "from django.urls import reverse_lazy, reverse"
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("reverse imported.")
