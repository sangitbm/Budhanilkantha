import os

with open('core/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

append_text = '''
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Testimonial
from .forms import TestimonialForm

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class DashboardTestimonialListView(StaffRequiredMixin, ListView):
    model = Testimonial
    template_name = 'core/dashboard_testimonial_list.html'
    context_object_name = 'testimonials'

    def post(self, request, *args, **kwargs):
        # Handle toggle publish
        if 'toggle_publish' in request.POST:
            t_id = request.POST.get('testimonial_id')
            t = get_object_or_404(Testimonial, id=t_id)
            t.is_published = not t.is_published
            t.save()
            status = "published" if t.is_published else "unpublished"
            messages.success(request, f"Testimonial by {t.name} is now {status}.")
            return redirect('dashboard-testimonials')
        return redirect('dashboard-testimonials')

class TestimonialCreateView(StaffRequiredMixin, CreateView):
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'core/testimonial_form.html'
    success_url = reverse_lazy('dashboard-testimonials')

    def form_valid(self, form):
        messages.success(self.request, "Testimonial added successfully.")
        return super().form_valid(form)

class TestimonialUpdateView(StaffRequiredMixin, UpdateView):
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'core/testimonial_form.html'
    success_url = reverse_lazy('dashboard-testimonials')

    def form_valid(self, form):
        messages.success(self.request, "Testimonial updated successfully.")
        return super().form_valid(form)

class TestimonialDeleteView(StaffRequiredMixin, DeleteView):
    model = Testimonial
    template_name = 'core/testimonial_confirm_delete.html'
    success_url = reverse_lazy('dashboard-testimonials')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Testimonial deleted.")
        return super().delete(request, *args, **kwargs)
'''

if 'class DashboardTestimonialListView' not in text:
    with open('core/views.py', 'a', encoding='utf-8') as f:
        f.write(append_text)
    print('Added testimonial views')
