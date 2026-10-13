from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from core.permissions import StaffRequiredMixin, staff_required
from core.mixins import DashboardDeleteMixin
from django.contrib import messages
from news.models import Notice, Event
from gallery.models import Photo
from records.models import Student, Staff
from .models import AdmissionInquiry, SiteSettings, HeroImage, AcademicProgram
from .forms import AdmissionForm, SiteSettingsForm
from .forms import ContactMessageForm
from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from .forms import AcademicProgramForm
from core.constants import ALLOWED_TABS, ALL_GRADES, FIELD_TO_TAB, GROUPED_GRADES
from .models import Testimonial
from .forms import TestimonialForm
from .forms import AdmissionStaffForm
from .models import ContactMessage

class HomePageView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testimonials'] = Testimonial.objects.filter(is_published=True).order_by('order', '-created_at')[:3]
        return context

class AboutView(TemplateView):
    template_name = 'core/about.html'


class ContactView(CreateView):
    template_name = 'core/contact.html'
    form_class = ContactMessageForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        messages.success(self.request, "Your message has been sent successfully. We will get back to you soon.")
        return super().form_valid(form)



class EventsView(ListView):
    template_name = 'core/events.html'
    model = Event
    context_object_name = 'events'
    
    def get_queryset(self):
        today = timezone.localdate()
        return Event.objects.filter(Q(event_date__gte=today) | Q(event_date__isnull=True)).order_by(
            F('event_date').asc(nulls_last=True), 
            F('start_time').asc(nulls_last=True), 
            'title'
        )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        context['past_events'] = Event.objects.filter(event_date__lt=today).order_by('-event_date', '-start_time')[:10]
        return context


class AdmissionCreateView(CreateView):
    model = AdmissionInquiry
    form_class = AdmissionForm
    template_name = 'core/admission_form.html'
    success_url = reverse_lazy('home')



class DashboardAdmissionListView(StaffRequiredMixin, ListView):
    model = AdmissionInquiry
    template_name = 'core/dashboard_admission_list.html'
    context_object_name = 'applications'  
    ordering = ['-submitted_at']
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        status = self.request.GET.get('status')
        grade = self.request.GET.get('grade')
        
        if query:
            queryset = queryset.filter(
                Q(student_name__icontains=query) |
                Q(parent_name__icontains=query) |
                Q(email__icontains=query) |
                Q(phone_number__icontains=query)
            )
        if status:
            queryset = queryset.filter(status=status)
        if grade:
            queryset = queryset.filter(grade_applying_for__icontains=grade)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['status'] = self.request.GET.get('status', '')
        context['grade'] = self.request.GET.get('grade', '')
        context['statuses'] = AdmissionInquiry.STATUS_CHOICES
        return context

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



@staff_required
def dashboard_index_view(request):
    today = timezone.now().date()
    recent_admissions = AdmissionInquiry.objects.all().order_by('-submitted_at')[:5]
    upcoming_events = Event.objects.filter(Q(event_date__gte=today) | Q(event_date__isnull=True)).order_by('event_date', 'start_time')[:5]
    recent_notices = Notice.objects.all().order_by('-created_at')[:5]

    context = {
        'notices_count': Notice.objects.count(),
        'photos_count': Photo.objects.count(),
        'students_count': Student.objects.count(),
        'staff_count': Staff.objects.count(),
        'recent_admissions': recent_admissions,
        'upcoming_events': upcoming_events,
        'recent_notices': recent_notices,
    }
    return render(request, 'core/dashboard_index.html', context)





def normalize_tab(raw):
    if raw and raw.startswith('tab_'):
        raw = raw[4:]
    if raw not in ALLOWED_TABS:
        return 'school'
    return raw

def save_hero_images(settings_obj, files):
    for img in files:
        HeroImage.objects.create(site_settings=settings_obj, image=img)

def handle_hero_delete(request, settings_obj):
    delete_id = request.POST.get('delete_hero_image_id')
    if delete_id:
        try:
            hero_img = HeroImage.objects.get(id=delete_id, site_settings=settings_obj)
            hero_img.delete()
            messages.success(request, 'Hero image removed.')
            return True
        except HeroImage.DoesNotExist:
            pass
    return False

def build_tab_errors(form, prog_forms=None):
    tab_errors = {tab: 0 for tab in ALLOWED_TABS}
    if hasattr(form, 'errors') and form.errors:
        for field in form.errors:
            if field in FIELD_TO_TAB:
                tab_errors[FIELD_TO_TAB[field]] += 1
    if prog_forms:
        for pform in prog_forms:
            if pform.errors:
                tab_errors['programs'] += 1
    return tab_errors

@staff_required
def program_remove_view(request, pk):
    settings_obj = SiteSettings.get_settings()
    program = get_object_or_404(AcademicProgram, pk=pk, site_settings=settings_obj)
    
    if request.method == 'POST':
        title = program.title
        program.delete()
        messages.success(request, f'Program "{title}" was deleted.')
        return redirect(reverse('dashboard-settings') + '?tab=programs')
        
    context = {
        'object_type': 'program',
        'object_label': program.title,
        'details': [('Title', program.title)],
        'impact': 'It will be removed from the Programs section of the home page.',
        'cancel_url': reverse('dashboard-settings') + '?tab=programs',
        'cancel_label': 'Settings',
    }
    return render(request, 'includes/dashboard_delete_shell.html', context)

@staff_required
def dashboard_settings_view(request):
    settings_obj = SiteSettings.get_settings()
    active_tab = normalize_tab(request.GET.get('tab', 'school'))
    
    if request.method == 'POST':
        active_tab = normalize_tab(request.POST.get('settings_tab', request.POST.get('tab', active_tab)))
        
        if handle_hero_delete(request, settings_obj):
            return redirect(reverse('dashboard-settings') + f'?tab={active_tab}')
            
        delete_prog_id = request.POST.get('delete_program_id')
        if delete_prog_id:
            return redirect('program-remove', pk=delete_prog_id)
            
        form = SiteSettingsForm(request.POST, request.FILES, instance=settings_obj)
        
        prog_ids = request.POST.getlist('program_id')
        prog_titles = request.POST.getlist('program_title')
        prog_descs = request.POST.getlist('program_desc')
        
        prog_forms = []
        seen_titles = set()
        programs_valid = True
        
        for i in range(len(prog_titles)):
            p_id = prog_ids[i] if i < len(prog_ids) else ''
            p_title = prog_titles[i].strip()
            p_desc = prog_descs[i].strip() if i < len(prog_descs) else ''
            
            if not p_title and not p_desc and not p_id:
                continue
                
            data = {'title': p_title, 'description': p_desc, 'order': i}
            instance = None
            if p_id:
                try:
                    instance = AcademicProgram.objects.get(id=p_id, site_settings=settings_obj)
                except AcademicProgram.DoesNotExist:
                    pass
                
            pform = AcademicProgramForm(data, instance=instance)
            prog_forms.append(pform)
            
            if not pform.is_valid():
                programs_valid = False
            elif p_title.lower() in seen_titles:
                pform.add_error('title', 'Duplicate title.')
                programs_valid = False
            else:
                seen_titles.add(p_title.lower())
                
        if form.is_valid() and programs_valid:
            form.save()
            save_hero_images(settings_obj, request.FILES.getlist('hero_images'))
            
            for pform in prog_forms:
                p = pform.save(commit=False)
                p.site_settings = settings_obj
                p.save()
                
            messages.success(request, 'Settings saved successfully!')
            return redirect(reverse('dashboard-settings') + f'?tab={active_tab}')
        else:
            messages.error(request, 'Please fix the errors below.')
            tab_errors = build_tab_errors(form, prog_forms)
            for tab, err_count in tab_errors.items():
                if err_count > 0:
                    active_tab = tab
                    break
    else:
        form = SiteSettingsForm(instance=settings_obj)
        prog_forms = [AcademicProgramForm(instance=p) for p in settings_obj.academic_programs.all()]

    tab_errors = build_tab_errors(form, prog_forms if request.method == 'POST' else None)
    
    programs = []
    if request.method == 'POST':
        for pf in prog_forms:
            programs.append({
                'id': pf.instance.id,
                'title': pf.data.get('title', ''),
                'description': pf.data.get('description', ''),
                'errors': pf.errors
            })
    else:
        for p in settings_obj.academic_programs.all():
            programs.append({
                'id': p.id,
                'title': p.title,
                'description': p.description,
            })
            
    active_ticker_count = Notice.objects.filter(show_in_ticker=True).count()
    
    return render(request, 'core/dashboard_settings.html', {
        'form': form,
        'active_tab': active_tab,
        'tab_errors': tab_errors,
        'programs': programs,
        'blank_program': {'id': '', 'title': '', 'description': ''},
        'active_ticker_count': min(5, active_ticker_count),
        'all_grades': ALL_GRADES,
        'grouped_grades': GROUPED_GRADES,
    })


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

class TestimonialDeleteView(DashboardDeleteMixin, DeleteView):
    model = Testimonial
    success_url = reverse_lazy('dashboard-testimonials')
    object_type = 'testimonial'
    list_url_name = 'dashboard-testimonials'
    list_label = 'Testimonials'
    impact = 'It will be removed from the home page.'

    def get_details(self, obj):
        q = obj.quote
        if len(q) > 120:
            q = q[:117] + '...'
        return [
            ('Quote', f'"{q}"'),
            ('By', f'{obj.name} ({obj.role})'),
        ]

    def get_thumbnail_url(self, obj):
        return obj.photo.url if obj.photo else None



class DashboardAdmissionUpdateView(StaffRequiredMixin, UpdateView):
    model = AdmissionInquiry
    form_class = AdmissionStaffForm
    template_name = 'core/dashboard_admission_form.html'
    success_url = reverse_lazy('dashboard-admissions')

    def form_valid(self, form):
        messages.success(self.request, "Admission status updated successfully.")
        return super().form_valid(form)



class DashboardContactListView(StaffRequiredMixin, ListView):
    model = ContactMessage
    template_name = 'core/dashboard_contact_list.html'
    context_object_name = 'messages'
    ordering = ['-submitted_at']
    paginate_by = 20
