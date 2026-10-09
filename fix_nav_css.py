import re

file_path = r'c:\Users\sangi\Desktop\budhanilkantha_school\static\css\style.css'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix navbar inner wrapping
old_navbar = """.navbar-inner {
  padding: 22px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}"""
new_navbar = """.navbar-inner {
  padding: 22px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: nowrap !important;
}"""
content = content.replace(old_navbar, new_navbar)

# Reduce gap on smaller desktops to prevent overflow before hamburger kicks in
if "@media (max-width: 1200px)" not in content:
    css_to_add = """
@media (max-width: 1200px) {
  .nav-links {
    gap: 12px;
  }
  .nav-links a {
    font-size: 0.85rem;
  }
  .nav-apply-btn {
    margin-left: 10px;
    padding: 6px 16px;
  }
}
"""
    content += css_to_add

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Navbar CSS fixed.")
