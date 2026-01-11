from django.db import models

class ProgramOutcome(models.Model):
    LEVEL_CHOICES = (
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    )
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="beginner", blank=True)
    icon_image = models.ImageField(upload_to="program_icons/", help_text="Upload PNG / SVG icon (recommended: transparent background)", blank=True)
    title = models.CharField(max_length=150)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title
