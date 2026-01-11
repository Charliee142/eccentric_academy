# academy/models/testimonial.py

from django.db import models

class Testimonial(models.Model):
    RATING_CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    quote = models.TextField()
    image = models.ImageField(upload_to='testimonials/')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.role})"
