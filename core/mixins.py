from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_active and self.request.user.is_staff

class DashboardDeleteMixin(StaffRequiredMixin):
    template_name = 'includes/dashboard_delete_shell.html'
    object_type = None
    list_url_name = None
    list_label = None
    impact = None

    def get_object_label(self, obj):
        return str(obj)

    def get_details(self, obj):
        return []

    def get_context_data(self, **kwargs):
        if not self.list_url_name:
            raise ImproperlyConfigured("DashboardDeleteMixin requires list_url_name to be set.")
            
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        
        context['object_type'] = self.object_type
        context['object_label'] = self.get_object_label(obj)
        context['details'] = self.get_details(obj)
        context['impact'] = self.impact
        context['cancel_url'] = reverse(self.list_url_name)
        context['cancel_label'] = self.list_label
        return context

    def form_valid(self, form):
        obj = self.get_object()
        label = self.get_object_label(obj)
        response = super().form_valid(form)
        
        obj_type_cap = str(self.object_type).capitalize() if self.object_type else "Item"
        messages.success(self.request, f'{obj_type_cap} "{label}" was deleted.')
        
        return response
