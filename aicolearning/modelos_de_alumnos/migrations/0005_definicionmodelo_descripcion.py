# Generated by Django 4.2.1 on 2023-06-17 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "modelos_de_alumnos",
            "0004_rename_caracteristica_valorseleccion_caracteristica",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="definicionmodelo",
            name="descripcion",
            field=models.TextField(blank=True, null=True, verbose_name="descripcion"),
        ),
    ]
