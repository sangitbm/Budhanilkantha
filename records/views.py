from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.permissions import StaffRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Student, Staff
from .forms import StudentForm, StaffForm

# --- Student Views ---
class StudentListView(StaffRequiredMixin, ListView):
    model = Student
    template_name = 'records/dashboard_student_list.html'
    context_object_name = 'students'
    ordering = ['grade', 'first_name']

class StudentCreateView(StaffRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'records/record_form.html'
    success_url = reverse_lazy('dashboard-students')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_type'] = 'Student'
        return context

class StudentUpdateView(StaffRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'records/record_form.html'
    success_url = reverse_lazy('dashboard-students')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_type'] = 'Student'
        return context

class StudentDeleteView(StaffRequiredMixin, DeleteView):
    model = Student
    template_name = 'records/record_confirm_delete.html'
    success_url = reverse_lazy('dashboard-students')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_type'] = 'Student'
        return context


# --- Staff Views ---
class StaffListView(StaffRequiredMixin, ListView):
    model = Staff
    template_name = 'records/dashboard_staff_list.html'
    context_object_name = 'staff_members'
    ordering = ['staff_type', 'first_name']

class StaffCreateView(StaffRequiredMixin, CreateView):
    model = Staff
    form_class = StaffForm
    template_name = 'records/record_form.html'
    success_url = reverse_lazy('dashboard-staff')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_type'] = 'Staff'
        return context

class StaffUpdateView(StaffRequiredMixin, UpdateView):
    model = Staff
    form_class = StaffForm
    template_name = 'records/record_form.html'
    success_url = reverse_lazy('dashboard-staff')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_type'] = 'Staff'
        return context

class StaffDeleteView(StaffRequiredMixin, DeleteView):
    model = Staff
    template_name = 'records/record_confirm_delete.html'
    success_url = reverse_lazy('dashboard-staff')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_type'] = 'Staff'
        return context
