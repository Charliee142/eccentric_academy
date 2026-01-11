from django.db import models
from django.utils import timezone

class Cohort(models.Model):
    name = models.CharField(max_length=100)
    registration_deadline = models.DateTimeField()
    max_slots = models.PositiveIntegerField(default=50)
    slots_taken = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-registration_deadline"]

    def slots_remaining(self):
        return max(self.max_slots - self.slots_taken, 0)

    def is_open(self):
        return (
            self.is_active
            and timezone.now() < self.registration_deadline
            and self.slots_remaining() > 0
        )

    def __str__(self):
        return self.name
