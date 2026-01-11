# academy/models/enrollment.py
from django.db import models
from django.contrib.auth.models import User
from .plan import *
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

User = settings.AUTH_USER_MODEL


class PlanEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # allow multiple plans
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def has_expired(self):
        return timezone.now() > self.expires_at

    @property
    def is_valid(self):
        return self.is_active and timezone.now() < self.expires_at

    class Meta:
        unique_together = ('user', 'plan')  # prevent duplicates

    def __str__(self):
        return f"{self.user} → {self.plan}"
