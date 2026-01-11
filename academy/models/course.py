# academy/models/course.py
from django.db import models
from .plan import *


class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    plan = models.ForeignKey(
        Plan,
        related_name='courses',
        on_delete=models.CASCADE
    )
    description = models.TextField()
    featured_image = models.ImageField(upload_to='courses/')
    is_published = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
