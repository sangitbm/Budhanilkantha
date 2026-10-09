import re

file_path = r'c:\Users\sangi\Desktop\budhanilkantha_school\core\views.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_snippet = """    if active_tab and active_tab.startswith('tab_'):
            active_tab = active_tab[4:]
        if active_tab not in ALLOWED_TABS:
        active_tab = 'school'"""

good_snippet = """    if active_tab and active_tab.startswith('tab_'):
        active_tab = active_tab[4:]
    if active_tab not in ALLOWED_TABS:
        active_tab = 'school'"""

content = content.replace(bad_snippet, good_snippet)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Indentation fixed.")
