import re

# Patch URLs
urls_path = r'c:\Users\sangi\Desktop\budhanilkantha_school\core\urls.py'
with open(urls_path, 'r', encoding='utf-8') as f:
    urls_content = f.read()

if 'program_remove_view' not in urls_content:
    urls_content = urls_content.replace("dashboard_settings_view", "dashboard_settings_view, program_remove_view")

path_str = "    path('dashboard/settings/programs/<int:pk>/remove/', program_remove_view, name='program-remove'),\n"
if "name='program-remove'" not in urls_content:
    urls_content = urls_content.replace(
        "    path('dashboard/settings/', dashboard_settings_view, name='dashboard-settings'),\n",
        "    path('dashboard/settings/', dashboard_settings_view, name='dashboard-settings'),\n" + path_str
    )

with open(urls_path, 'w', encoding='utf-8') as f:
    f.write(urls_content)


# Patch Views
views_path = r'c:\Users\sangi\Desktop\budhanilkantha_school\core\views.py'
with open(views_path, 'r', encoding='utf-8') as f:
    views_content = f.read()

before_func = views_content.split("@login_required(login_url='/admin/login/')\ndef dashboard_settings_view")[0]

clean_func = """from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

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
    settings_obj = SiteSettings.get_settings()
    active_tab = request.GET.get('tab', 'school')

    if request.method == 'POST':
        active_tab = request.POST.get('tab', active_tab)
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

    if active_tab not in ALLOWED_TABS:
        active_tab = 'school'

    programs = list(settings_obj.academic_programs.all())
    # Always append one empty program slot for the UI
    programs.append({'id': '', 'title': '', 'description': ''})

    return render(request, 'core/dashboard_settings.html', {
        'form': form,
        'all_grades': ALL_GRADES,
        'active_tab': active_tab,
        'tab_errors': tab_errors,
        'programs': programs,
    })
"""
with open(views_path, 'w', encoding='utf-8') as f:
    f.write(before_func + clean_func)

print("urls and views updated.")
