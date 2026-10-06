from django.urls import path
from .views import DashboardNoticeListView, NoticeCreateView, NoticeListView, NoticeUpdateView, NoticeDeleteView

urlpatterns = [
    path('', NoticeListView.as_view(), name='public-notices'),
    path('dashboard/notices/', DashboardNoticeListView.as_view(), name='dashboard-notices'),
    path('dashboard/notices/add/', NoticeCreateView.as_view(), name='add-notice'),
    
    # New URLs for updating and deleting
    path('dashboard/notices/<int:pk>/edit/', NoticeUpdateView.as_view(), name='edit-notice'),
    path('dashboard/notices/<int:pk>/delete/', NoticeDeleteView.as_view(), name='delete-notice'),
]
