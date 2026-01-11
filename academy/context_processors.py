from .models import *
from django.utils.timezone import now
from django.utils import timezone

def active_cohort_alert(request):
    alert = CohortAlert.objects.filter(is_active=True, start_date__gte=now().date()).first()
    return {
        "cohort_alert": alert
    }

def active_cohort(request):
    cohort = (
        Cohort.objects
        .filter(is_active=True, registration_deadline__gt=timezone.now())
        .first()
    )
    return {"active_cohort": cohort}

def social_links(request):
    return {
        'social_links': SocialLink.objects.filter(is_active=True)
    }