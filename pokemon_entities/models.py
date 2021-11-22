from django.db import models
from django.db.models.base import Model  # noqa F401

class Pokemon(models.Model):
    """Модель покемона."""

    title_ru = models.CharField(verbose_name='Имя (рус.)', max_length=200)
    title_en = models.CharField(
        verbose_name='Имя (англ.)',
        max_length=200,
        blank=True
    )
    title_jp = models.CharField(
        verbose_name='Имя (яп.)',
        max_length=200,
        blank=True
    )

    description = models.TextField(
        verbose_name='Описание',
        blank=True
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
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    """Модель для конкретного покемона на карте."""

    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='Покемон',
        related_name='entities',
        on_delete=models.CASCADE)

    lat = models.FloatField(
        verbose_name='Широта',
        null=True, blank=True
    )
    lon = models.FloatField(
        verbose_name='Долгота',
        null=True, blank=True
    )

    appeared_at = models.DateTimeField(
        verbose_name='Появление',
        null=True, blank=True
    )
    disappeared_at = models.DateTimeField(
        verbose_name='Исчезновение',
        null=True, blank=True
    )

    level = models.IntegerField(
        verbose_name='Уровень',
        null=True, blank=True
    )
    health = models.IntegerField(
        verbose_name='Здоровье',
        null=True, blank=True
    )
    strength = models.IntegerField(
        verbose_name='Сила',
        null=True, blank=True
    )
    defence = models.IntegerField(
        verbose_name='Защита',
        null=True, blank=True
    )
    stamina = models.IntegerField(
        verbose_name='Выносливость',
        null=True, blank=True
    )

    def __str__(self):
        return f'{self.pokemon}, уровень: {self.level or "Н/Д"}'
