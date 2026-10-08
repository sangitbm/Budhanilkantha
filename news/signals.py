from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Notice

@receiver(post_save, sender=Notice)
@receiver(post_delete, sender=Notice)
def invalidate_notice_cache(sender, instance, **kwargs):
    cache.delete('ticker_notices')
