import re

file_path = r'c:\Users\sangi\Desktop\budhanilkantha_school\core\forms.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r"'program_1_title',\s*'program_1_desc',", "", content)
content = re.sub(r"'program_2_title',\s*'program_2_desc',", "", content)
content = re.sub(r"'program_1_title':.*?,\s*", "", content)
content = re.sub(r"'program_1_desc':.*?,\s*", "", content)
content = re.sub(r"'program_2_title':.*?,\s*", "", content)
content = re.sub(r"'program_2_desc':.*?,\s*", "", content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("forms.py updated.")
