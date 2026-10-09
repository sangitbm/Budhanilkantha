with open('static/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re

# Remove old .st-img-clear
css = re.sub(r'\.st-img-clear\s*\{[^}]*\}', '', css)
css = re.sub(r'\.st-img-clear:hover\s*\{[^}]*\}', '', css)
# Remove old .st-clear-checkbox
css = re.sub(r'\.st-clear-checkbox\s*\{[^}]*\}', '', css)

# The updated CSS to append
new_css = '''
.st-clear-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  color: #B91C1C;
}
.st-clear-row input[type=checkbox] {
  width: 16px;
  height: 16px;
  margin: 0;
  flex: none;
}
'''

css += new_css

with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print('Updated CSS')
