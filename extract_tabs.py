import re
import io
with io.open('core/templates/core/dashboard_settings.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("== School Tab Fields ==")
school_match = re.search(r'(<div class="tab-pane[^>]*id="tab_school".*?)(?=<div class="tab-pane|$)', text, re.DOTALL)
if school_match:
    fields = re.findall(r'name="([^"]+)"', school_match.group(1))
    print(fields)

print("\n== Admissions Tab Fields ==")
admissions_match = re.search(r'(<div class="tab-pane[^>]*id="tab_admissions".*?)(?=<div class="tab-pane|$)', text, re.DOTALL)
if admissions_match:
    fields = re.findall(r'name="([^"]+)"', admissions_match.group(1))
    print(fields)
    
print("\n== Replace School Tab ==")
if school_match:
    new_school = school_match.group(1).replace('</form>', '<!-- Ticker --></form>')
    # Let's just find exactly where to insert ticker in school tab
