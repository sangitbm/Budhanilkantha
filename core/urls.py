from django.urls import path
from .views import (
    HomePageView, AboutView, ContactView, EventsView,
    AdmissionCreateView, DashboardAdmissionListView, DashboardAdmissionUpdateView, DashboardContactListView,
    teachers_view, staff_directory_view,
    dashboard_index_view, dashboard_settings_view, program_remove_view,
    DashboardTestimonialListView, TestimonialCreateView,
    TestimonialUpdateView, TestimonialDeleteView,
)

urlpatterns = [
    # Public Pages
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('events/', EventsView.as_view(), name='events'),
    path('admission/', AdmissionCreateView.as_view(), name='admissions'),
    
    # Directory
    path('directory/teachers/', teachers_view, name='teachers'),
    path('directory/staff/', staff_directory_view, name='staff-directory'),

    # Admin Dashboard
    path('dashboard/', dashboard_index_view, name='dashboard'),
    path('dashboard/admissions/', DashboardAdmissionListView.as_view(), name='dashboard-admissions'),

    path('dashboard/admissions/<int:pk>/update/', DashboardAdmissionUpdateView.as_view(), name='dashboard-admission-update'),
    path('dashboard/messages/', DashboardContactListView.as_view(), name='dashboard-messages'),
    path('dashboard/settings/', dashboard_settings_view, name='dashboard-settings'),
    path('dashboard/settings/programs/<int:pk>/remove/', program_remove_view, name='program-remove'),
    path('dashboard/testimonials/', DashboardTestimonialListView.as_view(), name='dashboard-testimonials'),
    path('dashboard/testimonials/add/', TestimonialCreateView.as_view(), name='testimonial-add'),
    path('dashboard/testimonials/<int:pk>/edit/', TestimonialUpdateView.as_view(), name='testimonial-edit'),
    path('dashboard/testimonials/<int:pk>/delete/', TestimonialDeleteView.as_view(), name='testimonial-delete'),
]
