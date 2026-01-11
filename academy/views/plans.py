from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..models import Plan, PlanEnrollment
from django.utils import timezone
from datetime import timedelta
from ..utils import user_has_plan

def plan_detail(request, slug):
    plan = get_object_or_404(Plan, slug=slug)

    # Does user own the plan?
    owned = False
    enrolled_courses = []

    if request.user.is_authenticated:
        owned = user_has_plan(request.user, plan)

        # If user owns plan → all courses in plan are accessible
        if owned:
            enrolled_courses = plan.courses.all()

    return render(request, 'academy/plan_detail.html', {
        'plan': plan,
        'owned': owned,
        'enrolled_courses': enrolled_courses,
    })


@login_required
def enroll_plan(request, slug):
    plan = get_object_or_404(Plan, slug=slug)

    # Prevent duplicate enrollment
    if PlanEnrollment.objects.filter(
        user=request.user,
        plan=plan,
        is_active=True
    ).exists():
        return redirect("dashboard")

    expires_at = timezone.now() + timedelta(days=plan.duration_weeks)

    PlanEnrollment.objects.create(
        user=request.user,
        plan=plan,
        expires_at=expires_at
    )
    return redirect("dashboard")