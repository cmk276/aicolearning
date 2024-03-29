# Generated by Django 4.2.1 on 2023-06-03 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Caracteristica",
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
                ("etiqueta", models.CharField(max_length=100, verbose_name="nombre")),
                (
                    "tipo",
                    models.CharField(
                        choices=[
                            ("NU", "Numérica"),
                            ("NO", "No Ordenada"),
                            ("TE", "Texto"),
                            ("BO", "Verdadero/Falso"),
                            ("OR", "Ordenada"),
                        ],
                        default="NU",
                        max_length=2,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ValorSeleccion",
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
                ("num_orden", models.IntegerField(verbose_name="número de orden")),
                ("etiqueta", models.CharField(max_length=100, verbose_name="nombre")),
                (
                    "Caracteristica",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="modelos_de_alumnos.caracteristica",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DefinicionModelo",
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
                ("nombre", models.CharField(max_length=50, verbose_name="nombre")),
                (
                    "caracteristicas",
                    models.ManyToManyField(to="modelos_de_alumnos.caracteristica"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DatoModelo",
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
                    "id_alumno",
                    models.CharField(max_length=10, verbose_name="id alumno"),
                ),
                ("datos", models.JSONField(verbose_name="datos")),
                (
                    "modelo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="modelos_de_alumnos.definicionmodelo",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="caracteristica",
            name="definicion_modelo",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="modelos_de_alumnos.definicionmodelo",
            ),
        ),
    ]
