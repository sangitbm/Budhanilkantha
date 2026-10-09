import re

with open('core/templates/core/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

search_prog = r'<!-- Programs Section -->.*?<section class="programs section-padding">.*?</section>'
replace_prog = '''{% if site_settings.academic_programs.all %}
<!-- Programs Section -->
<section class="programs prog-section">
  <div class="container">
    <div class="text-center">
      <p class="prog-subtitle">Our Programs</p>
      <h2 class="section-title">Academic Programs We Offer</h2>
      <p class="section-subtitle">Discover our comprehensive curriculum designed to foster academic excellence and personal growth.</p>
    </div>
    <div class="programs-grid prog-grid">
      {% for program in site_settings.academic_programs.all %}
      <div class="program-card {% if not forloop.counter0|divisibleby:2 %}prog-accent{% else %}prog-primary{% endif %}">
        <div class="feature-icon prog-icon">
          {% if forloop.counter0|divisibleby:2 %}
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>
          {% else %}
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          {% endif %}
        </div>
        <h3>{{ program.title }}</h3>
        {% if program.description %}
        <p>{{ program.description }}</p>
        {% endif %}
        <div class="prog-link-wrapper">
          <a href="{% url 'about' %}" class="prog-link">
            Learn more
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </a>
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
</section>
{% endif %}'''

if re.search(search_prog, text, re.DOTALL):
    text = re.sub(search_prog, replace_prog, text, flags=re.DOTALL)
    print("Replaced home.html successfully.")
else:
    print("Could not find programs section.")

with open('core/templates/core/home.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('static/css/style.css', 'r', encoding='utf-8') as f:
    style_text = f.read()

append_css = """
/* Programs additions */
.prog-section {
  padding: 80px 0;
}
.prog-subtitle {
  color: var(--primary);
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.9rem;
  letter-spacing: 1px;
}
.prog-grid {
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)) !important;
  align-items: stretch;
}
.program-card {
  display: flex !important;
  flex-direction: column;
  height: 100%;
}
.prog-icon {
  margin-bottom: 16px;
}
.prog-primary .prog-icon {
  background: rgba(45, 125, 210, 0.1);
  color: var(--secondary);
}
.prog-accent {
  border-top-color: var(--accent) !important;
}
.prog-accent .prog-icon {
  background: rgba(245, 166, 35, 0.1);
  color: var(--accent);
}
.prog-link-wrapper {
  margin-top: auto;
  padding-top: 16px;
}
.prog-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--primary);
  font-weight: 600;
  font-size: 0.95rem;
  transition: var(--transition);
}
.prog-link:hover {
  color: var(--secondary);
}
.prog-link svg {
  transition: transform 0.3s ease;
}
.prog-link:hover svg {
  transform: translateX(4px);
}
.prog-accent .prog-link {
  color: var(--accent);
}
.prog-accent .prog-link:hover {
  color: #d97706; /* darker orange */
}
"""

if '.prog-section' not in style_text:
    style_text += append_css
    
with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(style_text)
