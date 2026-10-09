import os

with open('core/templates/core/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Load tags
text = text.replace('{% load static %}', '{% load static ui %}')

# Hero block replace
search_hero = '''    <div class="hero-content">
      {% if site_settings.admissions_open %}
      <div class="hero-badge" style="display: inline-block; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: var(--white); padding: 6px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 500; margin-bottom: 16px;">
        🎓 Admissions Open for 2083 BS
      </div>
      {% endif %}
      
      <p class="tagline">Welcome to {{ site_settings.school_name }}</p>
      
      <h1 style="color: var(--white);"><span style="color: var(--accent);">Excellence</span> in Education</h1>
      
      <p class="legacy">Quality Education Since {{ site_settings.established_year }} AD</p>
      
      <p>{% if site_settings.about_short %}{{ site_settings.about_short }}{% else %}A premier institution dedicated to providing quality education and fostering holistic development for our students.{% endif %}</p>
      
      <div class="hero-buttons">
        {% if site_settings.admissions_open %}
        <a href="{% url 'admissions' %}" class="btn btn-accent">Apply for Admission 2083</a>
        {% endif %}
        <a href="{% url 'about' %}" class="btn btn-outline">Learn More</a>
      </div>
    </div>
    
    <div class="hero-visual" style="position: relative;">
      {% if site_settings.hero_images.all %}
      <div class="hero-slider" style="position: relative; border-radius: var(--radius); box-shadow: var(--shadow-hover); width: 100%; aspect-ratio: 4/3; overflow: hidden; background: #000;">
        {% for hero in site_settings.hero_images.all %}
        <img src="{{ hero.image.url }}" alt="{{ site_settings.school_name }}" class="hero-slide" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; opacity: {% if forloop.first %}1{% else %}0{% endif %}; transition: opacity 1s ease-in-out;">
        {% endfor %}
      </div>
      <script>
        document.addEventListener('DOMContentLoaded', () => {
          const slides = document.querySelectorAll('.hero-slide');
          if(slides.length > 1) {
            let current = 0;
            setInterval(() => {
              slides[current].style.opacity = '0';
              current = (current + 1) % slides.length;
              slides[current].style.opacity = '1';
            }, 4000);
          }
        });
      </script>
      {% else %}
      <img src="https://via.placeholder.com/600x400?text=School+Building+Image" alt="Budhanilkantha School" style="border-radius: var(--radius); box-shadow: var(--shadow-hover); width: 100%; object-fit: cover; aspect-ratio: 4/3;">
      {% endif %}
    </div>'''

replace_hero = '''    <div class="hero-content">
      {% if site_settings.is_admission_active %}
      <div class="hero-badge">
        <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:text-bottom;margin-right:4px;"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>
        {% if site_settings.admissions_badge %}{{ site_settings.admissions_badge }}{% else %}Admissions Open{% endif %}
      </div>
      {% endif %}
      
      <h1><span class="hero-accent">{{ site_settings.tagline|default:'Excellence in Education'|first_word }}</span> {{ site_settings.tagline|default:'Excellence in Education'|rest_words }}</h1>
      
      <p>
        {% if site_settings.about_short %}{{ site_settings.about_short }}{% else %}A premier institution dedicated to providing quality education and fostering holistic development for our students.{% endif %}
        <span class="hero-legacy">Quality Education Since {{ site_settings.established_year }} AD</span>
      </p>
      
      <div class="hero-buttons">
        {% if site_settings.is_admission_active %}
        <a href="{% url 'admissions' %}" class="btn btn-accent">{% if site_settings.admissions_btn_label %}{{ site_settings.admissions_btn_label }}{% else %}Apply for Admission{% endif %}</a>
        {% endif %}
        <a href="{% url 'about' %}" class="btn btn-outline">Learn More</a>
      </div>
    </div>
    
    <div class="hero-visual">
      {% if site_settings.hero_images.all %}
      <img src="{{ site_settings.hero_images.first.image.url }}" alt="{{ site_settings.school_name }}" class="hero-img">
      {% else %}
      <img src="{% static 'img/hero-fallback.jpg' %}" alt="{{ site_settings.school_name }}" class="hero-img">
      {% endif %}
    </div>'''

text = text.replace(search_hero, replace_hero)

search_features = '''<section class="container" style="position: relative;">
  <div class="features-grid">
    <div class="feature-card">
      <div class="feature-icon" style="background: rgba(26, 74, 138, 0.1); color: var(--primary); width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 16px;">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>
      </div>
      <h3>Quality Education</h3>
      <p>Committed to rigorous academic standards and holistic development.</p>
    </div>
    <div class="feature-card">
      <div class="feature-icon" style="background: rgba(26, 74, 138, 0.1); color: var(--primary); width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 16px;">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>
      </div>
      <h3>Experienced Faculty</h3>
      <p>Dedicated professionals guiding students with expertise and care.</p>
    </div>
    <div class="feature-card">
      <div class="feature-icon" style="background: rgba(26, 74, 138, 0.1); color: var(--primary); width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 16px;">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>
      </div>
      <h3>Modern Facilities</h3>
      <p>State-of-the-art infrastructure for learning and growth.</p>
    </div>
  </div>
</section>'''

replace_features = '''<section class="container hero-features-container">
  <div class="features-grid">
    <div class="feature-card">
      <div class="feature-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>
      </div>
      <h3>Quality Education</h3>
      <p>Committed to rigorous academic standards and holistic development.</p>
    </div>
    <div class="feature-card">
      <div class="feature-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>
      </div>
      <h3>Experienced Faculty</h3>
      <p>Dedicated professionals guiding students with expertise and care.</p>
    </div>
    <div class="feature-card">
      <div class="feature-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>
      </div>
      <h3>Modern Facilities</h3>
      <p>State-of-the-art infrastructure for learning and growth.</p>
    </div>
  </div>
</section>'''

text = text.replace(search_features, replace_features)

with open('core/templates/core/home.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('home.html modified')
