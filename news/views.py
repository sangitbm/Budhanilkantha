from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Notice
from .forms import NoticeForm

class DashboardNoticeListView(LoginRequiredMixin, ListView):
    model = Notice
    template_name = 'news/dashboard_notice_list.html'
    context_object_name = 'notices'
    login_url = '/admin/login/'
    ordering = ['-created_at']

class NoticeCreateView(LoginRequiredMixin, CreateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'news/notice_form.html'
    success_url = reverse_lazy('dashboard-notices')
    login_url = '/admin/login/'

class NoticeUpdateView(LoginRequiredMixin, UpdateView):
    model = Notice
    form_class = NoticeForm
    # We can reuse the exact same form template we use for creating!
    template_name = 'news/notice_form.html'
    success_url = reverse_lazy('dashboard-notices')
    login_url = '/admin/login/'


class NoticeListView(ListView):
    model = Notice
    template_name = 'news/public_notice_list.html'
    context_object_name = 'notices'
    ordering = ['-created_at']

class NoticeDeleteView(LoginRequiredMixin, DeleteView):
    model = Notice
    template_name = 'news/notice_confirm_delete.html'
    success_url = reverse_lazy('dashboard-notices')
    login_url = '/admin/login/'