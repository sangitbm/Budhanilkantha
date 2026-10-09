import re

with open('core/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

replacement = '''class HomePageView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testimonials'] = Testimonial.objects.filter(is_published=True).order_by('order', '-created_at')[:3]
        return context'''

if "context['testimonials']" not in text:
    text = re.sub(r'class HomePageView\(TemplateView\):\s*template_name = \'core/home\.html\'', replacement, text)
    with open('core/views.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated HomePageView')
