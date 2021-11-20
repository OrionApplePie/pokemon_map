from django.db import models
from django.db.models.base import Model  # noqa F401

class Pokemon(models.Model):
    """Модель покемона."""

    title_ru = models.CharField(verbose_name='Имя (рус.)', max_length=200)
    title_en = models.CharField(verbose_name='Имя (англ.)', max_length=200)
    title_jp = models.CharField(verbose_name='Имя (яп.)', max_length=200)

    description = models.TextField(
        verbose_name='Описание',
        null=True, blank=True
    )
    image = models.ImageField(
        verbose_name='Изображение',
        null=True, blank=True
    )

    previous_evolution = models.ForeignKey(
        'self',
        null=True, blank=True,
        verbose_name='Из кого эволюционировал',
        related_name='next_evolutions',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    """Модель для координат конкретного покемона на карте."""

    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='Покемон',
        on_delete=models.CASCADE)

    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')

    appeared_at = models.DateTimeField(verbose_name='Появление')
    disappeared_at = models.DateTimeField(verbose_name='Исчезновение')

    level = models.IntegerField(verbose_name='Уровень')
    health = models.IntegerField(verbose_name='Здоровье')
    strength = models.IntegerField(verbose_name='Сила')
    defence = models.IntegerField(verbose_name='Защита')
    stamina = models.IntegerField(verbose_name='Выносливость')

    def __str__(self):
        return f'{self.pokemon} {self.level} ур.'
