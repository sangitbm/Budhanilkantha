from django.urls import path
from .views import (
    SessionListView,
    SessionCreateView,
    SessionUpdateView,
    SessionDeleteView,
    SetCurrentSessionView,
    DuplicateSessionView,
)

urlpatterns = [
    path('sessions/', SessionListView.as_view(), name='dashboard-sessions'),
    path('sessions/add/', SessionCreateView.as_view(), name='add-session'),
    path('sessions/<int:pk>/edit/', SessionUpdateView.as_view(), name='edit-session'),
    path('sessions/<int:pk>/delete/', SessionDeleteView.as_view(), name='delete-session'),
    path('sessions/<int:pk>/set-current/', SetCurrentSessionView.as_view(), name='set-current-session'),
    path('sessions/<int:pk>/duplicate/', DuplicateSessionView.as_view(), name='duplicate-session'),
]
