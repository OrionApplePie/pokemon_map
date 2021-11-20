from django.db import models
from django.db.models.base import Model  # noqa F401

class Pokemon(models.Model):
    """Модель покемона."""

    title_ru = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    title_jp = models.CharField(max_length=200)

    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    """Модель для координат конкретного покемона на карте."""

    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    lat = models.FloatField()
    lon = models.FloatField()

    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()

    level = models.IntegerField()
    health = models.IntegerField()
    strength = models.IntegerField()
    defence = models.IntegerField()
    stamina = models.IntegerField()

    def __str__(self):
        return f'{self.pokemon} {self.level} ур.'
