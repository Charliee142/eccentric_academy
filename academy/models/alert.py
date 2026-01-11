from django.db import models
from django.utils.timezone import now


class CohortAlert(models.Model):
    title = models.CharField(max_length=100)
    message = models.CharField(max_length=255)
    start_date = models.DateField()
    cta_text = models.CharField(max_length=50, default="Enroll Now →")
    cta_url = models.CharField(max_length=200, default="/pricing/")
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


    @property
    def expired(self):
        return self.start_date < now().date()

    def __str__(self):
        return f"{self.title} ({'Active' if self.is_active else 'Inactive'})"
