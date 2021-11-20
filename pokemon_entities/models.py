from django.db import models
from django.db.models.base import Model  # noqa F401

class Pokemon(models.Model):
    """Модель покемона."""
    title = models.CharField(blank=False, max_length=200)
