with open('core/templates/core/dashboard_settings.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_str = '''<button type="submit" name="delete_hero_image_id" value="{{ hero.id }}" class="st-hero-remove" title="Remove" onclick="return confirm('Remove this hero image?');">&times;</button>'''
new_str = '''<button type="submit" name="delete_hero_image_id" value="{{ hero.id }}" class="st-hero-remove" aria-label="Remove hero image" title="Remove hero image" onclick="return confirm('Remove this hero image?');"><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg></button>'''

text = text.replace(old_str, new_str)

with open('core/templates/core/dashboard_settings.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("done")
