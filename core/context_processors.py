from .models import SiteSettings


def site_settings(request):
    """
    Makes the SiteSettings object available in ALL templates automatically.
    You can access it in any template as: {{ site_settings.school_name }}, etc.
    """
    return {
        'site_settings': SiteSettings.get_settings()
    }
