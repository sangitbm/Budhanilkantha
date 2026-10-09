import os

with open('core/urls.py', 'r', encoding='utf-8') as f:
    text = f.read()

append_imports = '''    DashboardTestimonialListView, TestimonialCreateView,
    TestimonialUpdateView, TestimonialDeleteView,
'''
if 'DashboardTestimonialListView' not in text:
    text = text.replace('program_remove_view', 'program_remove_view,\n' + append_imports)

    append_urls = '''    path('dashboard/testimonials/', DashboardTestimonialListView.as_view(), name='dashboard-testimonials'),
    path('dashboard/testimonials/add/', TestimonialCreateView.as_view(), name='testimonial-add'),
    path('dashboard/testimonials/<int:pk>/edit/', TestimonialUpdateView.as_view(), name='testimonial-edit'),
    path('dashboard/testimonials/<int:pk>/delete/', TestimonialDeleteView.as_view(), name='testimonial-delete'),
]'''
    text = text.replace(']', append_urls)
    
    with open('core/urls.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated urls.py')

with open('core/admin.py', 'r', encoding='utf-8') as f:
    admin_text = f.read()
    
if 'Testimonial' not in admin_text:
    admin_text = admin_text.replace('from .models import', 'from .models import Testimonial,')
    admin_text += '''
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'is_published', 'order', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('name', 'role', 'quote')
    ordering = ('order', '-created_at')
'''
    with open('core/admin.py', 'w', encoding='utf-8') as f:
        f.write(admin_text)
    print('Updated admin.py')
