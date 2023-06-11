# Generated by Django 4.2.1 on 2023-06-11 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("trabajo_colaborativo", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="equipo",
            name="id_agrupamiento",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="trabajo_colaborativo.agrupamiento",
            ),
        ),
        migrations.RemoveField(
            model_name="agrupamiento",
            name="equipos",
        ),
        migrations.AddField(
            model_name="agrupamiento",
            name="equipos",
            field=models.ManyToManyField(to="trabajo_colaborativo.equipo"),
        ),
    ]
