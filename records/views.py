from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.permissions import StaffRequiredMixin, staff_required
from core.mixins import DashboardDeleteMixin
from .models import Student, Staff
from .forms import StudentForm, StaffForm
from django.db.models import Q, F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
import csv
from django.utils import timezone
from academics.models import SchoolClass, Section

# --- Student Views ---
class StudentListView(StaffRequiredMixin, ListView):
    model = Student
    template_name = 'records/dashboard_student_list.html'
    context_object_name = 'students'
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset().select_related('school_class', 'section')
        qs = qs.order_by(
            F('school_class__order').asc(nulls_last=True),
            F('school_class__name').asc(nulls_last=True),
            'first_name',
            'last_name'
        )

        class_id = self.request.GET.get('class')
        selected_class = None
        if class_id:
            try:
                selected_class = SchoolClass.objects.filter(pk=int(class_id)).first()
            except (ValueError, TypeError):
                selected_class = None

        if selected_class:
            qs = qs.filter(school_class=selected_class)
            section_id = self.request.GET.get('section')
            if section_id:
                try:
                    selected_section = selected_class.sections.filter(pk=int(section_id), is_active=True).first()
                except (ValueError, TypeError):
                    selected_section = None
                if selected_section:
                    qs = qs.filter(section=selected_section)

        q = self.request.GET.get('q', '').strip()
        if q:
            terms = q.split()
            for term in terms:
                qs = qs.filter(
                    Q(first_name__icontains=term) |
                    Q(last_name__icontains=term) |
                    Q(roll_number__icontains=term) |
                    Q(guardian_name__icontains=term) |
                    Q(contact_number__icontains=term)
                )
        return qs.defer('date_of_birth', 'address')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '').strip()

        class_id = self.request.GET.get('class')
        selected_class = None
        sections = Section.objects.none()
        selected_section = None

        if class_id:
            try:
                selected_class = SchoolClass.objects.filter(pk=int(class_id)).first()
            except (ValueError, TypeError):
                selected_class = None

        if selected_class:
            sections = selected_class.sections.filter(is_active=True).order_by('name')
            section_id = self.request.GET.get('section')
            if section_id:
                try:
                    selected_section = sections.filter(pk=int(section_id)).first()
                except (ValueError, TypeError):
                    selected_section = None

        context['classes'] = SchoolClass.objects.filter(is_active=True).order_by('order', 'name')
        context['selected_class'] = selected_class
        context['sections'] = sections
        context['selected_section'] = selected_section
        context['total'] = self.get_queryset().count()
        return context

@staff_required
def export_students_csv(request):
    qs = Student.objects.select_related('school_class', 'section')

    class_id = request.GET.get('class')
    selected_class = None
    if class_id:
        try:
            selected_class = SchoolClass.objects.filter(pk=int(class_id)).first()
        except (ValueError, TypeError):
            selected_class = None

    if selected_class:
        qs = qs.filter(school_class=selected_class)
        section_id = request.GET.get('section')
        if section_id:
            try:
                selected_section = selected_class.sections.filter(pk=int(section_id), is_active=True).first()
            except (ValueError, TypeError):
                selected_section = None
            if selected_section:
                qs = qs.filter(section=selected_section)

    q = request.GET.get('q', '').strip()
    if q:
        terms = q.split()
        for term in terms:
            qs = qs.filter(
                Q(first_name__icontains=term) |
                Q(last_name__icontains=term) |
                Q(roll_number__icontains=term) |
                Q(guardian_name__icontains=term) |
                Q(contact_number__icontains=term)
            )

    qs = qs.order_by(
        F('school_class__order').asc(nulls_last=True),
        F('school_class__name').asc(nulls_last=True),
        'first_name',
        'last_name'
    )

    response = HttpResponse(content_type='text/csv')
    filename = f"students-{timezone.localdate().strftime('%Y-%m-%d')}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['Roll no', 'First name', 'Last name', 'Gender', 'Class', 'Section', 'Guardian', 'Contact'])

    for student in qs:
        class_name = student.school_class.name if student.school_class else (student.grade or "")
        section_name = student.section.name if student.section else ""
        row = [
            student.roll_number,
            student.first_name,
            student.last_name,
            student.gender,
            class_name,
            section_name,
            student.guardian_name,
            student.contact_number
        ]
        safe_row = []
        for cell in row:
            cell_str = str(cell) if cell is not None else ""
            if cell_str.startswith(('=', '+', '-', '@')):
                cell_str = "'" + cell_str
            safe_row.append(cell_str)
        writer.writerow(safe_row)

    return response

class StudentCreateView(StaffRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'records/student_form.html'
    success_url = reverse_lazy('dashboard-students')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_type'] = 'Student'
        return context

class StudentUpdateView(StaffRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'records/student_form.html'
    success_url = reverse_lazy('dashboard-students')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_type'] = 'Student'
        return context

class StudentDeleteView(DashboardDeleteMixin, DeleteView):
    model = Student
    success_url = reverse_lazy('dashboard-students')
    object_type = 'student'
    list_url_name = 'dashboard-students'
    list_label = 'Students'
    impact = "This student's record is permanently deleted."

    def get_details(self, obj):
        if obj.school_class and obj.section:
            class_str = f"{obj.school_class.name} - {obj.section.name}"
        elif obj.school_class:
            class_str = obj.school_class.name
        else:
            class_str = obj.grade or ""

        details = [
            ('Class', class_str),
            ('Roll Number', obj.roll_number),
            ('Guardian', obj.guardian_name),
        ]
        return details

    def get_thumbnail_url(self, obj):
        return obj.photo.url if obj.photo else None


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

class StaffDeleteView(DashboardDeleteMixin, DeleteView):
    model = Staff
    success_url = reverse_lazy('dashboard-staff')
    object_type = 'staff'
    list_url_name = 'dashboard-staff'
    list_label = 'Staff'
    impact = "They will be removed from the public staff directory and the dashboard."

    def get_object_label(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_details(self, obj):
        return [
            ('Designation', obj.designation),
            ('Department', obj.department),
        ]

@staff_required
@require_POST
def staff_deactivate(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    staff.is_active = False
    staff.save()
    messages.success(request, f"Staff '{staff.first_name} {staff.last_name}' was made inactive.")
    return redirect('dashboard-staff')
