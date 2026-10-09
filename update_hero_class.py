with open('core/templates/core/dashboard_settings.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('class="st-hero-card"', 'class="st-hero-thumb"')

with open('core/templates/core/dashboard_settings.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated HTML')
