# Generated by Django 4.2.1 on 2023-06-03 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("centro_de_estudios", "0003_grupo_alumno_grupos_curso_grupos"),
    ]

    operations = [
        migrations.AddField(
            model_name="alumno",
            name="id_alumno",
            field=models.CharField(
                default="0000000000", max_length=10, verbose_name="DNI"
            ),
        ),
    ]