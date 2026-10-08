from .models import SiteSettings
from django.core.cache import cache
from news.models import Notice

def site_settings(request):
    """
    Makes the SiteSettings object available in ALL templates automatically.
    You can access it in any template as: {{ site_settings.school_name }}, etc.
    """
    settings = SiteSettings.objects.prefetch_related('academic_programs', 'hero_images').first()
    if not settings:
        settings = SiteSettings.get_settings()
    return {
        'site_settings': settings
    }

def latest_notices(request):
    settings_obj = SiteSettings.get_settings()
    
    if not settings_obj.ticker_enabled:
        return {'ticker_notices': [], 'ticker_duration': 20}
        
    notices = cache.get('ticker_notices')
    if notices is None:
        notices = list(Notice.objects.filter(show_in_ticker=True).only('id', 'title', 'created_at').order_by('-created_at')[:5])
        cache.set('ticker_notices', notices, 60)
        
    has_marquee = bool(settings_obj.marquee_text)
    
    num_items = len(notices) + (1 if has_marquee else 0)
    ticker_duration = max(20, 8 * num_items)
    
    return {
        'ticker_notices': notices,
        'ticker_duration': ticker_duration
    }
