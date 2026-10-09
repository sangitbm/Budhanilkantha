import re

# Patch home.html
home_path = r'c:\Users\sangi\Desktop\budhanilkantha_school\core\templates\core\home.html'
with open(home_path, 'r', encoding='utf-8') as f:
    home_content = f.read()

# Replace hardcoded program sections
program_replacement = """        <div class="row">
            {% for program in site_settings.academic_programs.all %}
            <div class="col-md-6 mb-4">
                <div class="card h-100 shadow-sm" style="border: none; border-radius: var(--radius-md);">
                    <div class="card-body p-4 text-center">
                        <div style="width: 60px; height: 60px; background: rgba(30,58,138,0.1); color: var(--primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
                        </div>
                        <h4 style="color: var(--primary); margin-bottom: 15px;">{{ program.title }}</h4>
                        <p class="text-muted">{{ program.description }}</p>
                    </div>
                </div>
            </div>
            {% empty %}
            <div class="col-12 text-center text-muted">
                <p>No academic programs listed currently.</p>
            </div>
            {% endfor %}
        </div>"""

home_content = re.sub(
    r'        <div class="row">.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>',
    program_replacement,
    home_content,
    flags=re.DOTALL
)

with open(home_path, 'w', encoding='utf-8') as f:
    f.write(home_content)

# Patch admission_form.html
admission_path = r'c:\Users\sangi\Desktop\budhanilkantha_school\core\templates\core\admission_form.html'
with open(admission_path, 'r', encoding='utf-8') as f:
    admission_content = f.read()

admission_grade_replacement = """                            <label class="form-label fw-bold">Grade Applying For</label>
                            {% if site_settings.open_grades %}
                                <select name="grade_applying_for" class="form-select form-control" required>
                                    <option value="">-- Select Grade --</option>
                                    {% for grade in site_settings.open_grades %}
                                        <option value="{{ grade }}">{{ grade }}</option>
                                    {% endfor %}
                                </select>
                            {% else %}
                                {{ form.grade_applying_for }}
                            {% endif %}"""

admission_content = re.sub(
    r'                            <label class="form-label fw-bold">Grade Applying For</label>\s*{{ form.grade_applying_for }}',
    admission_grade_replacement,
    admission_content
)

with open(admission_path, 'w', encoding='utf-8') as f:
    f.write(admission_content)

print("HTML pages updated.")
