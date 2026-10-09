import re
import os

# 1. Update core/views.py
views_path = r'c:\Users\sangi\Desktop\budhanilkantha_school\core\views.py'
with open(views_path, 'r', encoding='utf-8') as f:
    views_content = f.read()

dismiss_view = """
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

@require_POST
def dismiss_announcement(request):
    request.session['announcement_dismissed'] = True
    next_url = request.POST.get('next')
    if next_url and url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure()
    ):
        return redirect(next_url)
    return redirect('home')
"""
if "def dismiss_announcement" not in views_content:
    views_content += "\n" + dismiss_view

with open(views_path, 'w', encoding='utf-8') as f:
    f.write(views_content)

# 2. Update core/urls.py
urls_path = r'c:\Users\sangi\Desktop\budhanilkantha_school\core\urls.py'
with open(urls_path, 'r', encoding='utf-8') as f:
    urls_content = f.read()

# Add path
dismiss_path = "    path('dismiss-announcement/', views.dismiss_announcement, name='dismiss-announcement'),\n"
if "dismiss-announcement" not in urls_content:
    urls_content = urls_content.replace(
        "path('contact/', views.ContactView.as_view(), name='contact'),",
        "path('contact/', views.ContactView.as_view(), name='contact'),\n" + dismiss_path
    )
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(urls_content)

print("views.py and urls.py patched.")
