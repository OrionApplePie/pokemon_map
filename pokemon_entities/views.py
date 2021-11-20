import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.all()

    for pokemon_entity in pokemon_entities:
        pokemon = Pokemon.objects.get(id=pokemon_entity.pokemon.id)
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon.image.url),
        )

    pokemons = Pokemon.objects.all()

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon_image_url = request.build_absolute_uri(
        requested_pokemon.image.url
    )

    previous_evolution = None
    next_evolution = None

    if requested_pokemon.previous_evolution is not None:
        previous_evolution_pokemon_image_url = request.build_absolute_uri(
            requested_pokemon.previous_evolution.image.url
        )
        previous_evolution = {
            'title_ru': requested_pokemon.previous_evolution.title_ru,
            'pokemon_id': requested_pokemon.previous_evolution.id,
            'img_url': previous_evolution_pokemon_image_url,
        }

    next_evolutions = requested_pokemon.next_evolutions.all()

    if next_evolutions.exists():
        next_evolution_pokemon_image_url = request.build_absolute_uri(
            next_evolutions[0].image.url
        )
        next_evolution = {
            'title_ru': next_evolutions[0].title_ru,
            'pokemon_id': next_evolutions[0].id,
            'img_url': next_evolution_pokemon_image_url,
        }

    pokemon = {
        'title_ru': requested_pokemon.title_ru,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
        'img_url': pokemon_image_url,

        'previous_evolution': previous_evolution,
        'next_evolution': next_evolution,
    }

    pokemon_entities = PokemonEntity.objects.filter(
        pokemon__id=pokemon_id
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_image_url,
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
