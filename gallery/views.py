from django.shortcuts import render
from .models import Photo
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import PhotoForm

class GalleryListView(ListView):
    model = Photo
    template_name = 'gallery_list.html'
    context_object_name = 'photos'
    ordering = ['-uploaded_at'] 

class DashboardGalleryListView(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'gallery/dashboard_gallery_list.html'
    context_object_name = 'photos'
    ordering = ['-uploaded_at']
    login_url = '/admin/login/'

class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photo_form.html'
    success_url = reverse_lazy('gallery')
    login_url = '/admin/login/'

class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'gallery/photo_form.html'
    success_url = reverse_lazy('dashboard-gallery')
    login_url = '/admin/login/'

class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    template_name = 'gallery/photo_confirm_delete.html'
    success_url = reverse_lazy('dashboard-gallery')
    login_url = '/admin/login/'