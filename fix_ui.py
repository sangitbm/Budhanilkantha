import re

with open('static/css/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. header style
text = text.replace('.site-header {\n  background: var(--white);\n  border-bottom: 1px solid var(--gray-light);\n  position: sticky;\n  top: 0;\n  z-index: 100;\n  padding: 14px 0;\n}', '.site-header {\n  background: var(--white);\n  border-bottom: 1px solid var(--gray-light);\n  position: sticky;\n  top: 0;\n  z-index: 100;\n  padding: 14px 0;\n}\n\n.hdr-no-padding {\n  padding: 0 !important;\n}')

# 2. navbar inner
text = text.replace('.navbar-inner {\n  padding: 22px 24px;\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  flex-wrap: nowrap;\n}', '.navbar-inner {\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  flex-wrap: nowrap;\n}\n\n.hdr-navbar {\n  padding: 16px 0;\n  min-height: 80px;\n}')
text = text.replace('.navbar-inner {\n  padding: 22px 24px;\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  flex-wrap: nowrap;\n}', '') # just in case

# 3. Logo
text = text.replace('.logo-text {\n  font-size: 1.3rem;\n  font-weight: 700;\n  color: var(--primary-dark);\n  line-height: 1.2;\n}', '.logo-text {\n  font-size: 1.35rem;\n  font-weight: 700;\n  color: var(--primary-dark);\n  line-height: 1.2;\n}')
text = text.replace('.logo-text small {\n  display: block;\n  font-weight: 500;\n  font-size: 0.7rem;\n  color: var(--text-muted);\n  letter-spacing: 0.04em;\n  max-width: 200px;\n  overflow: hidden;\n  text-overflow: ellipsis;\n}', '.logo-text small {\n  display: block;\n  font-weight: 500;\n  font-size: 0.75rem;\n  color: #5b6573;\n  letter-spacing: 0.04em;\n  max-width: 200px;\n  overflow: hidden;\n  text-overflow: ellipsis;\n}')
text = text.replace('.logo-img {\n  height: 54px;\n  width: 54px;\n  border-radius: 50%;\n  object-fit: cover;\n}', '.logo-img {\n  height: 56px;\n  width: 56px;\n  border-radius: 50%;\n  object-fit: cover;\n}')


# 4. Nav links margin auto
text = text.replace('.nav-links {\n  display: flex;\n  align-items: center;\n  gap: 4px;\n  flex-wrap: nowrap;\n  white-space: nowrap;\n}', '.nav-links {\n  display: flex;\n  align-items: center;\n  gap: 4px;\n  flex-wrap: nowrap;\n  white-space: nowrap;\n  margin-left: auto;\n}')

# 5. Top bar item gap
text = text.replace('.top-bar-item {\n  display: inline-flex;\n  align-items: center;\n  gap: 4px;\n}', '.top-bar-item {\n  display: flex;\n  align-items: center;\n  gap: 6px;\n}')

# 6. Active link & Focus visible
active_focus_css = '''
.nav-links a.active {
  font-weight: 700;
  color: var(--primary);
  background-color: rgba(30, 58, 138, 0.05); /* matches hover */
}

.nav-links a:focus-visible, .top-bar a:focus-visible, .logo:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 4px;
  border-radius: var(--radius-sm);
}

.hdr-faculty {
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
'''
if '.nav-links a.active' not in text:
    text += active_focus_css


with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(text)

print('style.css modified')
