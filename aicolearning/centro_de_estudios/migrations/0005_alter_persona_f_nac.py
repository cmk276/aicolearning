# Generated by Django 4.2.1 on 2023-06-07 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("centro_de_estudios", "0004_alumno_id_alumno"),
    ]

    operations = [
        migrations.AlterField(
            model_name="persona",
            name="f_nac",
            field=models.DateField(blank=True, verbose_name="fecha de nacimiento"),
        ),
    ]
