import re

file_path = r'c:\Users\sangi\Desktop\budhanilkantha_school\core\templates\core\dashboard_settings.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add grade-pill CSS
css_to_add = """
    /* Grade Pills CSS */
    .grade-pill {
        padding: 6px 14px;
        background: #f9fbfc;
        border: 1px solid #d1d5db;
        border-radius: 20px;
        font-size: 0.9rem;
        color: var(--text-muted);
        cursor: pointer;
        user-select: none;
        transition: all 0.2s ease;
    }
    .grade-pill:hover {
        border-color: var(--primary);
    }
    /* We use :has input:checked for pure CSS active state */
    .grade-pill:has(input:checked) {
        background: var(--primary);
        color: white;
        border-color: var(--primary);
    }
"""
if ".grade-pill {" not in content:
    content = content.replace("</style>", css_to_add + "\n</style>")

# Insert open_grades UI into admissions card
admissions_ui = """
                <div class="form-field full">
                    <label class="toggle-container" style="display: flex; gap: 12px; margin-bottom: 24px; font-weight: 600; color: var(--primary);">
                        {{ form.admissions_open }} Enable Admissions Campaign on Website
                    </label>
                </div>

                <div class="form-field full" style="margin-bottom: 24px;">
                    <label>Open Grades for Admission</label>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">Select which grades are currently accepting applications. If none are selected, all grades will be shown in the admission form.</p>
                    <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                        {% for grade in all_grades %}
                        <label class="grade-pill">
                            <input type="checkbox" name="open_grades" value="{{ grade }}" style="display: none;" {% if grade in form.instance.open_grades %}checked{% endif %}>
                            {{ grade }}
                        </label>
                        {% endfor %}
                    </div>
                </div>
                
                <div class="form-grid">
"""

content = re.sub(r'<div class="form-field full">\s*<label class="toggle-container".*?</div>\s*<div class="form-grid">', admissions_ui, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Restored open_grades pill checkboxes.")
