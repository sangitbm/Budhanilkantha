import re
with open('core/templates/core/dashboard_settings.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'tab-pane' in line or 'tab_' in line:
        print(f"Line {i+1}: {line.strip()}")
