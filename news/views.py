from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.permissions import StaffRequiredMixin, staff_required
from core.mixins import DashboardDeleteMixin
from django.urls import reverse_lazy
from .models import Notice
from .forms import NoticeForm
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme

class DashboardNoticeListView(StaffRequiredMixin, ListView):
    model = Notice
    template_name = 'news/dashboard_notice_list.html'
    context_object_name = 'notices'
    ordering = ['-created_at']
    paginate_by = 15

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '').strip()
        context['q'] = q
        if q:
            context['match_count'] = self.get_queryset().count()
        return context

@staff_required
@require_POST
def toggle_notice_ticker(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    notice.show_in_ticker = not notice.show_in_ticker
    notice.save()
    if notice.show_in_ticker:
        messages.success(request, f"Notice '{notice.title}' is now shown on the ticker.")
    else:
        messages.success(request, f"Notice '{notice.title}' is now hidden from the ticker.")
    next_url = request.POST.get('next')
    if next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect('dashboard-notices')

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

class NoticeDeleteView(DashboardDeleteMixin, DeleteView):
    model = Notice
    success_url = reverse_lazy('dashboard-notices')
    object_type = 'notice'
    list_url_name = 'dashboard-notices'
    list_label = 'Notices'
    impact = 'It will be removed from the public Notices page and from the scrolling bar.'

    def get_details(self, obj):
        details = [
            ('Posted', obj.created_at.strftime('%b %d, %Y')),
            ('On ticker', 'Yes' if obj.show_in_ticker else 'No'),
        ]
        if obj.file_attachment:
            import os
            details.append(('Attachment', os.path.basename(obj.file_attachment.name)))
        return details

from .models import Event
from .forms import EventForm

class DashboardEventListView(StaffRequiredMixin, ListView):
    model = Event
    template_name = 'news/dashboard_event_list.html'
    context_object_name = 'events'
    ordering = ['-start_time']
    paginate_by = 20

class EventCreateView(StaffRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'news/event_form.html'
    success_url = reverse_lazy('dashboard-events')

class EventUpdateView(StaffRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'news/event_form.html'
    success_url = reverse_lazy('dashboard-events')

class EventDeleteView(DashboardDeleteMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('dashboard-events')
    object_type = 'event'
    list_url_name = 'dashboard-events'
    list_label = 'Events'
    impact = 'It will be removed from the public Events page.'

    def get_details(self, obj):
        details = []
        if obj.event_date:
            details.append(('Date', obj.event_date.strftime('%b %d, %Y')))
        else:
            details.append(('Date', 'No date set'))
        if obj.start_time:
            time_str = obj.start_time.strftime('%I:%M %p')
            if obj.end_time:
                time_str += f" - {obj.end_time.strftime('%I:%M %p')}"
            details.append(('Time', time_str))
        if obj.location:
            details.append(('Location', obj.location))
        return details
