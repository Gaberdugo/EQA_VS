# Generated by Django 4.2.16 on 2024-11-22 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CuadernilloLengua',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Cuadernillo de Lenguaje',
                'verbose_name_plural': 'Cuadernillos de Lenguaje',
            },
        ),
        migrations.CreateModel(
            name='CuadernilloMate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Cuadernillo de Matemáticas',
                'verbose_name_plural': 'Cuadernillos de Matemáticas',
            },
        ),
        migrations.CreateModel(
            name='Encuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('fecha', models.DateField()),
                ('ciudad', models.CharField(max_length=100)),
                ('departamento', models.CharField(max_length=100)),
                ('aplicacion', models.CharField(max_length=100)),
                ('prueba', models.CharField(max_length=100)),
                ('nombre_institucion', models.CharField(max_length=255)),
                ('numero_cuadernillo', models.CharField(max_length=50)),
                ('nombre_estudiante', models.CharField(max_length=255)),
                ('documento_estudiante', models.CharField(max_length=20)),
                ('grado', models.CharField(max_length=50)),
                ('edad', models.IntegerField()),
                ('genero', models.CharField(blank=True, max_length=255, null=True)),
                ('respuesta_1', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('Blanco', 'Blanco'), ('Multi Marca', 'Multi Marca')], max_length=20, null=True)),
                ('respuesta_2', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('Blanco', 'Blanco'), ('Multi Marca', 'Multi Marca')], max_length=20, null=True)),
                ('respuesta_3', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('Blanco', 'Blanco'), ('Multi Marca', 'Multi Marca')], max_length=20, null=True)),
                ('respuesta_4', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('Blanco', 'Blanco'), ('Multi Marca', 'Multi Marca')], max_length=20, null=True)),
                ('respuesta_5', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('Blanco', 'Blanco'), ('Multi Marca', 'Multi Marca')], max_length=20, null=True)),
                ('respuesta_6', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('Blanco', 'Blanco'), ('Multi Marca', 'Multi Marca')], max_length=20, null=True)),
                ('respuesta_7', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('Blanco', 'Blanco'), ('Multi Marca', 'Multi Marca')], max_length=20, null=True)),
                ('respuesta_8', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('Blanco', 'Blanco'), ('Multi Marca', 'Multi Marca')], max_length=20, null=True)),
                ('respuesta_9', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('Blanco', 'Blanco'), ('Multi Marca', 'Multi Marca')], max_length=20, null=True)),
                ('respuesta_10', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('Blanco', 'Blanco'), ('Multi Marca', 'Multi Marca')], max_length=20, null=True)),
                ('respuesta_11', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('Blanco', 'Blanco'), ('Multi Marca', 'Multi Marca')], max_length=20, null=True)),
                ('respuesta_12', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('Blanco', 'Blanco'), ('Multi Marca', 'Multi Marca')], max_length=20, null=True)),
                ('respuesta_13', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('Blanco', 'Blanco'), ('Multi Marca', 'Multi Marca')], max_length=20, null=True)),
                ('respuesta_14', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('Blanco', 'Blanco'), ('Multi Marca', 'Multi Marca')], max_length=20, null=True)),
                ('respuesta_15', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('Blanco', 'Blanco'), ('Multi Marca', 'Multi Marca')], max_length=20, null=True)),
                ('respuesta_16', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('Blanco', 'Blanco'), ('Multi Marca', 'Multi Marca')], max_length=20, null=True)),
                ('respuesta_17', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('Blanco', 'Blanco'), ('Multi Marca', 'Multi Marca')], max_length=20, null=True)),
                ('respuesta_18', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('Blanco', 'Blanco'), ('Multi Marca', 'Multi Marca')], max_length=20, null=True)),
                ('respuesta_19', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('Blanco', 'Blanco'), ('Multi Marca', 'Multi Marca')], max_length=20, null=True)),
                ('respuesta_20', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('Blanco', 'Blanco'), ('Multi Marca', 'Multi Marca')], max_length=20, null=True)),
                ('calificacion_1', models.CharField(blank=True, max_length=200, null=True)),
                ('calificacion_2', models.CharField(blank=True, max_length=200, null=True)),
                ('calificacion_3', models.CharField(blank=True, max_length=200, null=True)),
                ('calificacion_4', models.CharField(blank=True, max_length=200, null=True)),
                ('calificacion_5', models.CharField(blank=True, max_length=200, null=True)),
                ('calificacion_6', models.CharField(blank=True, max_length=200, null=True)),
                ('calificacion_7', models.CharField(blank=True, max_length=200, null=True)),
                ('calificacion_8', models.CharField(blank=True, max_length=200, null=True)),
                ('calificacion_9', models.CharField(blank=True, max_length=200, null=True)),
                ('calificacion_10', models.CharField(blank=True, max_length=200, null=True)),
                ('calificacion_11', models.CharField(blank=True, max_length=200, null=True)),
                ('calificacion_12', models.CharField(blank=True, max_length=200, null=True)),
                ('calificacion_13', models.CharField(blank=True, max_length=200, null=True)),
                ('calificacion_14', models.CharField(blank=True, max_length=200, null=True)),
                ('calificacion_15', models.CharField(blank=True, max_length=200, null=True)),
                ('calificacion_16', models.CharField(blank=True, max_length=200, null=True)),
                ('calificacion_17', models.CharField(blank=True, max_length=200, null=True)),
                ('calificacion_18', models.CharField(blank=True, max_length=200, null=True)),
                ('calificacion_19', models.CharField(blank=True, max_length=200, null=True)),
                ('calificacion_20', models.CharField(blank=True, max_length=200, null=True)),
                ('correctos', models.IntegerField(default=0)),
                ('responsable', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Respuesta',
                'verbose_name_plural': 'Respuestas',
            },
        ),
        migrations.CreateModel(
            name='PreguntaLengua',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_pregunta', models.CharField(max_length=50, unique=True)),
                ('grado', models.CharField(max_length=50)),
                ('tipo_texto', models.CharField(max_length=50)),
                ('secuencia_textual', models.CharField(max_length=50)),
                ('num_texto', models.IntegerField()),
                ('texto', models.CharField(max_length=255)),
                ('competencia', models.CharField(max_length=255)),
                ('afirmacion', models.TextField()),
                ('evidencia', models.TextField()),
                ('tarea', models.TextField()),
                ('dificultad', models.CharField(choices=[('Baja', 'Baja'), ('Media', 'Media'), ('Alta', 'Alta')], max_length=50)),
                ('clave', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=20)),
            ],
            options={
                'verbose_name': 'Pregunta de lenguaje',
                'verbose_name_plural': 'Preguntas de lenguaje',
            },
        ),
        migrations.CreateModel(
            name='PreguntaMate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_pregunta', models.CharField(max_length=50, unique=True)),
                ('grado', models.CharField(max_length=50)),
                ('competencia', models.CharField(max_length=255)),
                ('componente', models.CharField(max_length=255)),
                ('afirmacion', models.TextField()),
                ('evidencia', models.TextField()),
                ('tarea', models.TextField()),
                ('dificultad', models.CharField(choices=[('Baja', 'Baja'), ('Media', 'Media'), ('Alta', 'Alta')], max_length=50)),
                ('clave', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=20)),
            ],
            options={
                'verbose_name': 'Pregunta de matemáticas',
                'verbose_name_plural': 'Preguntas de matemáticas',
            },
        ),
        migrations.CreateModel(
            name='CuadernilloPreguntaMate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orden', models.PositiveIntegerField()),
                ('cuadernillo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='respuestas.cuadernillomate')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='respuestas.preguntamate')),
            ],
            options={
                'db_table': 'cuadernillo_pregunta_mate',
                'unique_together': {('cuadernillo', 'pregunta')},
            },
        ),
        migrations.CreateModel(
            name='CuadernilloPreguntaLengua',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orden', models.PositiveIntegerField()),
                ('cuadernillo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='respuestas.cuadernillolengua')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='respuestas.preguntalengua')),
            ],
            options={
                'db_table': 'cuadernillo_pregunta_lengua',
                'unique_together': {('cuadernillo', 'pregunta')},
            },
        ),
        migrations.AddField(
            model_name='cuadernillomate',
            name='preguntas',
            field=models.ManyToManyField(blank=True, through='respuestas.CuadernilloPreguntaMate', to='respuestas.preguntamate'),
        ),
        migrations.AddField(
            model_name='cuadernillolengua',
            name='preguntas',
            field=models.ManyToManyField(blank=True, through='respuestas.CuadernilloPreguntaLengua', to='respuestas.preguntalengua'),
        ),
    ]
