import re

file_path = r'c:\Users\sangi\Desktop\budhanilkantha_school\core\views.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("active_tab = request.POST.get('tab', active_tab)", "active_tab = request.POST.get('settings_tab', request.POST.get('tab', active_tab))")
# Strip out the "tab_" from settings_tab if it starts with it
content = content.replace("if active_tab not in ALLOWED_TABS:", "if active_tab and active_tab.startswith('tab_'):\n            active_tab = active_tab[4:]\n        if active_tab not in ALLOWED_TABS:")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("views patched for tab state.")
