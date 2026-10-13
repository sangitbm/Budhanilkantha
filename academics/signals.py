from django.db.models.signals import post_delete, post_save
from django.core.cache import cache
from .models import AcademicSession, Term


def clear_current_session_cache(sender, instance, **kwargs):
    cache.delete('current_session')


def connect_signals():
    for model in (AcademicSession, Term):
        post_save.connect(
            clear_current_session_cache,
            sender=model,
            dispatch_uid=f"clear_current_session_cache_save_{model._meta.label}"
        )
        post_delete.connect(
            clear_current_session_cache,
            sender=model,
            dispatch_uid=f"clear_current_session_cache_delete_{model._meta.label}"
        )
