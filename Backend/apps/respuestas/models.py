from django.db import models

class Encuesta(models.Model):
    # Definición de las opciones de respuesta
    OPCIONES_RESPUESTA = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('Blanco', 'Blanco'),
        ('Multi Marca', 'Multi Marca'),
    ]
    
    # Campos generales
    nombre = models.CharField(max_length=255)  # Nombre del proyecto
    fecha = models.DateField()  # Fecha del proyecto
    ciudad = models.CharField(max_length=100)  # Ciudad
    departamento = models.CharField(max_length=100)  # Departamento
    aplicacion = models.CharField(max_length=100)  # Nombre de la aplicación
    prueba = models.CharField(max_length=100)  # Tipo de prueba Matenmaticas o lenguaje
    nombre_institucion = models.CharField(max_length=255)  # Nombre de la institución
    numero_cuadernillo = models.CharField(max_length=50)  # Número de cuadernillo
    nombre_estudiante = models.CharField(max_length=255)  # Nombre del estudiante
    documento_estudiante = models.CharField(max_length=20, unique=True, null=True, blank=True)  # Documento de identidad del estudiante
    grado = models.CharField(max_length=50)  # Grado
    edad = models.IntegerField()  # Edad
    genero = models.CharField(max_length=255, null=True, blank=True) # Genero

    # Respuestas (20 respuestas)
    respuesta_1 = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA, blank=True, null=True)
    respuesta_2 = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA, blank=True, null=True)
    respuesta_3 = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA, blank=True, null=True)
    respuesta_4 = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA, blank=True, null=True)
    respuesta_5 = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA, blank=True, null=True)
    respuesta_6 = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA, blank=True, null=True)
    respuesta_7 = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA, blank=True, null=True)
    respuesta_8 = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA, blank=True, null=True)
    respuesta_9 = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA, blank=True, null=True)
    respuesta_10 = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA, blank=True, null=True)
    respuesta_11 = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA, blank=True, null=True)
    respuesta_12 = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA, blank=True, null=True)
    respuesta_13 = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA, blank=True, null=True)
    respuesta_14 = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA, blank=True, null=True)
    respuesta_15 = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA, blank=True, null=True)
    respuesta_16 = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA, blank=True, null=True)
    respuesta_17 = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA, blank=True, null=True)
    respuesta_18 = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA, blank=True, null=True)
    respuesta_19 = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA, blank=True, null=True)
    respuesta_20 = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA, blank=True, null=True)
    
    # Respuestas (20 calificaciones)
    calificacion_1 = models.CharField(max_length=200 , blank=True, null=True)
    calificacion_2 = models.CharField(max_length=200 , blank=True, null=True)
    calificacion_3 = models.CharField(max_length=200 , blank=True, null=True)
    calificacion_4 = models.CharField(max_length=200 , blank=True, null=True)
    calificacion_5 = models.CharField(max_length=200 , blank=True, null=True)
    calificacion_6 = models.CharField(max_length=200 , blank=True, null=True)
    calificacion_7 = models.CharField(max_length=200 , blank=True, null=True)
    calificacion_8 = models.CharField(max_length=200 , blank=True, null=True)
    calificacion_9 = models.CharField(max_length=200 , blank=True, null=True)
    calificacion_10 = models.CharField(max_length=200 , blank=True, null=True)
    calificacion_11 = models.CharField(max_length=200 , blank=True, null=True)
    calificacion_12 = models.CharField(max_length=200 , blank=True, null=True)
    calificacion_13 = models.CharField(max_length=200 , blank=True, null=True)
    calificacion_14 = models.CharField(max_length=200 , blank=True, null=True)
    calificacion_15 = models.CharField(max_length=200 , blank=True, null=True)
    calificacion_16 = models.CharField(max_length=200 , blank=True, null=True)
    calificacion_17 = models.CharField(max_length=200 , blank=True, null=True)
    calificacion_18 = models.CharField(max_length=200 , blank=True, null=True)
    calificacion_19 = models.CharField(max_length=200 , blank=True, null=True)
    calificacion_20 = models.CharField(max_length=200 , blank=True, null=True)
    correctos = models.IntegerField(default=0) # Cantidad de respuestas correctas

    responsable = models.CharField(max_length=200 , blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_estudiante} - {self.nombre_institucion} - {self.fecha}"

    class Meta:
        verbose_name = "Respuesta"
        verbose_name_plural = "Respuestas"

#Modelos para las preguntas y cuedernillos de Matemáticas ----------------------------------------------------------------------------------------------------------------------------
class PreguntaMate(models.Model):
    # Definición de las opciones de respuesta
    OPCIONES_RESPUESTA = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]
    # Opciones de dificultad
    OPCIONES_DIFICULTAD = [
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta'),
    ]
    # Campos para la pregunta
    codigo_pregunta = models.CharField(max_length=50, unique=True)  # Código único de la pregunta
    grado = models.CharField(max_length=50)  # Grado al que está dirigida la pregunta
    competencia = models.CharField(max_length=255)  # Competencia evaluada por la pregunta
    componente = models.CharField(max_length=255)  # Componente que evalúa la pregunta
    afirmacion = models.TextField()  # Afirmación o enunciado de la pregunta
    evidencia = models.TextField()  # Evidencia que se busca tras la tarea
    tarea = models.TextField()  # Tarea asociada a la pregunta
    dificultad = models.CharField(max_length=50, choices=OPCIONES_DIFICULTAD)  # Dificultad de la pregunta
    clave = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA)  # Clave-respuesta correcta

    def __str__(self):
        return f"Pregunta {self.codigo_pregunta}"

    class Meta:
        verbose_name = "Pregunta de matemáticas"
        verbose_name_plural = "Preguntas de matemáticas"

class CuadernilloMate(models.Model):
    # Nombre del cuadernillo
    nombre = models.CharField(max_length=255, unique=True)
    preguntas = models.ManyToManyField(PreguntaMate, through='CuadernilloPreguntaMate', blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Cuadernillo de Matemáticas"
        verbose_name_plural = "Cuadernillos de Matemáticas"

class CuadernilloPreguntaMate(models.Model):
    cuadernillo = models.ForeignKey(CuadernilloMate, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(PreguntaMate, on_delete=models.CASCADE)
    orden = models.PositiveIntegerField()  # Puedes definir el orden de las preguntas en el cuadernillo

    class Meta:
        db_table = 'cuadernillo_pregunta_mate'
        unique_together = ('cuadernillo', 'pregunta')  # Para evitar que una pregunta esté duplicada en un cuadernillo

    def __str__(self):
        return f"Cuadernillo: {self.cuadernillo.nombre} - Pregunta: {self.pregunta.codigo_pregunta}"

#Modelos para las preguntas y cuedernillos de Lenguaje ----------------------------------------------------------------------------------------------------------------------------
class PreguntaLengua(models.Model):
    # Definición de las opciones de respuesta
    OPCIONES_RESPUESTA = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]
    # Opciones de dificultad
    OPCIONES_DIFICULTAD = [
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta'),
    ]
    # Campos para la pregunta
    codigo_pregunta = models.CharField(max_length=50, unique=True)  # Código único de la pregunta
    grado = models.CharField(max_length=50)  # Grado al que está dirigida la pregunta
    tipo_texto = models.CharField(max_length=50)
    secuencia_textual = models.CharField(max_length=50)
    num_texto = models.IntegerField()
    texto = models.CharField(max_length=255)
    competencia = models.CharField(max_length=255)  # Competencia evaluada por la pregunta
    afirmacion = models.TextField()  # Afirmación o enunciado de la pregunta
    evidencia = models.TextField()  # Evidencia que se busca tras la tarea
    tarea = models.TextField()  # Tarea asociada a la pregunta
    dificultad = models.CharField(max_length=50, choices=OPCIONES_DIFICULTAD)  # Dificultad de la pregunta
    clave = models.CharField(max_length=20, choices=OPCIONES_RESPUESTA)  # Clave-respuesta correcta

    def __str__(self):
        return f"Pregunta {self.codigo_pregunta}"

    class Meta:
        verbose_name = "Pregunta de lenguaje"
        verbose_name_plural = "Preguntas de lenguaje"

class CuadernilloLengua(models.Model):
    # Nombre del cuadernillo
    nombre = models.CharField(max_length=255, unique=True)
    preguntas = models.ManyToManyField(PreguntaLengua, through='CuadernilloPreguntaLengua', blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Cuadernillo de Lenguaje"
        verbose_name_plural = "Cuadernillos de Lenguaje"

class CuadernilloPreguntaLengua(models.Model):
    cuadernillo = models.ForeignKey(CuadernilloLengua, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(PreguntaLengua, on_delete=models.CASCADE)
    orden = models.PositiveIntegerField()  # Puedes definir el orden de las preguntas en el cuadernillo

    class Meta:
        db_table = 'cuadernillo_pregunta_lengua'
        unique_together = ('cuadernillo', 'pregunta')  # Para evitar que una pregunta esté duplicada en un cuadernillo

    def __str__(self):
        return f"Cuadernillo: {self.cuadernillo.nombre} - Pregunta: {self.pregunta.codigo_pregunta}"
