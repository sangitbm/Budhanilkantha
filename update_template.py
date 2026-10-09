import re

file_path = r'c:\Users\sangi\Desktop\budhanilkantha_school\core\templates\core\dashboard_settings.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. ADD RADIO BUTTONS FOR TABS BEFORE layout
tabs_html = """
    <!-- CSS-only tabs -->
    <input type="radio" name="tab" id="tab-school" value="school" class="st-tab-radio" form="settingsForm" {% if active_tab == 'school' %}checked{% endif %}>
    <input type="radio" name="tab" id="tab-about" value="about" class="st-tab-radio" form="settingsForm" {% if active_tab == 'about' %}checked{% endif %}>
    <input type="radio" name="tab" id="tab-programs" value="programs" class="st-tab-radio" form="settingsForm" {% if active_tab == 'programs' %}checked{% endif %}>
    <input type="radio" name="tab" id="tab-contact" value="contact" class="st-tab-radio" form="settingsForm" {% if active_tab == 'contact' %}checked{% endif %}>
    <input type="radio" name="tab" id="tab-social" value="social" class="st-tab-radio" form="settingsForm" {% if active_tab == 'social' %}checked{% endif %}>
    <input type="radio" name="tab" id="tab-admissions" value="admissions" class="st-tab-radio" form="settingsForm" {% if active_tab == 'admissions' %}checked{% endif %}>
    <input type="radio" name="tab" id="tab-seo" value="seo" class="st-tab-radio" form="settingsForm" {% if active_tab == 'seo' or active_tab == 'advanced' %}checked{% endif %}>
    <input type="radio" name="tab" id="tab-advanced" value="advanced" class="st-tab-radio" form="settingsForm" {% if active_tab == 'advanced' %}checked{% endif %}>

<div class="settings-layout">
"""
content = content.replace('<div class="settings-layout">', tabs_html)

# 2. CHANGE ASIDE LINKS TO LABELS
menu_html_old = """<aside class="settings-menu">
        <h6 class="menu-title">Settings Menu</h6>
        <ul class="menu-list">
            <li>
                <a href="#school" class="menu-item active">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path></svg>
                    School Info
                </a>
            </li>
            <li>
                <a href="#contact" class="menu-item">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
                    Contact
                </a>
            </li>
            <li>
                <a href="#social" class="menu-item">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg>
                    Social Media
                </a>
            </li>
            <li>
                <a href="#admissions" class="menu-item">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path></svg>
                    Admissions
                </a>
            </li>
            <li>
                <a href="#programs" class="menu-item">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>
                    Programs
                </a>
            </li>
            <li>
                <a href="#seo" class="menu-item">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                    SEO
                </a>
            </li>
            <li>
                <a href="#advanced" class="menu-item">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
                    Advanced
                </a>
            </li>
        </ul>
    </aside>"""

menu_html_new = """<aside class="settings-menu st-menu-container">
        <h6 class="menu-title">Settings Menu</h6>
        <div class="menu-list st-scrollable-menu">
            <label for="tab-school" class="menu-item st-menu-school">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path></svg>
                School Info {% if tab_errors.school %}<span class="st-error-dot">{{ tab_errors.school }}</span>{% endif %}
            </label>
            <label for="tab-about" class="menu-item st-menu-about">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
                About Us {% if tab_errors.about %}<span class="st-error-dot">{{ tab_errors.about }}</span>{% endif %}
            </label>
            <label for="tab-programs" class="menu-item st-menu-programs">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>
                Programs {% if tab_errors.programs %}<span class="st-error-dot">{{ tab_errors.programs }}</span>{% endif %}
            </label>
            <label for="tab-contact" class="menu-item st-menu-contact">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
                Contact {% if tab_errors.contact %}<span class="st-error-dot">{{ tab_errors.contact }}</span>{% endif %}
            </label>
            <label for="tab-social" class="menu-item st-menu-social">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg>
                Social Media {% if tab_errors.social %}<span class="st-error-dot">{{ tab_errors.social }}</span>{% endif %}
            </label>
            <label for="tab-admissions" class="menu-item st-menu-admissions">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path></svg>
                Admissions {% if tab_errors.admissions %}<span class="st-error-dot">{{ tab_errors.admissions }}</span>{% endif %}
            </label>
            <label for="tab-seo" class="menu-item st-menu-seo">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                SEO {% if tab_errors.seo %}<span class="st-error-dot">{{ tab_errors.seo }}</span>{% endif %}
            </label>
            <label for="tab-advanced" class="menu-item st-menu-advanced">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
                Advanced {% if tab_errors.advanced %}<span class="st-error-dot">{{ tab_errors.advanced }}</span>{% endif %}
            </label>
        </div>
    </aside>"""
content = content.replace(menu_html_old, menu_html_new)

# 3. ADD MISSING ABOUT TAB CONTENT (Was missing entirely in the stacked layout!)
# Wait, I didn't add an About section in the stacked layout earlier! The user's prompt specifically mentions "About Us" tab.
# Let's add it right after School Info.
about_card = """
            <!-- About Info -->
            <div class="settings-card st-card-about" id="about">
                <div class="card-header">
                    <div class="card-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle></svg></div>
                    <div><h2 class="card-title">About Us</h2><p class="card-subtitle">Manage about section and stats</p></div>
                </div>
                <div class="form-grid">
                    <div class="form-field full"><label>About Image</label>{{ form.about_image }}</div>
                    <div class="form-field full"><label>About Text</label>{{ form.about_text }}</div>
                    <div class="form-field full"><label>Curriculum Text</label>{{ form.curriculum_text }}</div>
                    <div class="form-field"><label>Value 1</label>{{ form.value_1 }}</div>
                    <div class="form-field"><label>Value 2</label>{{ form.value_2 }}</div>
                    <div class="form-field"><label>Value 3</label>{{ form.value_3 }}</div>
                    <div class="form-field"><label>Students Stat</label>{{ form.stat_students }}</div>
                    <div class="form-field"><label>Faculty Stat</label>{{ form.stat_faculty }}</div>
                    <div class="form-field"><label>Support Stat</label>{{ form.stat_support }}</div>
                </div>
            </div>
"""
if 'st-card-about' not in content:
    content = content.replace('<!-- Contact Information -->', about_card + '            <!-- Contact Information -->')

# 4. APPEND st-card CLASSES TO EACH CARD
content = content.replace('<div class="settings-card" id="school">', '<div class="settings-card st-card-school" id="school">')
content = content.replace('<div class="settings-card" id="contact">', '<div class="settings-card st-card-contact" id="contact">')
content = content.replace('<div class="settings-card" id="social">', '<div class="settings-card st-card-social" id="social">')
content = content.replace('<div class="settings-card" id="admissions">', '<div class="settings-card st-card-admissions" id="admissions">')
content = content.replace('<div class="settings-card" id="programs">', '<div class="settings-card st-card-programs" id="programs">')
content = content.replace('<div class="settings-card" id="seo">', '<div class="settings-card st-card-seo" id="seo">')
content = content.replace('<div class="settings-card" id="advanced">', '<div class="settings-card st-card-advanced" id="advanced">')

# 5. REDESIGN ADMISSIONS GRADES (grouped)
grades_old = """<div class="form-field full" style="margin-bottom: 24px;">
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
                </div>"""
grades_new = """<div class="form-field full" style="margin-bottom: 24px;">
                    <label>Open Grades for Admission</label>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">Select the grades currently accepting applications. Leave all unselected to show every grade.</p>
                    
                    {% for group_name, group_grades in grouped_grades %}
                    <div style="margin-bottom: 16px;">
                        <h6 style="font-size: 0.8rem; font-weight: 600; color: var(--text-dark); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em;">{{ group_name }}</h6>
                        <div class="st-grade-grid">
                            {% for grade in group_grades %}
                            <label class="st-grade-pill">
                                <input type="checkbox" name="open_grades" value="{{ grade }}" class="st-visually-hidden" {% if grade in form.instance.open_grades %}checked{% endif %}>
                                <span class="st-pill-text">{{ grade }}</span>
                            </label>
                            {% endfor %}
                        </div>
                    </div>
                    {% endfor %}
                </div>"""
content = content.replace(grades_old, grades_new)


# 6. INJECT CSS AT THE END OF STYLE BLOCK
css = """
    /* --- TAB LOGIC --- */
    .st-tab-radio {
        position: absolute;
        opacity: 0;
        width: 1px;
        height: 1px;
        overflow: hidden;
    }
    
    .settings-card {
        display: none; /* hide all by default */
    }
    
    #tab-school:checked ~ .settings-layout .st-card-school,
    #tab-about:checked ~ .settings-layout .st-card-about,
    #tab-programs:checked ~ .settings-layout .st-card-programs,
    #tab-contact:checked ~ .settings-layout .st-card-contact,
    #tab-social:checked ~ .settings-layout .st-card-social,
    #tab-admissions:checked ~ .settings-layout .st-card-admissions,
    #tab-seo:checked ~ .settings-layout .st-card-seo,
    #tab-advanced:checked ~ .settings-layout .st-card-advanced {
        display: block;
        animation: st-fade-in 0.3s ease;
    }
    
    #tab-school:checked ~ .settings-layout .st-menu-school,
    #tab-about:checked ~ .settings-layout .st-menu-about,
    #tab-programs:checked ~ .settings-layout .st-menu-programs,
    #tab-contact:checked ~ .settings-layout .st-menu-contact,
    #tab-social:checked ~ .settings-layout .st-menu-social,
    #tab-admissions:checked ~ .settings-layout .st-menu-admissions,
    #tab-seo:checked ~ .settings-layout .st-menu-seo,
    #tab-advanced:checked ~ .settings-layout .st-menu-advanced {
        background: #eef2ff;
        color: var(--primary);
    }
    
    .st-tab-radio:focus-visible ~ .settings-layout .menu-list label {
        /* outline */
    }

    @keyframes st-fade-in {
        from { opacity: 0; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .st-error-dot {
        background: #e74c3c;
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.7rem;
        font-weight: bold;
        margin-left: auto;
    }

    .menu-item {
        cursor: pointer; /* because they are labels now */
    }

    /* --- MOBILE MENU --- */
    @media (max-width: 768px) {
        .settings-layout {
            grid-template-columns: 1fr !important;
            display: flex;
            flex-direction: column;
        }
        .st-menu-container {
            display: block !important;
            position: static !important;
            width: 100%;
            margin-bottom: 20px;
        }
        .st-scrollable-menu {
            display: flex;
            flex-direction: row;
            overflow-x: auto;
            white-space: nowrap;
            padding-bottom: 10px;
        }
        .st-scrollable-menu label {
            flex-shrink: 0;
        }
        .menu-title { display: none; }
    }

    /* --- PILL CHECKBOXES --- */
    .st-visually-hidden {
        position: absolute;
        opacity: 0;
        width: 1px;
        height: 1px;
        overflow: hidden;
    }
    .st-grade-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(92px, 1fr));
        gap: 10px;
    }
    .st-grade-pill {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 8px;
        background: white;
        border: 1px solid #d1d5db;
        border-radius: 20px;
        font-size: 0.85rem;
        color: var(--text-muted);
        cursor: pointer;
        transition: all 0.2s;
        text-align: center;
    }
    .st-grade-pill:hover {
        border-color: var(--primary);
    }
    /* Add focus-visible */
    .st-grade-pill:has(input:focus-visible) {
        outline: 2px solid var(--primary);
        outline-offset: 2px;
    }
    /* Active State */
    .st-grade-pill:has(input:checked) {
        background: var(--primary);
        color: white;
        border-color: var(--primary);
    }
    .st-grade-pill:has(input:checked) .st-pill-text::before {
        content: '✓';
        margin-right: 4px;
        font-weight: bold;
    }
"""

content = content.replace("</style>", css + "\n</style>")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Template updated successfully.")
