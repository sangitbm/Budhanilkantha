with open('static/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re

# Remove old .st-hero-card
css = re.sub(r'\.st-hero-card\s*\{[^}]*\}\s*\.st-hero-card\simg\s*\{[^}]*\}', '', css)
# Remove old .st-hero-remove
css = re.sub(r'\.st-hero-remove\s*\{[^}]*\}\s*\.st-hero-remove:hover\s*\{[^}]*\}', '', css)
# Remove old .st-hero-grid
css = re.sub(r'\.st-hero-grid\s*\{[^}]*\}', '', css)

# The updated CSS to append
new_css = '''
.st-hero-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
  margin-top: 8px;
}
.st-hero-thumb {
  position: relative;
  width: 112px;
  height: 72px;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
}
.st-hero-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.st-hero-grid .st-hero-remove {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 24px;
  height: 24px;
  min-width: 0;
  min-height: 0;
  padding: 0;
  margin: 0;
  box-sizing: border-box;
  border: 2px solid #fff;
  border-radius: 50%;
  display: grid;
  place-items: center;
  line-height: 1;
  cursor: pointer;
  background: rgba(15, 23, 42, 0.75);
  color: white;
}
.st-hero-grid .st-hero-remove:hover,
.st-hero-grid .st-hero-remove:focus-visible {
  background: #dc2626;
  outline: 2px solid #dc2626;
  outline-offset: 2px;
}
@media (max-width: 600px) {
  .st-hero-grid .st-hero-remove {
    width: 32px;
    height: 32px;
  }
}
'''

css += new_css

with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print('Updated CSS')
