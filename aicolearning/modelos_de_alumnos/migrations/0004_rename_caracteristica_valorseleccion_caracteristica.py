# Generated by Django 4.2.1 on 2023-06-10 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("modelos_de_alumnos", "0003_alter_datomodelo_id_alumno"),
    ]

    operations = [
        migrations.RenameField(
            model_name="valorseleccion",
            old_name="Caracteristica",
            new_name="caracteristica",
        ),
    ]
