import re

with open('core/templates/core/dashboard_base.html', 'r', encoding='utf-8') as f:
    text = f.read()

new_link = '''        <a href="{% url 'dashboard-testimonials' %}" class="sidebar-item {% if request.resolver_match.url_name == 'dashboard-testimonials' or request.resolver_match.url_name == 'testimonial-add' or request.resolver_match.url_name == 'testimonial-edit' %}active{% endif %}">
          <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap=\"round\" stroke-linejoin="round">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          </svg>
          Manage Testimonials
        </a>
'''
if 'dashboard-testimonials' not in text:
    text = re.sub(r'(<a href="{% url \'dashboard-settings\' %}")', new_link + r'\1', text)
    with open('core/templates/core/dashboard_base.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Added sidebar link')
