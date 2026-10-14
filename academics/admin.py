from django.contrib import admin
from .models import AcademicSession, Term, SchoolClass, Section


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


class SectionInline(admin.TabularInline):
    model = Section
    extra = 1


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'order', 'is_active')
    inlines = [SectionInline]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'school_class', 'capacity', 'is_active')

