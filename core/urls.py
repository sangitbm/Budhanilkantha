from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    HomePageView, AboutView, ContactView,
    EventsView, AdmissionCreateView, DashboardAdmissionListView,
    # These are our new functions:
    teachers_view, staff_directory_view, dashboard_index_view,
    dashboard_settings_view
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    
    # Faculty & Events Routes
    # Notice .as_view() is removed for the function-based ones
    path('faculty/teachers/', teachers_view, name='teachers'),
    path('faculty/staff-directory/', staff_directory_view, name='staff-directory'),
    path('events/', EventsView.as_view(), name='events'),

    # Admin Dashboard Routes
    path('dashboard/', dashboard_index_view, name='dashboard'),
    path('dashboard/settings/', dashboard_settings_view, name='dashboard-settings'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    # Admission Route
    path('admission/', AdmissionCreateView.as_view(), name='admissions'),
    path('dashboard/admissions/', DashboardAdmissionListView.as_view(), name='dashboard-admissions'),
]
