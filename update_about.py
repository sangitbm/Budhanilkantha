import re

with open('core/templates/core/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove the inline styles
text = re.sub(r'<style>.*?</style>', '', text, flags=re.DOTALL)

# Replace the about section and stats
search_about = r'<section class="about" style="padding: 96px 0;">.*?</section>'
replace_about = '''<section class="about about-section">
  <div class="container">
    <div class="about-grid {% if not site_settings.about_image %}no-image{% endif %}">
      <div class="about-text-wrapper">
        <p class="about-subtitle">About Us</p>
        <h2 class="section-title about-title">Nurturing Minds, Building Futures</h2>
        
        <p class="about-p">{{ site_settings.about_text }}</p>
        <p class="about-p">{{ site_settings.curriculum_text }}</p>

        <!-- Values List -->
        <div class="about-values">
          {% if site_settings.value_1 %}
          <div class="about-value-item">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="about-value-icon"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            {{ site_settings.value_1 }}
          </div>
          {% endif %}
          {% if site_settings.value_2 %}
          <div class="about-value-item">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="about-value-icon"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            {{ site_settings.value_2 }}
          </div>
          {% endif %}
          {% if site_settings.value_3 %}
          <div class="about-value-item">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="about-value-icon"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            {{ site_settings.value_3 }}
          </div>
          {% endif %}
        </div>

        {% if site_settings.principal_photo or site_settings.principal_name or site_settings.principal_message %}
        <!-- Principal Card -->
        <div class="about-principal">
          {% if site_settings.principal_photo %}
          <img src="{{ site_settings.principal_photo.url }}" alt="{{ site_settings.principal_name }}" class="about-principal-img">
          {% else %}
          <div class="about-principal-img-placeholder">{{ site_settings.principal_name|slice:":1" }}</div>
          {% endif %}
          <div>
            {% if site_settings.principal_message %}
            <p class="about-principal-quote">"{{ site_settings.principal_message }}"</p>
            {% endif %}
            <p class="about-principal-name">{{ site_settings.principal_name }} {% if site_settings.principal_name %}<span class="about-principal-role">— Principal</span>{% endif %}</p>
          </div>
        </div>
        {% endif %}

        <a href="{% url 'about' %}" class="btn btn-primary about-btn">
          Read More About Us 
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
        </a>
      </div>

      {% if site_settings.about_image %}
      <div class="about-img-wrapper">
        <img src="{{ site_settings.about_image.url }}" alt="About Us" class="about-img">
        
        <!-- Floating Badge -->
        <div class="about-badge">
          <div class="about-badge-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          </div>
          <div class="about-badge-text-wrapper">
            <div class="about-badge-label">Since</div>
            <div class="about-badge-value">{{ site_settings.established_year }}</div>
          </div>
        </div>
      </div>
      {% endif %}
    </div>

    <!-- Stats Row -->
    <div class="stat-grid">
      <div class="stat-card primary">
        <div class="stat-value">{{ site_settings.established_year|years_since }}</div>
        <div class="stat-label">Years of Excellence</div>
      </div>
      <div class="stat-card accent">
        <div class="stat-value">{{ site_settings.stat_students }}</div>
        <div class="stat-label">Students</div>
      </div>
      <div class="stat-card primary">
        <div class="stat-value">{{ site_settings.stat_faculty }}</div>
        <div class="stat-label">Faculty</div>
      </div>
      <div class="stat-card accent">
        <div class="stat-value">{{ site_settings.stat_support }}</div>
        <div class="stat-label">Support Staff</div>
      </div>
    </div>
  </div>
</section>'''

if re.search(search_about, text, re.DOTALL):
    text = re.sub(search_about, replace_about, text, flags=re.DOTALL)
    print('home replaced successfully')
else:
    print('home NOT replaced')

with open('core/templates/core/home.html', 'w', encoding='utf-8') as f:
    f.write(text)
