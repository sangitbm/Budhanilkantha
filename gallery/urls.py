from django.urls import path
from .views import GalleryListView, PhotoCreateView, DashboardGalleryListView, PhotoUpdateView, PhotoDeleteView

urlpatterns = [
    # Public route
    path('', GalleryListView.as_view(), name='gallery'),
    
    # Admin routes
    path('dashboard/photos/', DashboardGalleryListView.as_view(), name='dashboard-gallery'),
    path('dashboard/photos/upload/', PhotoCreateView.as_view(), name='add-photo'),
    path('dashboard/photos/<int:pk>/edit/', PhotoUpdateView.as_view(), name='edit-photo'),
    path('dashboard/photos/<int:pk>/delete/', PhotoDeleteView.as_view(), name='delete-photo'),
]
