# Generated by Django 4.2.16 on 2024-11-24 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('respuestas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encuesta',
            name='documento_estudiante',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
