from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages

from news.models import Notice
from gallery.models import Photo
from records.models import Student, Staff
from .models import AdmissionInquiry, SiteSettings, HeroImage
from .forms import AdmissionForm, SiteSettingsForm

class HomePageView(TemplateView):
    template_name = 'core/home.html'

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

@login_required(login_url='/admin/login/')
def dashboard_settings_view(request):
    settings_obj = SiteSettings.get_settings()

    if request.method == 'POST':
        # Handle hero image deletion
        delete_id = request.POST.get('delete_hero_image_id')
        if delete_id:
            try:
                hero_img = HeroImage.objects.get(id=delete_id, site_settings=settings_obj)
                hero_img.delete()
                messages.success(request, 'Hero image removed.')
            except HeroImage.DoesNotExist:
                pass
            return redirect('dashboard-settings')

        form = SiteSettingsForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            
            # Handle multiple hero images upload
            hero_images = request.FILES.getlist('hero_images')
            for img in hero_images:
                HeroImage.objects.create(site_settings=settings_obj, image=img)
                
            messages.success(request, '✅ Settings saved successfully!')
            return redirect('dashboard-settings')
        else:
            messages.error(request, '❌ Please fix the errors below.')
    else:
        form = SiteSettingsForm(instance=settings_obj)

    return render(request, 'core/dashboard_settings.html', {'form': form})
