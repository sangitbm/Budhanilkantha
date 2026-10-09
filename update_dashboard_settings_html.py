import re

with open('core/templates/core/dashboard_settings.html', 'r', encoding='utf-8') as f:
    text = f.read()

principal_old = '''<div class="upload-box" style="padding: 16px; display: flex; align-items: center; gap: 16px;">
                                    <div style="width: 40px; height: 40px; background: #eef2f6; border-radius: var(--radius-sm); display: flex; align-items: center; justify-content: center; color: var(--text-muted);">
                                        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                                    </div>
                                    <div style="flex:1; text-align: left;">
                                        {{ form.principal_photo }}
                                    </div>
                                </div>'''
principal_new = '''{% include 'includes/image_field.html' with field=form.principal_photo is_circle=True hint="Clear face photo" %}'''
text = text.replace(principal_old, principal_new)

branding_old = '''<div class="small-upload-row">
                            <div class="small-upload">
                                <div class="card-icon" style="background: white; border: 1px dashed var(--gray-light);"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg></div>
                                <span style="font-size: 0.8rem; font-weight: 500; margin-bottom:8px;">School Logo</span>
                                {{ form.logo }}
                            </div>
                            <div class="small-upload">
                                <div class="card-icon" style="background: white; border: 1px dashed var(--gray-light);"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg></div>
                                <span style="font-size: 0.8rem; font-weight: 500; margin-bottom:8px;">Favicon</span>
                                {{ form.favicon }}
                            </div>
                        </div>'''
branding_new = '''<div class="st-branding-row">
                            <div class="st-branding-col">
                                <label>School Logo</label>
                                {% include 'includes/image_field.html' with field=form.logo hint="Square PNG or JPG, at least 256px" %}
                            </div>
                            <div class="st-branding-col">
                                <label>Favicon</label>
                                {% include 'includes/image_field.html' with field=form.favicon hint="Square PNG or ICO, 64 to 512px" %}
                            </div>
                        </div>'''
text = text.replace(branding_old, branding_new)

hero_old = '''<label>Homepage Hero Image</label>
                        <div class="upload-box" style="display: flex; align-items: center; gap: 16px;">
                            <div style="width: 48px; height: 48px; background: #eef2f6; border-radius: var(--radius-sm); display: flex; align-items: center; justify-content: center; color: var(--text-muted);">
                                <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
                            </div>
                            <div style="flex:1; text-align: left;">
                                <input type="file" name="hero_images" multiple accept="image/*">
                                <p style="margin-top: 4px;">Recommended size: 1920x1080. You can upload multiple images for the homepage.</p>
                            </div>
                        </div>'''
hero_new = '''<label>Homepage Hero Images (slider)</label>
                        
                        {% if form.instance.hero_images.all %}
                        <div class="st-hero-grid">
                            {% for hero in form.instance.hero_images.all %}
                            <div class="st-hero-card">
                                <img src="{{ hero.image.url }}" alt="Hero Image">
                                <button type="submit" name="delete_hero_image_id" value="{{ hero.id }}" class="st-hero-remove" title="Remove" onclick="return confirm('Remove this hero image?');">&times;</button>
                            </div>
                            {% endfor %}
                        </div>
                        {% endif %}
                        
                        <div class="st-hero-upload">
                            <input type="file" name="hero_images" multiple accept="image/*" class="st-file-input">
                            <p class="st-img-hint">Recommended 1920x1080. You can select several images.</p>
                        </div>'''
text = text.replace(hero_old, hero_new)

with open('core/templates/core/dashboard_settings.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated dashboard_settings.html')
