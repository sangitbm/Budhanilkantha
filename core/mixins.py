from django.db import models
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse

from core.permissions import StaffRequiredMixin
from core.signals import get_file_fields

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

    def get_thumbnail_url(self, obj):
        return None

    def get_context_data(self, **kwargs):
        if not self.list_url_name:
            raise ImproperlyConfigured("DashboardDeleteMixin requires list_url_name to be set.")
            
        context = super().get_context_data(**kwargs)
        obj = self.object
        
        context['object_type'] = self.object_type
        context['object_label'] = self.get_object_label(obj)
        context['details'] = self.get_details(obj)
        context['thumbnail_url'] = self.get_thumbnail_url(obj)
        impact = self.impact if self.impact is not None else ""
        file_fields = get_file_fields(obj)
        if file_fields:
            if len(file_fields) == 1 and isinstance(obj._meta.get_field(file_fields[0]), models.ImageField):
                impact += " The image will also be deleted."
            else:
                impact += " The attached file will also be deleted."
            
        context['impact'] = impact
        context['cancel_url'] = reverse(self.list_url_name)
        context['cancel_label'] = self.list_label
        return context

    def form_valid(self, form):
        obj = self.object
        label = self.get_object_label(obj)
        response = super().form_valid(form)
        
        obj_type_cap = str(self.object_type).capitalize() if self.object_type else "Item"
        messages.success(self.request, f'{obj_type_cap} "{label}" was deleted.')
        
        return response
