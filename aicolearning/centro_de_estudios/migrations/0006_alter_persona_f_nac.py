# Generated by Django 4.2.1 on 2023-06-07 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("centro_de_estudios", "0005_alter_persona_f_nac"),
    ]

    operations = [
        migrations.AlterField(
            model_name="persona",
            name="f_nac",
            field=models.DateField(null=True, verbose_name="fecha de nacimiento"),
        ),
    ]
