from django.contrib import admin
from .models import AcademicSession, Term


class TermInline(admin.TabularInline):
    model = Term
    extra = 0


@admin.register(AcademicSession)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_current')
    inlines = [TermInline]


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'session', 'start_date', 'end_date', 'order')
