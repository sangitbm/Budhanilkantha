with open('static/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re

# Update .st-image-field
css = re.sub(r'\.st-image-field\s*\{[^}]*\}', 
'''.st-image-field {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 16px;
}''', css)

# Update .st-img-preview
css = re.sub(r'\.st-img-preview\s*\{[^}]*\}', 
'''.st-img-preview {
  width: 80px;
  height: 80px;
  background: var(--light-bg);
  border: 1px solid var(--gray-light);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  overflow: hidden;
  flex-shrink: 0;
}''', css)

# Update .st-img-filename
css = re.sub(r'\.st-img-filename\s*\{[^}]*\}', 
'''.st-img-filename {
  font-size: 0.85rem;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 280px;
}''', css)

# Update .st-file-input max width
css = re.sub(r'\.st-file-input\s*\{[^}]*\}', 
'''.st-file-input {
  font-size: 0.9rem;
  color: var(--text-dark);
  max-width: 280px;
}''', css)

# Update .st-img-clear
css = re.sub(r'\.st-img-clear\s*\{[^}]*\}', 
'''.st-img-clear {
  font-size: 0.85rem;
  font-weight: normal;
  color: #B91C1C;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}
.st-clear-checkbox {
  width: 16px;
  height: 16px;
  margin: 0;
}''', css)

# Update .st-hero-card
css = re.sub(r'\.st-hero-card\s*\{[^}]*\}', 
'''.st-hero-card {
  position: relative;
  width: 96px;
  height: 96px;
  border-radius: 10px;
  overflow: visible;
  border: 1px solid var(--gray-light);
}
.st-hero-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
}''', css)

# Update .st-hero-remove
css = re.sub(r'\.st-hero-remove\s*\{[^}]*\}', 
'''.st-hero-remove {
  position: absolute;
  top: -6px;
  right: -6px;
  background: #DC2626;
  color: white;
  border: 2px solid white;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  padding: 0;
  display: grid;
  place-items: center;
  line-height: 1;
  cursor: pointer;
}''', css)

# Add <600px media query
if '@media (max-width: 600px) {' not in css or '.st-image-field {' not in css.split('@media (max-width: 600px) {')[-1]:
    css += '''
@media (max-width: 600px) {
  .st-image-field {
    flex-direction: column;
  }
}
'''

with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print('Updated CSS rules')
