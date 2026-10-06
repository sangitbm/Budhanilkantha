from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Student, Staff
from .forms import StudentForm, StaffForm

# --- Student Views ---
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'records/dashboard_student_list.html'
    context_object_name = 'students'
    login_url = '/admin/login/'
    ordering = ['grade', 'first_name']

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'records/record_form.html'
    success_url = reverse_lazy('dashboard-students')
    login_url = '/admin/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_type'] = 'Student'
        return context

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'records/record_form.html'
    success_url = reverse_lazy('dashboard-students')
    login_url = '/admin/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_type'] = 'Student'
        return context

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'records/record_confirm_delete.html'
    success_url = reverse_lazy('dashboard-students')
    login_url = '/admin/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_type'] = 'Student'
        return context


# --- Staff Views ---
class StaffListView(LoginRequiredMixin, ListView):
    model = Staff
    template_name = 'records/dashboard_staff_list.html'
    context_object_name = 'staff_members'
    login_url = '/admin/login/'
    ordering = ['staff_type', 'first_name']

class StaffCreateView(LoginRequiredMixin, CreateView):
    model = Staff
    form_class = StaffForm
    template_name = 'records/record_form.html'
    success_url = reverse_lazy('dashboard-staff')
    login_url = '/admin/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_type'] = 'Staff'
        return context

class StaffUpdateView(LoginRequiredMixin, UpdateView):
    model = Staff
    form_class = StaffForm
    template_name = 'records/record_form.html'
    success_url = reverse_lazy('dashboard-staff')
    login_url = '/admin/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_type'] = 'Staff'
        return context

class StaffDeleteView(LoginRequiredMixin, DeleteView):
    model = Staff
    template_name = 'records/record_confirm_delete.html'
    success_url = reverse_lazy('dashboard-staff')
    login_url = '/admin/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_type'] = 'Staff'
        return context
