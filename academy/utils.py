from .models import PlanEnrollment
from django.utils import timezone

def user_has_plan(user, plan):
    if not user.is_authenticated:
        return False

    return PlanEnrollment.objects.filter(
        user=user,
        plan=plan,
        is_active=True
    ).exists()
