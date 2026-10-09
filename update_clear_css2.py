with open('static/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re

# Remove old .st-clear-row and its input rule
css = re.sub(r'\.st-clear-row\s*\{[^}]*\}', '', css)
css = re.sub(r'\.st-clear-row input\[type=checkbox\]\s*\{[^}]*\}', '', css)

# The updated CSS to append
new_css = '''
.st-clear-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 8px 0 0;
  padding: 0;
  line-height: 1.2;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  color: #B91C1C;
}
.st-clear-row input[type="checkbox"] {
  width: 16px;
  height: 16px;
  margin: 0;
  padding: 0;
  min-height: 0;
  flex: none;
}
.st-clear-row span {
  display: inline;
  margin: 0;
  padding: 0;
}
'''

css += new_css

with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print('Updated CSS')
