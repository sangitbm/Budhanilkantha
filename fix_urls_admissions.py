import re

file_path = r'c:\Users\sangi\Desktop\budhanilkantha_school\core\urls.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("name='admission'", "name='admissions'")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("urls fixed admissions.")
