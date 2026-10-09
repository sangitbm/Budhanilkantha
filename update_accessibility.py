import os
import re

with open('templates/base.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Meta description
if 'site_settings.meta_description' not in text:
    meta_tag = '<meta name="description" content="{% if site_settings.meta_description %}{{ site_settings.meta_description }}{% else %}Budhanilkantha School{% endif %}">'
    text = text.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">', '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n  ' + meta_tag)

# Skip to content
if 'skip-link' not in text:
    text = text.replace('<body class="site-body">', '<body class="site-body">\n  <a href="#main-content" class="skip-link">Skip to content</a>')

# Main tag ID
if 'id="main-content"' not in text:
    text = text.replace('<main>{% block content %}', '<main id="main-content" tabindex="-1">{% block content %}')

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(text)

# Also adding skip-link styles and accessibility focus-visible to style.css
with open('static/css/style.css', 'r', encoding='utf-8') as f:
    style_text = f.read()

append_css = """
/* Accessibility additions */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--primary);
  color: white;
  padding: 8px;
  z-index: 10000;
  transition: top 0.3s;
}
.skip-link:focus {
  top: 0;
}
*:focus-visible {
  outline: 3px solid var(--accent);
  outline-offset: 2px;
}
main#main-content:focus {
  outline: none;
}
"""

if '.skip-link' not in style_text:
    style_text += append_css
    with open('static/css/style.css', 'w', encoding='utf-8') as f:
        f.write(style_text)

print('Updated base.html and style.css for accessibility.')
