import os

with open('static/css/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

append_css = """
/* Hero additions */
.hero-badge {
  display: inline-flex;
  align-items: center;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.2);
  color: var(--white);
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
  margin-bottom: 16px;
}

.hero-accent {
  color: var(--accent);
}

.hero-legacy {
  display: block;
  font-size: 0.85rem;
  opacity: 0.7;
  margin-top: 8px;
  font-weight: 300;
}

.hero-img {
  width: 100%;
  border-radius: var(--radius);
  box-shadow: var(--shadow-hover);
  object-fit: cover;
  aspect-ratio: 4/3;
  display: block;
}

.hero-visual {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.hero-features-container {
  position: relative;
}

.feature-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
}
.feature-card h3 {
  font-size: 1.1rem;
  margin-bottom: 8px;
}
.feature-card p {
  font-size: 0.95rem;
  margin-bottom: 0;
}
.feature-icon {
  background: rgba(26, 74, 138, 0.1);
  color: var(--primary);
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

@media (max-width: 900px) {
  .hero .container {
    grid-template-columns: 1fr;
    text-align: center;
  }
  .hero-buttons {
    justify-content: center;
  }
  .hero-content p {
    margin-left: auto;
    margin-right: auto;
  }
}
"""

if '.hero-badge' not in text:
    text += append_css
    
with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(text)

print('style updated')
