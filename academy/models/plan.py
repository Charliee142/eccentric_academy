# academy/models/plan.py
from django.db import models



class Plan(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'Beginner Track'),
        ('intermediate', 'Intermediate Track'),
        ('advanced', 'Advanced Track'),
    )

    name = models.CharField(max_length=50)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField(help_text="One feature per line", blank=True, null=True)
    description = models.TextField()
    duration_weeks = models.PositiveIntegerField(help_text="Duration in weeks (e.g. 30, 90, 180)",default=90)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.name
