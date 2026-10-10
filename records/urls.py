from django.urls import path
from .views import (
    StudentListView, StudentCreateView, StudentUpdateView, StudentDeleteView,
    export_students_csv,
    StaffListView, StaffCreateView, StaffUpdateView, StaffDeleteView, staff_deactivate
)

urlpatterns = [
    path('dashboard/students/', StudentListView.as_view(), name='dashboard-students'),
    path('dashboard/students/add/', StudentCreateView.as_view(), name='add-student'),
    path('dashboard/students/edit/<int:pk>/', StudentUpdateView.as_view(), name='edit-student'),
    path('dashboard/students/delete/<int:pk>/', StudentDeleteView.as_view(), name='delete-student'),
    path('dashboard/students/export/', export_students_csv, name='students-export'),
    
    path('dashboard/staff/', StaffListView.as_view(), name='dashboard-staff'),
    path('dashboard/staff/add/', StaffCreateView.as_view(), name='add-staff'),
    path('dashboard/staff/edit/<int:pk>/', StaffUpdateView.as_view(), name='edit-staff'),
    path('dashboard/staff/delete/<int:pk>/', StaffDeleteView.as_view(), name='delete-staff'),
    path('dashboard/staff/deactivate/<int:pk>/', staff_deactivate, name='staff-deactivate'),
]
