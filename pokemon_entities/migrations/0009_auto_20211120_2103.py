# Generated by Django 3.1.13 on 2021-11-20 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0008_auto_20211120_2034'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pokemon',
            old_name='picture',
            new_name='image',
        ),
    ]
