from django.views.generic import ListView, DeleteView, View
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction, IntegrityError

from core.mixins import DashboardDeleteMixin
from core.templatetags.ui import bs_date
from .mixins import AcademicsAccessMixin
from .models import AcademicSession, Term
from .forms import AcademicSessionForm, make_term_formset
from .services import (
    set_current_session,
    duplicate_session,
    default_session_dates,
    suggest_terms,
    SessionOverlapError,
)


class SessionListView(AcademicsAccessMixin, ListView):
    model = AcademicSession
    template_name = 'academics/session_list.html'
    context_object_name = 'sessions'
    ordering = ['-start_date']

    def get_queryset(self):
        return super().get_queryset().prefetch_related('terms')


class SessionCreateView(AcademicsAccessMixin, View):
    template_name = 'academics/session_form.html'

    def get(self, request, *args, **kwargs):
        default_name, default_start, default_end = default_session_dates()
        form = AcademicSessionForm(initial={
            'name': default_name,
            'start_date': default_start,
            'end_date': default_end,
        })
        suggested = suggest_terms(default_start, default_end)
        formset_cls = make_term_formset(extra=3)
        formset = formset_cls(
            queryset=Term.objects.none(),
            prefix='terms',
            initial=suggested
        )
        context = {
            'form': form,
            'formset': formset,
            'is_edit': False,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = AcademicSessionForm(request.POST)
        formset_cls = make_term_formset(extra=0)
        formset = formset_cls(request.POST, prefix='terms')
        formset.session_form = form

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    session = form.save(commit=False)
                    session.save()
                    formset.instance = session
                    formset.save()
                    if form.cleaned_data.get('make_current'):
                        set_current_session(session)
                messages.success(request, f"Academic year {session.name} was created.")
                return redirect('dashboard-sessions')
            except IntegrityError:
                pass

        context = {
            'form': form,
            'formset': formset,
            'is_edit': False,
        }
        return render(request, self.template_name, context)


class SessionUpdateView(AcademicsAccessMixin, View):
    template_name = 'academics/session_form.html'

    def get(self, request, pk, *args, **kwargs):
        session = get_object_or_404(AcademicSession, pk=pk)
        form = AcademicSessionForm(instance=session)
        formset_cls = make_term_formset(extra=2)
        formset = formset_cls(instance=session, prefix='terms')
        context = {
            'form': form,
            'formset': formset,
            'session_obj': session,
            'is_edit': True,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        session = get_object_or_404(AcademicSession, pk=pk)
        form = AcademicSessionForm(request.POST, instance=session)
        formset_cls = make_term_formset(extra=0)
        formset = formset_cls(request.POST, instance=session, prefix='terms')
        formset.session_form = form

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    session = form.save(commit=False)
                    session.save()
                    formset.save()
                    if form.cleaned_data.get('make_current') and not session.is_current:
                        set_current_session(session)
                messages.success(request, f"Academic year {session.name} was updated.")
                return redirect('dashboard-sessions')
            except IntegrityError:
                pass

        context = {
            'form': form,
            'formset': formset,
            'session_obj': session,
            'is_edit': True,
        }
        return render(request, self.template_name, context)


class SessionDeleteView(AcademicsAccessMixin, DashboardDeleteMixin, DeleteView):
    model = AcademicSession
    success_url = reverse_lazy('dashboard-sessions')
    object_type = 'academic year'
    list_url_name = 'dashboard-sessions'
    list_label = 'Academic Years'
    impact = 'All of its terms are deleted too.'

    def _block_if_current(self, request):
        obj = self.get_object()
        if obj.is_current:
            messages.error(request, f"Set another year as current before deleting {obj.name}.")
            return redirect('dashboard-sessions')
        return None

    def get(self, request, *args, **kwargs):
        block = self._block_if_current(request)
        if block:
            return block
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        block = self._block_if_current(request)
        if block:
            return block
        return super().post(request, *args, **kwargs)

    def get_details(self, obj):
        term_count = obj.terms.count()
        return [
            ('Dates (AD)', f"{obj.start_date.strftime('%b %d, %Y')} – {obj.end_date.strftime('%b %d, %Y')}"),
            ('Dates (BS)', f"{bs_date(obj.start_date)} – {bs_date(obj.end_date)}"),
            ('Terms', f"{term_count} terms"),
        ]


class SetCurrentSessionView(AcademicsAccessMixin, View):
    def post(self, request, pk, *args, **kwargs):
        session = get_object_or_404(AcademicSession, pk=pk)
        set_current_session(session)
        messages.success(request, f"{session.name} is now the current academic year.")
        return redirect('dashboard-sessions')


class DuplicateSessionView(AcademicsAccessMixin, View):
    def post(self, request, pk, *args, **kwargs):
        session = get_object_or_404(AcademicSession, pk=pk)
        try:
            new_session = duplicate_session(session)
            term_count = new_session.terms.count()
            messages.success(request, f"Created {new_session.name} with {term_count} terms. Dates moved forward by one Nepali year.")
        except SessionOverlapError as e:
            messages.error(request, str(e))
        return redirect('dashboard-sessions')
