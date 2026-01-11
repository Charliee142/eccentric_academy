from django.db import models
from django.contrib.auth.models import User
from .plan import Plan

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()  # in kobo
    reference = models.CharField(max_length=100, unique=True)
    verified = models.BooleanField(default=False)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.plan} - {self.amount}"
