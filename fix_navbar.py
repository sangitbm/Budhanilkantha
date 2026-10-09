import re

file_path = r'c:\Users\sangi\Desktop\budhanilkantha_school\templates\base.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# ADD MARQUEE TO ANNOUNCEMENT BAR
old_announcement_text = """<a href="{% url 'admissions' %}" style="color: var(--white); text-decoration: none; font-size: 0.95rem; font-weight: 600; text-align: center; width: 100%;">
        {{ site_settings.marquee_text|default:"Hurry up! Admissions are open — limited seats available." }}
      </a>"""
new_announcement_text = """<div style="flex: 1; overflow: hidden;">
        <marquee behavior="scroll" direction="left" scrollamount="6" style="color: var(--white); font-size: 0.95rem; font-weight: 600; padding-top: 4px;">
            <a href="{% url 'admissions' %}" style="color: var(--white); text-decoration: none;">
                {{ site_settings.marquee_text|default:"Hurry up! Admissions are open — limited seats available." }}
            </a>
        </marquee>
      </div>"""
content = content.replace(old_announcement_text, new_announcement_text)

# Fix possible navbar alignment issue if logo is missing or too big
# Ensure navbar-inner has a nice height
navbar_fix = """<div class="container navbar-inner" style="padding: 16px 24px; min-height: 80px;">"""
content = content.replace('<div class="container navbar-inner" style="padding: 18px 24px;">', navbar_fix)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Navbar marquee added.")
