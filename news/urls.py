from django.urls import path
from .views import DashboardNoticeListView, NoticeCreateView, NoticeListView, NoticeUpdateView, NoticeDeleteView, DashboardEventListView, EventCreateView, EventUpdateView, EventDeleteView, toggle_notice_ticker

urlpatterns = [
    path('', NoticeListView.as_view(), name='public-notices'),
    path('dashboard/notices/', DashboardNoticeListView.as_view(), name='dashboard-notices'),
    path('dashboard/notices/add/', NoticeCreateView.as_view(), name='add-notice'),
    
    # New URLs for updating and deleting
    path('dashboard/notices/<int:pk>/edit/', NoticeUpdateView.as_view(), name='edit-notice'),
    path('dashboard/notices/<int:pk>/delete/', NoticeDeleteView.as_view(), name='delete-notice'),
    path('dashboard/notices/<int:pk>/toggle-ticker/', toggle_notice_ticker, name='toggle-notice-ticker'),

    path('dashboard/events/', DashboardEventListView.as_view(), name='dashboard-events'),
    path('dashboard/events/add/', EventCreateView.as_view(), name='add-event'),
    path('dashboard/events/<int:pk>/edit/', EventUpdateView.as_view(), name='edit-event'),
    path('dashboard/events/<int:pk>/delete/', EventDeleteView.as_view(), name='delete-event'),
]
