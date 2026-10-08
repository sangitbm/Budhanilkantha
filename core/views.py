from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.contrib import messages

from news.models import Notice
from gallery.models import Photo
from records.models import Student, Staff
from .models import AdmissionInquiry, SiteSettings, HeroImage, AcademicProgram
from .forms import AdmissionForm, SiteSettingsForm

class HomePageView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testimonials'] = Testimonial.objects.filter(is_published=True).order_by('order', '-created_at')[:3]
        return context

class AboutView(TemplateView):
    template_name = 'core/about.html'

class ContactView(TemplateView):
    template_name = 'core/contact.html'

class EventsView(TemplateView):
    template_name = 'core/events.html'

class AdmissionCreateView(CreateView):
    model = AdmissionInquiry
    form_class = AdmissionForm
    template_name = 'core/admission_form.html'
    success_url = reverse_lazy('home')

class DashboardAdmissionListView(LoginRequiredMixin, ListView):
    model = AdmissionInquiry
    template_name = 'core/dashboard_admission_list.html'
    context_object_name = 'applications'  
    ordering = ['-submitted_at'] 

def teachers_view(request):
    context = {
        'teachers': Staff.objects.filter(staff_type='TEACHER', is_active=True).order_by('first_name')
    }
    return render(request, 'core/teachers.html', context)


def staff_directory_view(request):
    context = {
        'staff_members': Staff.objects.filter(is_active=True).order_by('staff_type', 'first_name')
    }
    return render(request, 'core/staff_directory.html', context)


@login_required(login_url='/admin/login/')
def dashboard_index_view(request):
    context = {
        'notices_count': Notice.objects.count(),
        'photos_count': Photo.objects.count(),
        'students_count': Student.objects.count(),
        'staff_count': Staff.objects.count()
    }
    return render(request, 'core/dashboard_index.html', context)

from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden


ALLOWED_TABS = ['school', 'about', 'programs', 'contact', 'social', 'admissions', 'advanced']
ALL_GRADES = ['ECD', 'Nursery', 'LKG', 'UKG', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6', 'Grade 7', 'Grade 8', 'Grade 9', 'Grade 10', 'Grade 11', 'Grade 12']
FIELD_TO_TAB = {
    'school_name': 'school', 'school_short_name': 'school', 'marquee_text': 'school', 'ticker_enabled': 'school', 'tagline': 'school',
    'established_year': 'school', 'principal_name': 'school', 'principal_photo': 'school', 'principal_message': 'school',
    'about_short': 'school', 'logo': 'school', 'favicon': 'school',
    'about_image': 'about', 'about_text': 'about', 'curriculum_text': 'about',
    'value_1': 'about', 'value_2': 'about', 'value_3': 'about',
    'stat_students': 'about', 'stat_faculty': 'about', 'stat_support': 'about',
    'phone_primary': 'contact', 'phone_secondary': 'contact', 'email_general': 'contact', 'email_admissions': 'contact',
    'address': 'contact', 'google_maps_url': 'contact', 'office_hours': 'contact',
    'facebook_url': 'social', 'youtube_url': 'social', 'twitter_url': 'social', 'instagram_url': 'social', 'whatsapp_url': 'social',
    'admissions_open': 'admissions', 'admissions_btn_label': 'admissions', 'admissions_btn_link': 'admissions',
    'admissions_badge': 'admissions', 'admissions_start': 'admissions', 'admissions_end': 'admissions', 'admissions_message': 'admissions',
    'meta_description': 'advanced', 'og_title': 'advanced', 'og_image': 'advanced', 'maintenance_mode': 'advanced'
}

@login_required(login_url='/admin/login/')
def program_remove_view(request, pk):

    if not request.user.is_staff:
        return HttpResponseForbidden("Not allowed.")
    
    settings_obj = SiteSettings.get_settings()
    program = get_object_or_404(AcademicProgram, pk=pk, site_settings=settings_obj)
    
    if request.method == 'POST':
        title = program.title
        program.delete()
        messages.success(request, f"Program '{title}' removed.")
        return redirect(reverse('dashboard-settings') + '?tab=programs')
        
    return render(request, 'core/confirm_remove_program.html', {'program': program})

@login_required(login_url='/admin/login/')
def dashboard_settings_view(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Not allowed.")
        
    settings_obj = SiteSettings.get_settings()
    active_tab = request.GET.get('tab', 'school')

    if request.method == 'POST':
        active_tab = request.POST.get('settings_tab', request.POST.get('tab', active_tab))
        if active_tab and active_tab.startswith('tab_'):
            active_tab = active_tab[4:]
        if active_tab not in ALLOWED_TABS:
            active_tab = 'school'

        # Handle hero image deletion
        delete_id = request.POST.get('delete_hero_image_id')
        if delete_id:
            try:
                hero_img = HeroImage.objects.get(id=delete_id, site_settings=settings_obj)
                hero_img.delete()
                messages.success(request, 'Hero image removed.')
            except HeroImage.DoesNotExist:
                pass
            return redirect(reverse('dashboard-settings') + f'?tab={active_tab}')

        # Handle Academic Program deletion redirect
        delete_prog_id = request.POST.get('delete_program_id')
        if delete_prog_id:
            if not request.user.is_staff:
                return HttpResponseForbidden("Not allowed.")
            return redirect('program-remove', pk=delete_prog_id)

        form = SiteSettingsForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.open_grades = request.POST.getlist('open_grades')
            obj.save()
            
            hero_images = request.FILES.getlist('hero_images')
            for img in hero_images:
                HeroImage.objects.create(site_settings=settings_obj, image=img)
                
            # Handle Academic Programs
            prog_ids = request.POST.getlist('program_id')
            prog_titles = request.POST.getlist('program_title')
            prog_descs = request.POST.getlist('program_desc')
            
            for i in range(len(prog_titles)):
                p_id = prog_ids[i] if i < len(prog_ids) else ''
                p_title = prog_titles[i].strip()
                p_desc = prog_descs[i].strip() if i < len(prog_descs) else ''
                
                if p_id:
                    try:
                        prog = AcademicProgram.objects.get(id=p_id, site_settings=settings_obj)
                        prog.title = p_title
                        prog.description = p_desc
                        prog.order = i
                        prog.save()
                    except AcademicProgram.DoesNotExist:
                        pass
                elif p_title:
                    # Create new
                    AcademicProgram.objects.create(
                        site_settings=settings_obj,
                        title=p_title,
                        description=p_desc,
                        order=i
                    )
                
            messages.success(request, '✅ Settings saved successfully!')
            return redirect(reverse('dashboard-settings') + f'?tab={active_tab}')
        else:
            messages.error(request, '❌ Please fix the errors below.')
            # Find the first error and switch to its tab
            for field in form.errors:
                if field in FIELD_TO_TAB:
                    active_tab = FIELD_TO_TAB[field]
                    break
                    
    else:
        form = SiteSettingsForm(instance=settings_obj)

    # Compute error counts per tab for the UI indicator
    tab_errors = {tab: 0 for tab in ALLOWED_TABS}
    if hasattr(form, 'errors') and form.errors:
        for field in form.errors:
            if field in FIELD_TO_TAB:
                tab_errors[FIELD_TO_TAB[field]] += 1

    if active_tab and active_tab.startswith('tab_'):
        active_tab = active_tab[4:]
    if active_tab not in ALLOWED_TABS:
        active_tab = 'school'

    programs = list(settings_obj.academic_programs.all())
    # Always append one empty program slot for the UI
    programs.append({'id': '', 'title': '', 'description': ''})

    grouped_grades = [
        ("Early Childhood", [g for g in ALL_GRADES if g in ['ECD', 'Nursery', 'LKG', 'UKG']]),
        ("Primary", [g for g in ALL_GRADES if g in ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5']]),
        ("Lower Secondary", [g for g in ALL_GRADES if g in ['Grade 6', 'Grade 7', 'Grade 8']]),
        ("Secondary", [g for g in ALL_GRADES if g in ['Grade 9', 'Grade 10']]),
        ("+2", [g for g in ALL_GRADES if g in ['Grade 11', 'Grade 12']]),
    ]
    
    active_ticker_count = Notice.objects.filter(show_in_ticker=True).count()
    
    return render(request, 'core/dashboard_settings.html', {
        'form': form,
        'all_grades': ALL_GRADES,
        'grouped_grades': grouped_grades,
        'active_tab': active_tab,
        'tab_errors': tab_errors,
        'programs': programs,
        'active_ticker_count': min(5, active_ticker_count),
    })

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
