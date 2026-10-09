with open('templates/base.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('<a href="{{ site_settings.facebook_url }}" target="_blank">', '<a href="{{ site_settings.facebook_url }}" target="_blank" aria-label="Facebook" rel="noopener noreferrer">')

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated aria-label on top-bar facebook link")
