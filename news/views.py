from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.permissions import StaffRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Notice
from .forms import NoticeForm

class DashboardNoticeListView(StaffRequiredMixin, ListView):
    model = Notice
    template_name = 'news/dashboard_notice_list.html'
    context_object_name = 'notices'
    ordering = ['-created_at']

class NoticeCreateView(StaffRequiredMixin, CreateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'news/notice_form.html'
    success_url = reverse_lazy('dashboard-notices')

class NoticeUpdateView(StaffRequiredMixin, UpdateView):
    model = Notice
    form_class = NoticeForm
    # We can reuse the exact same form template we use for creating!
    template_name = 'news/notice_form.html'
    success_url = reverse_lazy('dashboard-notices')


class NoticeListView(ListView):
    model = Notice
    template_name = 'news/public_notice_list.html'
    context_object_name = 'notices'
    ordering = ['-created_at']

class NoticeDeleteView(StaffRequiredMixin, DeleteView):
    model = Notice
    template_name = 'news/notice_confirm_delete.html'
    success_url = reverse_lazy('dashboard-notices')