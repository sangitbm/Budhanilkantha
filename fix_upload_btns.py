import re

file_path = r'c:\Users\sangi\Desktop\budhanilkantha_school\core\templates\core\dashboard_settings.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add CSS for upload buttons
css_to_add = """
    .upload-btn-wrapper {
        position: relative;
        overflow: hidden;
        display: inline-block;
    }
    .upload-btn-wrapper input[type=file] {
        font-size: 100px;
        position: absolute;
        left: 0;
        top: 0;
        opacity: 0;
        cursor: pointer;
        height: 100%;
    }
    .custom-upload-btn {
        background-color: var(--primary);
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: var(--radius-sm);
        font-size: 0.85rem;
        font-weight: 500;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    .custom-upload-btn:hover {
        background-color: var(--primary-dark);
    }
"""
if ".upload-btn-wrapper {" not in content:
    content = content.replace("</style>", css_to_add + "\n</style>")

# Replace standard file inputs with styled ones
# 1. Principal Photo
principal_photo_old = """<div style="flex:1; text-align: left;">
                                        {{ form.principal_photo }}
                                    </div>"""
principal_photo_new = """<div style="flex:1; text-align: left;">
                                        <div class="upload-btn-wrapper">
                                            <button type="button" class="custom-upload-btn">
                                                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                                                Upload Photo
                                            </button>
                                            {{ form.principal_photo }}
                                        </div>
                                    </div>"""
content = content.replace(principal_photo_old, principal_photo_new)

# 2. Logo
logo_old = """<span style="font-size: 0.8rem; font-weight: 500;">School Logo</span>
                                {{ form.logo }}"""
logo_new = """<span style="font-size: 0.8rem; font-weight: 500; margin-bottom:8px;">School Logo</span>
                                <div class="upload-btn-wrapper">
                                    <button type="button" class="custom-upload-btn">Upload icon</button>
                                    {{ form.logo }}
                                </div>"""
content = content.replace(logo_old, logo_new)

# 3. Favicon
favicon_old = """<span style="font-size: 0.8rem; font-weight: 500;">Favicon</span>
                                {{ form.favicon }}"""
favicon_new = """<span style="font-size: 0.8rem; font-weight: 500; margin-bottom:8px;">Favicon</span>
                                <div class="upload-btn-wrapper">
                                    <button type="button" class="custom-upload-btn">Upload icon</button>
                                    {{ form.favicon }}
                                </div>"""
content = content.replace(favicon_old, favicon_new)

# 4. Hero Images
hero_old = """<input type="file" name="hero_images" multiple accept="image/*" class="form-control">"""
hero_new = """<div class="upload-btn-wrapper">
                                    <button type="button" class="custom-upload-btn">Upload cover image</button>
                                    <input type="file" name="hero_images" multiple accept="image/*">
                                </div>"""
content = content.replace(hero_old, hero_new)

# 5. OG Image
og_old = """{{ form.og_image }}"""
og_new = """<div class="upload-btn-wrapper">
                                    <button type="button" class="custom-upload-btn">Select image</button>
                                    {{ form.og_image }}
                                </div>"""
# Careful, this might replace multiple. Let's do it with the surrounding context.
og_context_old = """<div style="flex:1; text-align: left;">
                                {{ form.og_image }}
                                <p style="margin-top: 4px;">1200 x 630 recommended.</p>
                            </div>"""
og_context_new = """<div style="flex:1; text-align: left;">
                                <div class="upload-btn-wrapper" style="margin-bottom: 8px;">
                                    <button type="button" class="custom-upload-btn" style="background: white; color: var(--text-dark); border: 1px solid var(--gray-light);">
                                        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                                        Select image
                                    </button>
                                    {{ form.og_image }}
                                </div>
                                <span style="font-size: 0.75rem; color: var(--text-muted); margin-left: 12px;">No image selected</span>
                            </div>"""
content = content.replace(og_context_old, og_context_new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("File input buttons updated.")
