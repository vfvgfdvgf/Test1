from .models import Notification
from django.utils import timezone
from django.db.models import Q  # ✅ أضف هذا

def active_notifications(request):
    notifications = Notification.objects.filter(is_active=True).filter(
        Q(end_date__gte=timezone.now()) | Q(end_date__isnull=True)
    )
    return {'notifications': notifications}
from .models import SiteSettings

def site_settings(request):
    settings = SiteSettings.objects.first()
    return {"site_settings": settings}
