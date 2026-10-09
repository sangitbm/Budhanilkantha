import re

# UPDATE HOME.HTML
with open('core/templates/core/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

testimonials_html = '''
{% if testimonials %}
<!-- Testimonials Section -->
<section class="tst-section">
  <div class="container">
    <div class="text-center">
      <p class="tst-subtitle">Student Voices</p>
      <h2 class="section-title">What Our Students Say</h2>
    </div>
    <div class="tst-grid">
      {% for t in testimonials %}
      <div class="tst-card">
        <svg class="tst-quote-icon" xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="currentColor"><path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"/></svg>
        <p class="tst-quote">"{{ t.quote }}"</p>
        <hr class="tst-divider">
        <div class="tst-author">
          {% if t.photo %}
          <img src="{{ t.photo.url }}" alt="{{ t.name }}" class="tst-avatar-img">
          {% else %}
          <div class="tst-avatar-circle">{{ t.name|first|upper }}</div>
          {% endif %}
          <div class="tst-author-info">
            <h3 class="tst-name">{{ t.name }}</h3>
            {% if t.role %}
            <p class="tst-role">{{ t.role }}</p>
            {% endif %}
          </div>
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
</section>
{% endif %}
'''

if '<!-- Testimonials Section -->' not in text:
    text = text.replace('{% endblock %}', testimonials_html + '\n{% endblock %}')
    with open('core/templates/core/home.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Added testimonials to home.html')


# UPDATE STYLE.CSS
with open('static/css/style.css', 'r', encoding='utf-8') as f:
    css_text = f.read()

tst_css = '''
/* Testimonials */
.tst-section {
  padding: 80px 0;
  background: var(--light-bg);
}
.tst-subtitle {
  color: var(--accent);
  text-transform: uppercase;
  letter-spacing: 2px;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 8px;
}
.tst-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 32px;
  margin-top: 48px;
}
@media (min-width: 768px) {
  .tst-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
.tst-card {
  background: var(--white);
  padding: 40px 32px;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  transition: var(--transition);
  position: relative;
  display: flex;
  flex-direction: column;
}
.tst-card:hover {
  box-shadow: var(--shadow-hover);
  transform: translateY(-5px);
}
.tst-quote-icon {
  color: var(--gray-light);
  margin-bottom: 24px;
}
.tst-quote {
  font-size: 1.05rem;
  line-height: 1.6;
  color: var(--text-dark);
  font-style: italic;
  flex-grow: 1;
}
.tst-divider {
  border: 0;
  height: 1px;
  background: #e5e7eb;
  margin: 24px 0;
}
.tst-author {
  display: flex;
  align-items: center;
  gap: 16px;
}
.tst-avatar-img {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  object-fit: cover;
}
.tst-avatar-circle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--white);
}
.tst-author-info {
  display: flex;
  flex-direction: column;
}
.tst-name {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 4px;
}
.tst-role {
  font-size: 0.9rem;
  margin: 0;
}

/* Cycle colors: nth-child */
.tst-card:nth-child(3n+1) .tst-avatar-circle {
  background: var(--primary);
}
.tst-card:nth-child(3n+1) .tst-name, .tst-card:nth-child(3n+1) .tst-role {
  color: var(--primary);
}

.tst-card:nth-child(3n+2) .tst-avatar-circle {
  background: var(--accent);
}
.tst-card:nth-child(3n+2) .tst-name, .tst-card:nth-child(3n+2) .tst-role {
  color: var(--accent);
}

.tst-card:nth-child(3n+3) .tst-avatar-circle {
  background: var(--secondary);
}
.tst-card:nth-child(3n+3) .tst-name, .tst-card:nth-child(3n+3) .tst-role {
  color: var(--secondary);
}
'''
if '.tst-section' not in css_text:
    with open('static/css/style.css', 'a', encoding='utf-8') as f:
        f.write(tst_css)
    print('Added testimonials CSS')
