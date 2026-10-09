from django.contrib import admin
from news.models import Notice, Event

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'show_in_ticker')
    search_fields = ('title', 'description')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'location')
    search_fields = ('title', 'description', 'location')

