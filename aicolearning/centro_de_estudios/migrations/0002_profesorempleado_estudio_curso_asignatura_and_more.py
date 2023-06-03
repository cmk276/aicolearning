# Generated by Django 4.2.1 on 2023-06-03 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("centro_de_estudios", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProfesorEmpleado",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "fecha_alta",
                    models.DateField(auto_now_add=True, verbose_name="fecha de alta"),
                ),
                ("fecha_baja", models.DateField(verbose_name="fecha de baja")),
                (
                    "centroDeEstudios",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="centro_de_estudios.centrodeestudios",
                    ),
                ),
                (
                    "profesor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="centro_de_estudios.profesor",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Estudio",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=150, verbose_name="estudio")),
                (
                    "centroDeEstudios",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="centro_de_estudios.centrodeestudios",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Curso",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=150, verbose_name="curso")),
                ("descripcion", models.TextField(verbose_name="descripción")),
                (
                    "estudio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="centro_de_estudios.estudio",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Asignatura",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=150, verbose_name="curso")),
                ("descripcion", models.TextField(verbose_name="descripción")),
                ("cursos", models.ManyToManyField(to="centro_de_estudios.curso")),
            ],
        ),
        migrations.AddField(
            model_name="centrodeestudios",
            name="profesores",
            field=models.ManyToManyField(
                through="centro_de_estudios.ProfesorEmpleado",
                to="centro_de_estudios.profesor",
            ),
        ),
    ]