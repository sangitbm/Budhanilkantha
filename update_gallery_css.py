with open('static/css/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

css = '''
/* Gallery Fixes */
.gal-breadcrumb {
  margin-bottom: 12px;
  color: var(--text-muted);
  font-size: 0.95rem;
}
.gal-breadcrumb a {
  color: var(--primary);
  text-decoration: none;
}
.gal-breadcrumb a:hover {
  text-decoration: underline;
}
.gal-count {
  margin-top: 8px;
  font-size: 0.95rem;
  color: var(--text-muted);
}
.gal-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
  margin-top: 40px;
  width: 100%;
}
@media (max-width: 480px) {
  .gal-grid {
    grid-template-columns: 1fr;
  }
}
.gal-card {
  background: var(--white);
  border-radius: 14px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.gal-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}
.gal-link {
  display: block;
}
.gal-img {
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
  display: block;
}
.gal-body {
  padding: 16px;
}
.gal-title {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 4px 0;
  color: var(--text-dark);
}
.gal-desc {
  font-size: 0.9rem;
  color: var(--text-muted);
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.gal-empty {
  grid-column: 1 / -1;
  text-align: center;
  padding: 64px 24px;
  background: var(--white);
  border-radius: 14px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}
.gal-empty-icon {
  color: #9ca3af;
  margin-bottom: 16px;
}
.gal-pagination-wrapper {
  margin-top: 48px;
}
.gal-lightbox {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.9);
  z-index: 9999;
  align-items: center;
  justify-content: center;
}
.gal-lightbox:target {
  display: flex;
}
.gal-lightbox-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.gal-lightbox-img {
  max-width: 90vw;
  max-height: 85vh;
  object-fit: contain;
}
.gal-lightbox-title {
  color: white;
  margin-top: 16px;
  font-size: 1.1rem;
  text-align: center;
}
.gal-close, .gal-prev, .gal-next {
  position: fixed;
  color: white;
  text-decoration: none;
  font-size: 2.5rem;
  padding: 16px;
  opacity: 0.8;
  transition: opacity 0.2s;
}
.gal-close:hover, .gal-prev:hover, .gal-next:hover {
  opacity: 1;
}
.gal-close {
  top: 16px;
  right: 24px;
  font-size: 3rem;
  line-height: 1;
}
.gal-close:focus-visible {
  outline: 2px solid white;
  outline-offset: 4px;
}
.gal-prev {
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
}
.gal-next {
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
}
'''
if '.gal-lightbox' not in text:
    with open('static/css/style.css', 'a', encoding='utf-8') as f:
        f.write(css)
    print('Updated CSS')
