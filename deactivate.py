import re

file_path = r'c:\Users\sangi\Desktop\budhanilkantha_school\core\templates\core\dashboard_settings.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. FIX FILE UPLOADS (Remove .upload-btn-wrapper)
# Principal Photo
photo_old = """<div class="upload-btn-wrapper">
                                            <button type="button" class="custom-upload-btn">
                                                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                                                Upload Photo
                                            </button>
                                            {{ form.principal_photo }}
                                        </div>"""
content = content.replace(photo_old, '{{ form.principal_photo }}')

# Logo
logo_old = """<div class="upload-btn-wrapper">
                                    <button type="button" class="custom-upload-btn">Upload icon</button>
                                    {{ form.logo }}
                                </div>"""
content = content.replace(logo_old, '{{ form.logo }}')

# Favicon
favicon_old = """<div class="upload-btn-wrapper">
                                    <button type="button" class="custom-upload-btn">Upload icon</button>
                                    {{ form.favicon }}
                                </div>"""
content = content.replace(favicon_old, '{{ form.favicon }}')

# Hero Images
hero_old = """<div class="upload-btn-wrapper">
                                    <button type="button" class="custom-upload-btn">Upload cover image</button>
                                    <input type="file" name="hero_images" multiple accept="image/*">
                                </div>"""
content = content.replace(hero_old, '<input type="file" name="hero_images" multiple accept="image/*">')

# About Image
about_old = """<div class="upload-btn-wrapper">
                            <button type="button" class="custom-upload-btn">
                                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                                Upload Image
                            </button>
                            {{ form.about_image }}
                        </div>"""
content = content.replace(about_old, '{{ form.about_image }}')

# OG Image
og_old = """<div class="upload-btn-wrapper" style="margin-bottom: 8px;">
                                    <button type="button" class="custom-upload-btn" style="background: white; color: var(--text-dark); border: 1px solid var(--gray-light);">
                                        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                                        Select image
                                    </button>
                                    {{ form.og_image }}
                                </div>
                                <span style="font-size: 0.75rem; color: var(--text-muted); margin-left: 12px;">No image selected</span>"""
content = content.replace(og_old, '{{ form.og_image }}')


# 2. REMOVE LIVE PREVIEW
live_preview_block = """    <!-- Live Preview -->
    <aside class="live-preview">
        <h6 class="menu-title">Live Preview</h6>
        <div class="preview-card">
            <div class="preview-header">
                <div class="preview-logo">
                    <div class="preview-logo-circle"></div>
                    BSS
                </div>
                <div class="preview-btn">Apply Now</div>
            </div>
            <div class="preview-body">
                <div class="mock-line"></div>
                <div class="mock-line short"></div>
                <div style="margin-top: 24px; padding: 12px; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px;">
                    <div class="mock-line" style="background: #22c55e;"></div>
                    <div class="mock-line short" style="background: #86efac;"></div>
                </div>
            </div>
        </div>
    </aside>"""
content = content.replace(live_preview_block, '')

# Adjust grid layout
content = content.replace('grid-template-columns: 200px 1fr 280px;', 'grid-template-columns: 200px 1fr;')


# 3. DEACTIVATE SEO
# Remove radio button
content = re.sub(r'<input type="radio" name="tab" id="tab-seo".*?>', '', content)
# Remove menu item
seo_menu = """<label for="tab-seo" class="menu-item st-menu-seo">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                SEO {% if tab_errors.seo %}<span class="st-error-dot">{{ tab_errors.seo }}</span>{% endif %}
            </label>"""
content = content.replace(seo_menu, '')
# Comment out SEO Card
seo_card_start = '<div class="settings-card st-card-seo" id="seo">'
if seo_card_start in content:
    idx = content.find(seo_card_start)
    # find next card (Advanced)
    idx_end = content.find('<!-- Advanced -->', idx)
    seo_card = content[idx:idx_end]
    content = content.replace(seo_card, f'<!-- SEO Deactivated\n{seo_card}\n-->\n')


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Modifications applied.")
