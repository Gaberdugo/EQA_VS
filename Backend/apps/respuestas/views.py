import random
import pandas as pd
import math
import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.platypus import Image as RLImage
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from traceback import format_exc
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from rest_framework import permissions
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Encuesta, CuadernilloMate, CuadernilloLengua
from .serializers import EncuestaSerializer, CuadernilloMateSerializer, PreguntaMateSerializer, PreguntaLenguaSerializer, Encuesta2Serializer, InstitucionSerializer
from rest_framework.permissions import AllowAny

class EncuestaView(APIView):
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación

    def post(self, request):

        respuesta = {}

        try:
            if request.data['prueba'] == 'Matemáticas':
                num = request.data['numero_cuadernillo']
                cuadernillo = CuadernilloMate.objects.get(nombre=num)
                preguntas = cuadernillo.preguntas.all()
            elif request.data['prueba'] == 'Lenguaje':
                num = request.data['numero_cuadernillo']
                cuadernillo = CuadernilloLengua.objects.get(nombre=num)
                preguntas = cuadernillo.preguntas.all()
        except:
            preguntas = []

        res = []
        for k,v in request.data.items():
            
            if k[:3] == 'res':
                res.append(v)
            
            respuesta[k] = v

        val = [0]

        i = 0
        c = 0
        for pregunta in preguntas:
            if res[i] == 'Blanco':
                val.append(str(pregunta.codigo_pregunta) + ' 99')
            elif res[i] == 'Multi Marca':
                val.append(str(pregunta.codigo_pregunta) + ' 97')
            elif res[i] == pregunta.clave:
                val.append(str(pregunta.codigo_pregunta) + ' 1')
                c+=1
            else:
                val.append(str(pregunta.codigo_pregunta) + ' 0')
            i+=1
            respuesta[f'calificacion_{i}'] = val[-1]

        respuesta['correctos'] = c

        respuesta['responsable'] = request.data['responsable']

        # Modulo para calcular la edad
        if len(request.data['edad']) == 0:
            edad = 0
        elif int(request.data['fecha'].split('-')[1]) - int(request.data['edad'].split('-')[1]) < 0:
            edad = int(request.data['fecha'].split('-')[0]) - int(request.data['edad'].split('-')[0]) - 1
        elif int(request.data['fecha'].split('-')[1]) - int(request.data['edad'].split('-')[1]) == 0:
            if int(request.data['fecha'].split('-')[2]) - int(request.data['edad'].split('-')[2]) < 0:
                edad = int(request.data['fecha'].split('-')[0]) - int(request.data['edad'].split('-')[0]) - 1
            else:
                edad = int(request.data['fecha'].split('-')[0]) - int(request.data['edad'].split('-')[0])
        else:
            edad = int(request.data['fecha'].split('-')[0]) - int(request.data['edad'].split('-')[0]) 
        
        respuesta['edad'] = edad

        # Crear una nueva instancia de Encuesta utilizando los datos del request
        serializer = EncuestaSerializer(data=respuesta)
        
        if serializer.is_valid():
            # Si los datos son válidos, guardamos el objeto Encuesta
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Devuelve la respuesta con el objeto creado
        else:
            # Si los datos no son válidos, devolvemos un error con los detalles
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EncuestaExportView(APIView):
    def get(self, request):
        # Obtener el nombre del proyecto desde los parámetros de la URL
        nombre_proyecto = request.GET.get('nombre_proyecto')

        # Si no se proporciona el nombre del proyecto, devolver un error
        if not nombre_proyecto:
            return Response({"error": "Se debe proporcionar el nombre del proyecto."}, status=400)

        # Filtrar las encuestas por el nombre del proyecto
        encuestas = Encuesta.objects.filter(nombre=nombre_proyecto).order_by('id')


        # Si no hay encuestas para el proyecto proporcionado
        if not encuestas:
            return Response({"error": "No se encontraron encuestas para el proyecto proporcionado."}, status=404)
            
        #print(cuadernillo.preguntas.get(codigo_pregunta="M3CN111001"))

        # Crear una lista de diccionarios con los datos de las encuestas
        data = []
        for encuesta in encuestas:
            try:
                data.append({
                    'ID': encuesta.id,
                    'Digitador': encuesta.responsable,
                    'Cargado': encuesta.fecha_cargue,
                    'Proyecto': encuesta.nombre,
                    'Fecha': encuesta.fecha,
                    'Ciudad': encuesta.ciudad,
                    'Departamento': encuesta.departamento,
                    'Colegio': encuesta.nombre_institucion,
                    'Nombre': encuesta.nombre_estudiante,
                    'Prueba': encuesta.prueba,
                    'Grado': encuesta.grado,
                    'Edad': encuesta.edad,
                    'Genero': encuesta.genero,
                    'Cuadernillo': encuesta.numero_cuadernillo,
                    'Respuesta 1': encuesta.respuesta_1,
                    'Respuesta 2': encuesta.respuesta_2,
                    'Respuesta 3': encuesta.respuesta_3,
                    'Respuesta 4': encuesta.respuesta_4,
                    'Respuesta 5': encuesta.respuesta_5,
                    'Respuesta 6': encuesta.respuesta_6,
                    'Respuesta 7': encuesta.respuesta_7,
                    'Respuesta 8': encuesta.respuesta_8,
                    'Respuesta 9': encuesta.respuesta_9,
                    'Respuesta 10': encuesta.respuesta_10,
                    'Respuesta 11': encuesta.respuesta_11,
                    'Respuesta 12': encuesta.respuesta_12,
                    'Respuesta 13': encuesta.respuesta_13,
                    'Respuesta 14': encuesta.respuesta_14,
                    'Respuesta 15': encuesta.respuesta_15,
                    'Respuesta 16': encuesta.respuesta_16,
                    'Respuesta 17': encuesta.respuesta_17,
                    'Respuesta 18': encuesta.respuesta_18,
                    'Respuesta 19': encuesta.respuesta_19,
                    'Respuesta 20': encuesta.respuesta_20,
                    'Calificación 1': encuesta.calificacion_1.split()[1],
                    'Calificación 2': encuesta.calificacion_2.split()[1],
                    'Calificación 3': encuesta.calificacion_3.split()[1],
                    'Calificación 4': encuesta.calificacion_4.split()[1],
                    'Calificación 5': encuesta.calificacion_5.split()[1],
                    'Calificación 6': encuesta.calificacion_6.split()[1],
                    'Calificación 7': encuesta.calificacion_7.split()[1],
                    'Calificación 8': encuesta.calificacion_8.split()[1],
                    'Calificación 9': encuesta.calificacion_9.split()[1],
                    'Calificación 10': encuesta.calificacion_10.split()[1],
                    'Calificación 11': encuesta.calificacion_11.split()[1],
                    'Calificación 12': encuesta.calificacion_12.split()[1],
                    'Calificación 13': encuesta.calificacion_13.split()[1],
                    'Calificación 14': encuesta.calificacion_14.split()[1],
                    'Calificación 15': encuesta.calificacion_15.split()[1],
                    'Calificación 16': encuesta.calificacion_16.split()[1],
                    'Calificación 17': encuesta.calificacion_17.split()[1],
                    'Calificación 18': encuesta.calificacion_18.split()[1],
                    'Calificación 19': encuesta.calificacion_19.split()[1],
                    'Calificación 20': encuesta.calificacion_20.split()[1],
                    'Correctas': encuesta.correctos
                })
            except :
                pass

        # Crear un DataFrame de pandas con los datos
        df = pd.DataFrame(data)

        # Crear la respuesta HTTP para descargar el archivo Excel
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=reporte_encuestas.xlsx'

        # Escribir el DataFrame a un archivo Excel en la respuesta
        with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)

        return response

class CuadernilloMateAPIView(APIView):
    
    def get(self, request, pk=None):
        """
        Obtener todos los cuadernillos o un cuadernillo específico
        """
        if pk:
            # Si se proporciona un ID (pk), devolver un cuadernillo específico
            try:
                cuadernillo = CuadernilloMate.objects.get(pk=pk)
            except CuadernilloMate.DoesNotExist:
                return Response({"detail": "Cuadernillo no encontrado."}, status=status.HTTP_404_NOT_FOUND)

            serializer = CuadernilloMateSerializer(cuadernillo)
            return Response(serializer.data)
        else:
            # Devolver la lista de cuadernillos
            cuadernillos = CuadernilloMate.objects.all()
            serializer = CuadernilloMateSerializer(cuadernillos, many=True)
            return Response(serializer.data)
    
    def post(self, request):
        """
        Crear un nuevo CuadernilloMate
        """
        serializer = CuadernilloMateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EncuestaAleatoriaView(APIView):
    def get(self, request):
        """
        Obtener una encuesta aleatoria de un proyecto específico
        """
        # Obtener el nombre del proyecto desde los parámetros de la URL
        nombre_proyecto = request.GET.get('nombre_proyecto')

        # Si no se proporciona el nombre del proyecto, devolver un error
        if not nombre_proyecto:
            return Response({"error": "Se debe proporcionar el nombre del proyecto."}, status=400)

        # Filtrar las encuestas por el nombre del proyecto
        encuestas = Encuesta.objects.filter(nombre=nombre_proyecto)

        # Si no hay encuestas disponibles para el proyecto proporcionado
        if not encuestas:
            return Response({"error": "No hay encuestas disponibles para el proyecto especificado."}, status=404)

        # Seleccionar una encuesta aleatoria
        random_encuesta = random.choice(encuestas)

        # Crear la respuesta con los datos de la encuesta aleatoria
        data = {
            'Proyecto': random_encuesta.nombre,
            'Fecha': random_encuesta.fecha,
            'Ciudad': random_encuesta.ciudad,
            'Departamento': random_encuesta.departamento,
            'Colegio': random_encuesta.nombre_institucion,
            'Nombre': random_encuesta.nombre_estudiante,
            'Edad': random_encuesta.edad,
            'Prueba': random_encuesta.prueba,
            'Grado': random_encuesta.grado,
            'Genero': random_encuesta.genero,
            'Cuadernillo': random_encuesta.numero_cuadernillo,
            'Respuesta 1': random_encuesta.respuesta_1,
            'Respuesta 2': random_encuesta.respuesta_2,
            'Respuesta 3': random_encuesta.respuesta_3,
            'Respuesta 4': random_encuesta.respuesta_4,
            'Respuesta 5': random_encuesta.respuesta_5,
            'Respuesta 6': random_encuesta.respuesta_6,
            'Respuesta 7': random_encuesta.respuesta_7,
            'Respuesta 8': random_encuesta.respuesta_8,
            'Respuesta 9': random_encuesta.respuesta_9,
            'Respuesta 10': random_encuesta.respuesta_10,
            'Respuesta 11': random_encuesta.respuesta_11,
            'Respuesta 12': random_encuesta.respuesta_12,
            'Respuesta 13': random_encuesta.respuesta_13,
            'Respuesta 14': random_encuesta.respuesta_14,
            'Respuesta 15': random_encuesta.respuesta_15,
            'Respuesta 16': random_encuesta.respuesta_16,
            'Respuesta 17': random_encuesta.respuesta_17,
            'Respuesta 18': random_encuesta.respuesta_18,
            'Respuesta 19': random_encuesta.respuesta_19,
            'Respuesta 20': random_encuesta.respuesta_20,
        }

        return Response(data)

class PreguntaView(APIView):
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación

    def post(self, request):

        data = request.data
        tipo = data.get("tipo")  # Determina el tipo de pregunta

        try:
            if tipo == "mate":
                # Serialización y validación para PreguntaMate
                serializer = PreguntaMateSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "Pregunta de Matemáticas agregada correctamente."}, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            elif tipo == "lengua":
                # Serialización y validación para PreguntaLengua
                serializer = PreguntaLenguaSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "Pregunta de Lenguaje agregada correctamente."}, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({"error": "Tipo de pregunta no válido."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": f"Error al guardar la pregunta: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CuadernillosNombresAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        # Obtener todos los cuadernillos de Matemáticas y Lengua
        cuadernillos_mate = CuadernilloMate.objects.all()
        cuadernillos_lengua = CuadernilloLengua.objects.all()

        # Extraer solo los nombres de los cuadernillos
        nombres = [
            cuadernillo.nombre for cuadernillo in cuadernillos_mate
        ] + [
            cuadernillo.nombre for cuadernillo in cuadernillos_lengua
        ]

        # Devolver la respuesta con todos los nombres de cuadernillos
        return Response(nombres)

class EncuestaDeleteView(APIView):
    permission_classes = [AllowAny]  # Ajusta según tus necesidades

    def post(self, request):
        # Verificar que se envió el ID en los datos
        pk = request.data.get("id")
        if not pk:
            return Response(
                {"error": "ID de la encuesta es obligatorio."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar y eliminar la encuesta
        encuesta = get_object_or_404(Encuesta, pk=pk)
        encuesta.delete()
        return Response(
            {"message": "Encuesta eliminada con éxito."},
            status=status.HTTP_204_NO_CONTENT
        )

class EncuestasResponsableView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        responsable = request.GET.get("responsable")  # Obtener el responsable desde la URL
        print(responsable)
        if responsable:
            # Filtrar las encuestas del responsable
            encuestas = Encuesta.objects.filter(responsable=responsable)
            # Usar el serializer para convertir los datos en formato JSON
            serializer = Encuesta2Serializer(encuestas, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Responsable no proporcionado"}, status=400)

class ObtenerEncuestaAPIView(APIView):
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación
    def get(self, request, pk):
        try:
            encuesta = Encuesta.objects.get(pk=pk)
            serializer = EncuestaSerializer(encuesta)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Encuesta.DoesNotExist:
            return Response({"detail": "Encuesta no encontrada."}, status=status.HTTP_404_NOT_FOUND)

class ModificarEncuestaAPIView(APIView):
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación
    def post(self, request):
        data = request.data
        pk = data.get('id')  # ID de la encuesta
        datos_modificados = data.get('datos')  # Datos modificados

        if not pk or not datos_modificados:
            return Response({"detail": "ID y datos son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            encuesta = Encuesta.objects.get(pk=pk)
        except Encuesta.DoesNotExist:
            return Response({"detail": "Encuesta no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        # Actualizar la encuesta con los nuevos datos
        serializer = EncuestaSerializer(encuesta, data=datos_modificados, partial=True)  # Partial permite actualizar campos específicos
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Encuesta modificada con éxito."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ObtenerInstitucionesAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Obtener parámetros
        proyecto_id = request.GET.get('proyecto_id')
        municipio = request.GET.get('municipio')

        # Validar parámetros
        if not proyecto_id or not municipio:
            return Response({'error': 'Los parámetros proyecto_id y municipio son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar encuestas por proyecto y municipio
        encuestas = Encuesta.objects.filter(nombre=proyecto_id, ciudad=municipio)

        # Extraer instituciones únicas
        instituciones = set(encuestas.values_list('nombre_institucion', flat=True))

        # Convertir el set a lista
        instituciones_list = list(instituciones)

        # Retornar respuesta
        return Response(instituciones_list, status=status.HTTP_200_OK)

class ObtenerMunicipiosAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        proyecto_id = request.GET.get('proyecto_id')

        if not proyecto_id:
            return Response({'error': 'El parámetro proyecto_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar las encuestas asociadas al proyecto
        encuestas = Encuesta.objects.filter(nombre=proyecto_id)

        # Extraer los municipios únicos
        municipios = set(encuestas.values_list('ciudad', flat=True))  # O usa 'municipio' si tienes ese campo

        resultado = []
        for municipio in municipios:
            resultado.append(municipio)

        return Response(resultado, status=status.HTTP_200_OK)

class GenerarReporte1APIIew(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            institucion = request.GET.get('institucion')
            proyecto = request.GET.get('proyecto')
            aplicacion = request.GET.get('aplicacion')
            tercero_entrada = int(request.GET.get('matriculados_tercero'))
            quinto_entrada = int(request.GET.get('matriculados_quinto'))
            res = request.GET.get('dane')

            if not institucion or not proyecto or not aplicacion:
                return Response({
                    "error": "Faltan parámetros: aplicacion, institucion y proyecto son requeridos"
                }, status=400)

            encuestas = Encuesta.objects.filter(
                aplicacion=aplicacion,
                nombre_institucion=institucion,
                nombre=proyecto
            )

            if not encuestas.exists():
                return Response({
                    "error": "No se encontraron encuestas para los filtros proporcionados."
                }, status=404)

            ciudad = ''
            fecha_aplicacion = ''
            # Preparar los datos
            ter = []
            quin = []
            for encuesta in encuestas:
                grado = encuesta.grado or "N/A"
                if grado == 'Tercero':
                    ter.append(grado)
                elif grado == 'Quinto':
                    quin.append(grado)
                ciudad = encuesta.ciudad
                fecha_aplicacion = encuesta.fecha

            buffer = BytesIO()

            # Crear el documento
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            
            # Estilo verde centrado
            titulo_style = ParagraphStyle(
                name="TituloVerdeCentrado",
                alignment=TA_CENTER,
                fontSize=18,
                textColor=HexColor("#1B8830"),
                leading=22,
                spaceAfter=12
            )

            subtitulo_style = ParagraphStyle(
                name="SubtituloVerdeCentrado",
                alignment=TA_CENTER,
                fontSize=14,
                textColor=HexColor("#1B8830"),
                leading=20,
                spaceAfter=6
            )

            descripcion_style = ParagraphStyle(
                name="DescripcionVerdeCentrada",
                alignment=TA_CENTER,
                fontSize=12,
                textColor=HexColor("#1B8830"),
                leading=16
            )

            parrafo_estilo = ParagraphStyle(
                name='IntroJustificado',
                fontName='Helvetica',
                fontSize=10.5,
                leading=14,
                textColor=colors.black,
                alignment=4,  # Justificado
                spaceAfter=20,
                leftIndent=10,
                rightIndent=10,
            )

            parrafo_estilo2 = ParagraphStyle(
                name='IntroIzquierda',
                fontName='Helvetica',
                fontSize=10.5,
                leading=14,
                textColor=colors.black,
                alignment=TA_LEFT,
                spaceAfter=20,
                leftIndent=10,
                rightIndent=10,
            )

            parrafo_estilo3 = ParagraphStyle(
                name='IntroCentradoVerde',
                fontName='Helvetica',
                fontSize=10.5,
                leading=14,
                textColor=HexColor("#33A652"),  # Color verde personalizado
                alignment=TA_CENTER,            # Texto centrado
                spaceAfter=20,
                leftIndent=10,
                rightIndent=10,
            )

            parrafo_estilo4 = ParagraphStyle(
                name='IntroCentradoVerde',
                fontName='Helvetica',
                fontSize=10.5,
                leading=14,
                textColor=HexColor("#ffffff"),  # Color verde personalizado
                alignment=TA_CENTER,            # Texto centrado
                spaceAfter=20,
                leftIndent=10,
                rightIndent=10,
            )

            descripcion_izq_style = ParagraphStyle(
                name="DescripcionIzquierda",
                alignment=TA_LEFT,
                fontSize=12,
                textColor=HexColor("#1B8830"),
                leading=16,
                spaceBefore=12,
                spaceAfter=8,
            )

            recuadro_style = ParagraphStyle(
                name="RecuadroJustificado",
                fontSize=10.5,
                leading=14,
                alignment=4,  # Justificado
                textColor=colors.black,
            )

            # Contenido
            titulo_texto = f"""
            <b>Reporte de resultados para la instutución</b><br/>
            <b>{institucion} - Aplicación: {str(aplicacion).title()}</b>
            """

            subtitulo_texto = "<b>Programa Escuelas que Aprenden®</b>"
            descripcion_texto = f"<b>Reporte de resultados de la institución educativa {institucion} en las pruebas de Lenguaje y Matemáticas – aplicación de {aplicacion}</b>"
            
            # Insertar en elementos
            elements.append(Spacer(1, 200))  # Centrar verticalmente
            elements.append(Paragraph(titulo_texto, titulo_style))
            elements.append(Spacer(1, 10))
            elements.append(PageBreak())
            elements.append(Paragraph(subtitulo_texto, subtitulo_style))
            elements.append(Paragraph(descripcion_texto, descripcion_style))

            contenido =  f"""Este reporte contiene los resultados de la institución educativa en la <b><u>aplicación de
                            {aplicacion}</u></b> de las pruebas de Lenguaje y Matemáticas presentadas por una muestra
                            representativa de estudiantes de tercero y quinto grados.<br/><br/>
                            Para cada grado y área se presentan los siguientes tipos de resultados, tanto de la
                            institución educativa como del conjunto de los establecimientos educativos del municipio
                            que están participando en el programa Escuelas que Aprenden (EQA), con el fin de
                            posibilitar la realización de algunas comparaciones:<br/><br/>
                            • Puntaje promedio<br/>
                            • Desviación estándar<br/>
                            • Puntaje mínimo<br/>
                            • Puntaje máximo<br/>
                            • Distribución porcentual de los estudiantes según niveles de desempeño<br/><br/>

                            Esperamos que esta información sea de utilidad para que la institución educativa conozca
                            las fortalezas de sus estudiantes en las áreas evaluadas y, a partir de ello, establezca
                            estrategias pedagógicas necesarias para lograr que todos alcancen o superen los
                            desempeños esperados.

                            """
    

            contenido_parrafo = Paragraph(contenido, recuadro_style)
            recuadro_tabla = Table([[contenido_parrafo]], colWidths=[460])

            # Estilos de la tabla
            recuadro_tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#A4D7B2")),
                ('BOX', (0, 0), (0, 0), 0.5, colors.HexColor("#1B8830")),
                ('LEFTPADDING', (0, 0), (0, 0), 10),
                ('RIGHTPADDING', (0, 0), (0, 0), 10),
                ('TOPPADDING', (0, 0), (0, 0), 6),
                ('BOTTOMPADDING', (0, 0), (0, 0), 6),
            ]))

            # Añádelo a la lista de elementos
            elements.append(Spacer(1, 5))
            elements.append(recuadro_tabla)
            elements.append(Spacer(1, 5))
            
            descripcion_texto = '<b>1. Datos de identificación de la institución educativa</b>'

            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))

            # Cambio de formato fecha 
            nFecha = fecha_aplicacion.strftime("%d-%m-%Y")

            # Datos de la tabla
            resumen_data = [
                ['Ciudad:', ciudad],
                ['Institución educativa:', institucion],
                ['Código DANE:', res],
                ['Fecha de aplicación:', nFecha],
                ['Tipo de aplicación:', str(aplicacion).title()],
            ]

            # Crear tabla de resumen
            tabla_resumen = Table(resumen_data, colWidths=[130, 220])
            tabla_resumen.setStyle(TableStyle([
                ('TEXTCOLOR', (0, 0), (0, -1), HexColor("#1B8830")),  # columna izquierda verde
                ('TEXTCOLOR', (1, 0), (1, -1), colors.black),         # columna derecha negra
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                # Optional borders:
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey)
            ]))

            # Añadir a los elementos después del texto introductorio
            elements.append(tabla_resumen)
            elements.append(Spacer(1, 5))

            descripcion_texto = '<b>2. Ficha técnica: número de estudiantes matriculados y evaluados</b>'

            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))
            
            
            c = self.tabla_inicial(tercero_entrada, len(ter), quinto_entrada, len(quin))

            tabla_datos = [
                ["Grado", "Total matriculados", "Total evaluados", "%"], # Encabezados
                ["Tercero", tercero_entrada, len(ter), f"{self.comma_dot(c[0])}%"],  # Fila 1
                ["Quinto ", quinto_entrada, len(quin), f"{self.comma_dot(c[1])}%"],  # Fila 2
                ["Total", tercero_entrada+quinto_entrada , len(ter)+len(quin), f"{self.comma_dot(c[2])}%"],  # Fila 3
            ]

            # Crear la tabla
            tabla_estadistica = Table(tabla_datos, colWidths=[70, 100, 100, 70])
            tabla_estadistica.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor("#1B8830")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),

            ]))

            elements.append(Spacer(1, 5))
            elements.append(tabla_estadistica)
            elements.append(Spacer(1, 10))

            #----------------------------------------------------------------------------------------------------------------------------

            descripcion_texto = '<b>3. Resultados en la prueba de Lenguaje</b>'

            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))

            contenido = """
            <b><font color='#1B8830'>Qué se evalúa:</font></b><br/><br/>
            Las pruebas de Lenguaje evalúan las habilidades de los estudiantes de tercero y quinto grados para interpretar y comprender diversos tipos y formatos de textos orientados a diferentes propósitos.<br/><br/>
            Los tipos de textos evaluados son los siguientes: narrativos, descriptivos, dialogales, explicativos y argumentativos.<br/><br/>
            Los formatos de textos evaluados son los siguientes: continuos (organizados en forma de párrafos) y discontinuos (organizados de manera gráfica y no lineal).<br/><br/>
            Las pruebas abordan tres niveles de comprensión textual:.<br/><br/>
            • <b>Literal:</b> implica reconocer el significado explícito dentro de un texto.<br/>
            • <b>Inferencial:</b> implica reconocer el significado implícito de los contenidos en un texto.<br/>
            • <b>Crítica:</b> implica evaluar los contenidos y las formas de los textos, así como hacer una valoración de argumentos.<br/>
            """

            contenido_parrafo = Paragraph(contenido, recuadro_style)
            recuadro_tabla = Table([[contenido_parrafo]], colWidths=[460])

            # Estilos de la tabla
            recuadro_tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#A4D7B2")),
                ('BOX', (0, 0), (0, 0), 0.5, colors.HexColor("#1B8830")),  # Borde más delgado y color personalizado
                ('LEFTPADDING', (0, 0), (0, 0), 10),
                ('RIGHTPADDING', (0, 0), (0, 0), 10),
                ('TOPPADDING', (0, 0), (0, 0), 6),
                ('BOTTOMPADDING', (0, 0), (0, 0), 6),
            ]))

            # Añádelo a la lista de elementos
            elements.append(Spacer(1, 12))
            elements.append(recuadro_tabla)
            elements.append(Spacer(1, 20))

            #-----------------------------------------------------------------------------------------------------------------------

            descripcion_texto = '<b>3.1. Tercer grado </b><br/><b>a. Puntaje</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))

            contenido =  f"""
                            <b>Los puntajes se presentan en una escala de 0 a 20 puntos.</b><br/><br/>
                            <b>La media (o puntaje promedio)</b> se obtiene de sumar los puntajes obtenidos por cada
                            estudiante y dividir ese total por el número de estudiantes evaluados. Permite establecer
                            cuál fue el puntaje más representativo de los estudiantes en la prueba.<br/><br/>

                            La <b>desviación estándar</b> permite conocer la magnitud en la cual la mayoría de los
                            puntajes se alejan, “hacia arriba” o “hacia abajo”, del promedio. Un menor valor de la
                            desviación estándar quiere decir que la distribución de los estudiantes es más
                            homogénea, o sea, que la mayoría obtuvo puntajes similares. Por el contrario, un alto
                            valor significa mayor heterogeneidad: mientras algunos obtuvieron puntajes muy altos,
                            otros sacaron puntajes muy bajos.<br/><br/>

                            El <b>puntaje mínimo</b> corresponde al menor valor de puntuación obtenido en el grupo de
                            estudiantes evaluados. A su vez, el <b>puntaje máximo</b> corresponde al mayor valor de
                            puntuación obtenido por ese grupo.
                            """
    

            contenido_parrafo = Paragraph(contenido, recuadro_style)
            recuadro_tabla = Table([[contenido_parrafo]], colWidths=[460])

            # Estilos de la tabla
            recuadro_tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#A4D7B2")),
                ('BOX', (0, 0), (0, 0), 0.5, colors.HexColor("#1B8830")),
                ('LEFTPADDING', (0, 0), (0, 0), 10),
                ('RIGHTPADDING', (0, 0), (0, 0), 10),
                ('TOPPADDING', (0, 0), (0, 0), 6),
                ('BOTTOMPADDING', (0, 0), (0, 0), 6),
            ]))

            # Añádelo a la lista de elementos
            elements.append(Spacer(1, 12))
            elements.append(recuadro_tabla)
            elements.append(Spacer(1, 20))


            t = self.tabla(0, institucion, aplicacion, proyecto, 3, 'L')
            c = self.tabla(1, institucion, aplicacion, proyecto, 3, 'L')
            
            tabla_datos = [
                ["", "# evaluados", "Media", "Desv. est.", "Mínimo", "Máximo"],  # Encabezados
                ["Institución educativa", t[0], self.comma_dot(t[1]), self.comma_dot(t[2]), t[3], t[4]],  # Fila 1
                ["Agregado del municipio", c[0], self.comma_dot(c[1]), self.comma_dot(c[2]), c[3], c[4]],  # Fila 2 
            ]

            # Crear la tabla
            tabla_estadistica = Table(tabla_datos, colWidths=[130, 70, 50, 70, 50, 50])
            tabla_estadistica.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor("#1B8830")),  # Fondo verde para encabezados
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),          # Texto blanco en encabezados
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),          # Líneas de tabla
            ]))

            elements.append(Spacer(1, 12))
            elements.append(tabla_estadistica)
            elements.append(Spacer(1, 20))

            

            descripcion_texto = '<b>b. Descripción</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))

            contenido =  f"""
                            Los <b>niveles de desempeño</b> muestran la distribución porcentual de los estudiantes según
                            los desempeños alcanzados en cada una de las pruebas. Además, describen lo que ellos
                            saben y saben hacer, y permiten conocer cómo se encuentran en relación con la
                            capacidad para resolver problemas de distintos niveles de complejidad.<br/><br/>
                            <b>Se establecieron tres niveles de desempeño: bajo, medio y alto.</b><br/><br/>
                            Estos niveles de desempeño son <b>específicos</b>, <b>jerárquicos</b> e <b>inclusivos</b>. Esto quiere
                            decir que son definidos para cada prueba, tienen una complejidad creciente y que, para
                            ubicarse en un determinado nivel, es necesario haber superado los niveles anteriores.<br/><br/>
                            
                            <b>Nota:</b> la suma de los porcentajes puede no ser exactamente 100% debido a
                            aproximaciones realizadas entre cifras decimales.<br/>
                            """
    

            contenido_parrafo = Paragraph(contenido, recuadro_style)
            recuadro_tabla = Table([[contenido_parrafo]], colWidths=[460])

            # Estilos de la tabla
            recuadro_tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#A4D7B2")),
                ('BOX', (0, 0), (0, 0), 0.5, colors.HexColor("#1B8830")),
                ('LEFTPADDING', (0, 0), (0, 0), 10),
                ('RIGHTPADDING', (0, 0), (0, 0), 10),
                ('TOPPADDING', (0, 0), (0, 0), 6),
                ('BOTTOMPADDING', (0, 0), (0, 0), 6),
            ]))

            # Añádelo a la lista de elementos
            elements.append(Spacer(1, 12))
            elements.append(recuadro_tabla)
            elements.append(Spacer(1, 20)) 

            # Datos del gráfico
            niveles = ['Bajo', 'Medio', 'Alto']
            t = self.desempeño(0, institucion, aplicacion, proyecto, 3, 'L', 5, 13)
            c = self.desempeño(1, institucion, aplicacion, proyecto, 3, 'L', 5, 13)

            # Posiciones para barras
            x = range(len(niveles))
            bar_width = 0.35

            # Crear gráfico
            plt.figure(figsize=(6, 5))
            bars1 = plt.bar([i - bar_width/2 for i in x], t, width=bar_width, label='Institución', color='#1B8830')
            bars2 = plt.bar([i + bar_width/2 for i in x], c, width=bar_width, label='Ciudad', color='#6FBF73')

            # Agregar etiquetas encima de las barras
            for i, bar in enumerate(bars1):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{t[i]}%', ha='center', va='bottom', fontsize=10)

            for i, bar in enumerate(bars2):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{c[i]}%', ha='center', va='bottom', fontsize=10)

            # Ajustes del gráfico
            plt.xticks(x, niveles)
            plt.title('Distribución por Niveles de Desempeño\n')
            plt.legend()
            plt.tight_layout()

            # QUITAR eje Y
            plt.gca().axes.get_yaxis().set_visible(False)

            # QUITAR TODOS LOS BORDES, excepto abajo
            for spine in ['top', 'right', 'left']:
                plt.gca().spines[spine].set_visible(False)

            # Guardar a un archivo temporal en memoria
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png')
            plt.close()
            img_buffer.seek(0)

            # Insertar imagen en el PDF (usando ReportLab Image)
            grafico = RLImage(img_buffer, width=400, height=300)
            elements.append(Spacer(1, 12))
            elements.append(grafico)
            elements.append(Spacer(1, 20))
            
            

            descripcion_texto = '<b>Significado de los niveles de desempeño – Lenguaje, tercer grado</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style)) 

            # Tabla descriptiva de niveles de desempeño
            niveles_data = [
                [
                    Paragraph("Nivel", parrafo_estilo3),
                    Paragraph("Descripción", parrafo_estilo3)
                ],
                [
                    Paragraph("<b>Bajo<br/>(entre 1 y 4 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Los estudiantes ubicados en este nivel de desempeño:</b><br/>
                            • Tienen una comprensión básica pero significativa del lenguaje, al reconocer
                            sinónimos y antónimos.<br/>
                            • Comparan textos con diferentes formatos y finalidades.""", parrafo_estilo2)
                ],
                [
                    Paragraph("<b>Medio<br/>(entre 5 y 12 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Además de lo descrito en el nivel anterior, los estudiantes ubicados en este nivel:</b><br/>

                            • Comprenden tanto el significado literal como el implícito de un texto:
                            identifican su estructura, intención y relaciones internas.<br/>
                            • Reconocen el significado de palabras dentro del contexto de un enunciado
                            en situaciones comunicativas específicas.<br/>
                            • Identifican elementos estructurales y narrativos clave: la voz del narrador,
                            los personajes, los escenarios donde se desarrollan los hechos y la
                            secuencia lógica de las acciones.<br/>
                            • Relacionan el título con el contenido de textos explicativos y argumentativos.<br/>
                            • Parafrasean proposiciones presentadas en los textos.<br/>
                            • Identifican causas, consecuencias, problemas y soluciones planteadas en los textos.<br/>
                            • Hacen deducciones a partir de información implícita.<br/>
                            """, parrafo_estilo2)
                ],
                [
                    Paragraph("<b>Alto<br/>(entre 13 y 20 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Además de lo descrito en los niveles anteriores, los estudiantes ubicados en este nivel:</b><br/>
                            • Identifican con claridad una secuencia discursiva.<br/>
                            • Comprenden la relación entre el título y el contenido de diversos tipos de
                            texto.<br/>
                            • Deducen el tema central a partir de información implícita.<br/>
                            • Reconocen en qué personaje se enfoca la acción.<br/>
                            • Parafrasean fragmentos narrativos.<br/>
                            • Vinculan el contexto de producción de un texto con sus propios saberes.<br/>
                            • Establecen relaciones entre textos y discriminan estructuras argumentativas
                            con claridad.<br/>
                            • Formulan hipótesis de lectura para construir un sentido global del texto.<br/>
                            • Interpretan textos que integran lenguaje verbal e imágenes, evidenciando
                            una lectura multimodal efectiva.<br/>
                            """, parrafo_estilo2)
                ],
            ]

            tabla_niveles = Table(niveles_data, colWidths=[80, 400])
            tabla_niveles.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10.5),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('LINEBELOW', (0, 0), (-1, -2), 0.25, colors.grey),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey)
            ]))

            elements.append(Spacer(1, 12))
            elements.append(tabla_niveles)

            parrafo_intro = Paragraph(
                "<b>Nota:</b> el Anexo 1 contiene las descripciones más detalladas de estos niveles de desempeño; por tanto, se recomienda su consulta y análisis.",
                parrafo_estilo
            )

            elements.append(Spacer(1, 12))
            elements.append(parrafo_intro) 
            

            #-----------------------------------------------------------------------------------------------------------------------

            descripcion_texto = '<b>3.2. Quinto grado </b><br/><b>a. Puntaje</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))

              
            t = self.tabla(0, institucion, aplicacion, proyecto, 5, 'L')
            c = self.tabla(1, institucion, aplicacion, proyecto, 5, 'L')
            
            tabla_datos = [
                ["", "# evaluados", "Media", "Desv. est.", "Mínimo", "Máximo"],  # Encabezados
                ["Instución educativa", t[0], self.comma_dot(t[1]), self.comma_dot(t[2]), t[3], t[4]],  # Fila 1
                ["Agregado del municipio", c[0], self.comma_dot(c[1]), self.comma_dot(c[2]), c[3], c[4]],  # Fila 2 
            ]

            # Crear la tabla
            tabla_estadistica = Table(tabla_datos, colWidths=[130, 70, 50, 70, 50, 50])
            tabla_estadistica.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor("#1B8830")),  # Fondo verde para encabezados
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),          # Texto blanco en encabezados
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),          # Líneas de tabla
            ]))

            elements.append(Spacer(1, 12))
            elements.append(tabla_estadistica)
            elements.append(Spacer(1, 20))

            

            descripcion_texto = '<b>b. Descripción</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))

            # Datos del gráfico
            niveles = ['Bajo', 'Medio', 'Alto']
            t = self.desempeño(0, institucion, aplicacion, proyecto, 5, 'L', 7, 14)
            c = self.desempeño(1, institucion, aplicacion, proyecto, 5, 'L', 7, 14)

            # Posiciones para barras
            x = range(len(niveles))
            bar_width = 0.35

            # Crear gráfico
            plt.figure(figsize=(6, 5))
            bars1 = plt.bar([i - bar_width/2 for i in x], t, width=bar_width, label='Institución', color='#1B8830')
            bars2 = plt.bar([i + bar_width/2 for i in x], c, width=bar_width, label='Ciudad', color='#6FBF73')

            # Agregar etiquetas encima de las barras
            for i, bar in enumerate(bars1):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{t[i]}%', ha='center', va='bottom', fontsize=10)

            for i, bar in enumerate(bars2):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{c[i]}%', ha='center', va='bottom', fontsize=10)

            # Ajustes del gráfico
            plt.xticks(x, niveles)
            plt.title('Distribución por Niveles de Desempeño\n')
            plt.legend()
            plt.tight_layout()

            # QUITAR eje Y
            plt.gca().axes.get_yaxis().set_visible(False)

            # QUITAR TODOS LOS BORDES, excepto abajo
            for spine in ['top', 'right', 'left']:
                plt.gca().spines[spine].set_visible(False)

            # Guardar a un archivo temporal en memoria
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png')
            plt.close()
            img_buffer.seek(0)

            # Insertar imagen en el PDF (usando ReportLab Image)
            grafico = RLImage(img_buffer, width=400, height=300)
            elements.append(Spacer(1, 12))
            elements.append(grafico)
            elements.append(Spacer(1, 20))

            

            descripcion_texto = '<b>Significado de los niveles de desempeño – Lenguaje, quinto grado</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style)) 

            # Tabla descriptiva de niveles de desempeño
            niveles_data = [
                [
                    Paragraph("Nivel", parrafo_estilo3),
                    Paragraph("Descripción", parrafo_estilo3)
                ],
                [
                    Paragraph("<b>Bajo<br/>(entre 1 y 6 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Los estudiantes ubicados en este nivel de desempeño:</b><br/><br/>
                            • <b>Reconocen léxico básico:</b> identifican el uso de sinónimos y antónimos
                            para ampliar su vocabulario.<br/>
                            • <b>Comprenden la relación título-contenido:</b> identifican la relación entre el
                            título y el contenido en textos narrativos.<br/>
                            • <b>Interpretan aspectos básicos de textos visuales:</b> relacionan textos
                            compuestos por imágenes e interpretan su significado.
                            """, parrafo_estilo2)
                ],
                [
                    Paragraph("<b>Medio<br/>(entre 7 y 13 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            Además de lo descrito en el nivel anterior, los estudiantes ubicados en este nivel:<br/><br/>
                            • <b>Identifican elementos textuales básicos:</b> reconocen personajes,
                            secuencia de acciones, tipo de texto por su estructura y la relación entre
                            título y contenido en diversos tipos de textos.<br/>
                            • <b>Comprenden la acción y el tema:</b> identifican el foco de la acción en
                            narrativas y deducen el tema implícito en descripciones.<br/>
                            • <b>Procesan y relacionan información:</b> parafrasean oraciones, relacionan
                            textos con saberes previos y discriminan tema e idea principal para conectar
                            textos.<br/>
                            • <b>Analizan y comparan textos:</b> elaboran hipótesis de lectura, comparan
                            textos por formato y finalidad, identifican elementos argumentativos (causas,
                            consecuencias, etc.) y distinguen tipos de descripción según la perspectiva
                            del autor.
                            """, parrafo_estilo2)
                ],
                [
                    Paragraph("<b>Alto<br/>(entre 14 y 20 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Además de lo descrito en los niveles anteriores, los estudiantes ubicados
                            en este nivel:</b><br/><br/>
                            
                            • <b>Comprenden vocabulario contextual:</b> reconocen el significado de
                            palabras dentro de enunciados específicos en el texto, y también identifican
                            el significado del vocabulario en situaciones comunicativas.<br/>
                            • <b>Identifican</b> la voz narrativa en una historia.<br/>
                            • <b>Relacionan título-contenido en textos descriptivos:</b> identifican la relación
                            entre el título y el contenido de un texto descriptivo.
                            """, parrafo_estilo2)
                ],
            ]

            tabla_niveles = Table(niveles_data, colWidths=[80, 400])
            tabla_niveles.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10.5),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('LINEBELOW', (0, 0), (-1, -2), 0.25, colors.grey),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey)
            ]))

            elements.append(Spacer(1, 12))
            elements.append(tabla_niveles)

            parrafo_intro = Paragraph(
                "<b>Nota:</b> el Anexo 2 contiene las descripciones más detalladas de estos niveles de desempeño; por tanto, se recomienda su consulta y análisis.",
                parrafo_estilo
            )

            elements.append(Spacer(1, 12))
            elements.append(parrafo_intro)
            elements.append(PageBreak()) 

            #-----------------------------------------------------------------------------------------------------------------------
            
            descripcion_texto = '<b>4. Resultados en la prueba de Matemáticas</b>'

            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))

            contenido = """
            <b><font color='#1B8830'>Qué se evalúa:</font></b><br/><br/>
            Las pruebas de Matemáticas evalúan las habilidades de los estudiantes de tercero y quinto grados para plantear y resolver 
            diferentes tipos de problemas matemáticos teniendo en cuenta las siguientes competencias y componentes, establecidos en los 
            estándares básicos de competencias del Ministerio de Educación Nacional:.<br/><br/>
            <b><font color='#1B8830'>Competencias:</font></b><br/><br/>
            • <b><font color='#1B8830'>Comunicación, modelación y representación:</font></b>implica comprender cómo se presenta una información matemática y elaborar representaciones que permitan hacer comprensible dicha información a otros.<br/>
            • <b><font color='#1B8830'>Planteamiento y resolución de problemas:</font></b>implica comprender la utilidad del conocimiento disponible.<br/>
            • <b><font color='#1B8830'>Razonamiento y argumentación:</font></b>implica hacer una valoración sobre la adecuación de unos pasos realizados o para establecer la veracidad de lo que se afirma, entre otros.<br/><br/>
            <b><font color='#1B8830'>Componentes:</font></b><br/><br/>
            • Númerico - variacional<br/>
            • Espacial - métrico<br/>
            • Aleatorio<br/><br/>
            """

            contenido_parrafo = Paragraph(contenido, recuadro_style)
            recuadro_tabla = Table([[contenido_parrafo]], colWidths=[460])

            # Estilos de la tabla
            recuadro_tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#A4D7B2")),
                ('BOX', (0, 0), (0, 0), 0.5, colors.HexColor("#1B8830")),  # Borde más delgado y color personalizado
                ('LEFTPADDING', (0, 0), (0, 0), 10),
                ('RIGHTPADDING', (0, 0), (0, 0), 10),
                ('TOPPADDING', (0, 0), (0, 0), 6),
                ('BOTTOMPADDING', (0, 0), (0, 0), 6),
            ]))

            # Añádelo a la lista de elementos
            elements.append(Spacer(1, 12))
            elements.append(recuadro_tabla)
            elements.append(Spacer(1, 20))

            #-----------------------------------------------------------------------------------------------------------------------

            descripcion_texto = '<b>4.1. Tercer grado</b><br/><b>a. Puntaje</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))
  
            t = self.tabla(0, institucion, aplicacion, proyecto, 3, 'M')
            c = self.tabla(1, institucion, aplicacion, proyecto, 3, 'M')
            
            tabla_datos = [
                ["", "# evaluados", "Media", "Desv. est.", "Mínimo", "Máximo"],  # Encabezados
                ["Instución educativa", t[0], self.comma_dot(t[1]), self.comma_dot(t[2]), t[3], t[4]],  # Fila 1
                ["Agregado del municipio", c[0], self.comma_dot(c[1]), self.comma_dot(c[2]), c[3], c[4]],  # Fila 2 
            ]
            

            # Crear la tabla
            tabla_estadistica = Table(tabla_datos, colWidths=[130, 70, 50, 70, 50, 50])
            tabla_estadistica.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor("#1B8830")),  # Fondo verde para encabezados
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),          # Texto blanco en encabezados
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),          # Líneas de tabla
            ]))

            elements.append(Spacer(1, 12))
            elements.append(tabla_estadistica)
            elements.append(Spacer(1, 20))

            
            descripcion_texto = 'b. Descripción'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))  

            # Datos del gráfico
            niveles = ['Bajo', 'Medio', 'Alto']
            t = self.desempeño(0, institucion, aplicacion, proyecto, 3, 'M', 7, 14)
            c = self.desempeño(1, institucion, aplicacion, proyecto, 3, 'M', 7, 14)

            # Posiciones para barras
            x = range(len(niveles))
            bar_width = 0.35

            # Crear gráfico
            plt.figure(figsize=(6, 5))
            bars1 = plt.bar([i - bar_width/2 for i in x], t, width=bar_width, label='Institución', color='#1B8830')
            bars2 = plt.bar([i + bar_width/2 for i in x], c, width=bar_width, label='Ciudad', color='#6FBF73')

            # Agregar etiquetas encima de las barras
            for i, bar in enumerate(bars1):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{t[i]}%', ha='center', va='bottom', fontsize=10)

            for i, bar in enumerate(bars2):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{c[i]}%', ha='center', va='bottom', fontsize=10)

            # Ajustes del gráfico
            plt.xticks(x, niveles)
            plt.title('Distribución por Niveles de Desempeño\n')
            plt.legend()
            plt.tight_layout()

            # QUITAR eje Y
            plt.gca().axes.get_yaxis().set_visible(False)

            # QUITAR TODOS LOS BORDES, excepto abajo
            for spine in ['top', 'right', 'left']:
                plt.gca().spines[spine].set_visible(False)

            # Guardar a un archivo temporal en memoria
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png')
            plt.close()
            img_buffer.seek(0)

            # Insertar imagen en el PDF (usando ReportLab Image)
            grafico = RLImage(img_buffer, width=400, height=300)
            elements.append(Spacer(1, 12))
            elements.append(grafico)
            elements.append(Spacer(1, 20))

            

            descripcion_texto = '<b>Significado de los niveles de desempeño – Matemáticas, tercer grado</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style)) 

            # Tabla descriptiva de niveles de desempeño
            niveles_data = [
                [
                    Paragraph("Nivel", parrafo_estilo3),
                    Paragraph("Descripción", parrafo_estilo3)
                ],
                [
                    Paragraph("<b>Bajo<br/>(entre 1 y 6 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Los estudiantes ubicados en este nivel de desempeño:</b><br/><br/>
                            • Resuelven problemas rutinarios con apoyo, aplicando algoritmos de forma
                            guiada y utilizando herramientas básicas como fracciones simples,
                            secuencias numéricas y unidades de medida estandarizadas.<br/>
                            • Demuestran una comprensión inicial de conceptos elementales, aunque su
                            razonamiento presenta limitaciones.<br/>
                            • Siguen patrones mecánicos, cometen errores frecuentes y requieren
                            reforzar la argumentación y la conexión entre ideas matemáticas.
                            """, parrafo_estilo2)
                ],
                [
                    Paragraph("<b>Medio<br/>(entre 7 y 13 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Además de lo descrito en el nivel anterior, los estudiantes ubicados en
                            este nivel:</b><br/><br/>
                            • Resuelven problemas estándar: aplican adecuadamente los conceptos y
                            justifican los pasos con cierto rigor, comunicando soluciones claras, aunque
                            con margen para profundizar.<br/>
                            • Demuestran comprensión en problemas multiplicativos.<br/>
                            • Seleccionan unidades de medida adecuadas.<br/>
                            • Reconocen movimientos de figuras.<br/>
                            • Determinan áreas mediante patrones de recubrimiento.<br/>
                            • Identifican patrones de cambio.<br/>
                            • Estiman probabilidades simples.
                            """, parrafo_estilo2)
                ],
                [
                    Paragraph("<b>Alto<br/>(entre 14 y 20 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Además de lo descrito en los niveles anteriores, los estudiantes ubicados
                            en este nivel:</b><br/><br/>
                            • Resuelven problemas compuestos y no rutinarios mediante estrategias
                            innovadoras, integrando múltiples conceptos, argumentando con precisión,
                            utilizando lenguaje técnico y demostrando pensamiento crítico y creativo en
                            sus respuestas.<br/>
                            • Resuelven problemas con transformaciones.<br/>
                            • Analizan frecuencias y toman decisiones fundamentadas en medidas
                            estadísticas como la moda.<br/>
                            """, parrafo_estilo2)
                ],
            ]

            tabla_niveles = Table(niveles_data, colWidths=[80, 400])
            tabla_niveles.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10.5),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('LINEBELOW', (0, 0), (-1, -2), 0.25, colors.grey),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey)
            ]))

            elements.append(Spacer(1, 12))
            elements.append(tabla_niveles)

            parrafo_intro = Paragraph(
                "<b>Nota:</b> el Anexo 3 contiene las descripciones más detalladas de estos niveles de desempeño; por tanto, se recomienda su consulta y análisis.",
                parrafo_estilo
            )

            elements.append(Spacer(1, 12))
            elements.append(parrafo_intro) 
            
            #-----------------------------------------------------------------------------------------------------------------------

            descripcion_texto = '<b>4.2. Quinto grado </b><br/><b>a. Puntaje</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))

            parrafo_intro = Paragraph(
                "Espacio estático para incluir un texto, pendiente de construir, para explicar que el puntaje se presenta en una escala de 0 a 20 puntos, qué es el promedio y la desviación estándar (dos párrafos cortos como máximo).",
                parrafo_estilo
            )

            elements.append(Spacer(1, 12))
            elements.append(parrafo_intro)   
            t = self.tabla(0, institucion, aplicacion, proyecto, 5, 'M')
            c = self.tabla(1, institucion, aplicacion, proyecto, 5, 'M')

            tabla_datos = [
                ["", "# evaluados", "Media", "Desv. est.", "Mínimo", "Máximo"],  # Encabezados
                ["Instución educativa", t[0], self.comma_dot(t[1]), self.comma_dot(t[2]), t[3], t[4]],  # Fila 1
                ["Agregado del municipio", c[0], self.comma_dot(c[1]), self.comma_dot(c[2]), c[3], c[4]],  # Fila 2 
            ]

            # Crear la tabla
            tabla_estadistica = Table(tabla_datos, colWidths=[130, 70, 50, 70, 50, 50])
            tabla_estadistica.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor("#1B8830")),  # Fondo verde para encabezados
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),          # Texto blanco en encabezados
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),          # Líneas de tabla
            ]))

            elements.append(Spacer(1, 12))
            elements.append(tabla_estadistica)
            elements.append(Spacer(1, 20))

            

            descripcion_texto = '<b>b. Descripción</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))

              

            # Datos del gráfico
            niveles = ['Bajo', 'Medio', 'Alto']
            t = self.desempeño(0, institucion, aplicacion, proyecto, 5, 'M', 6, 12)
            c = self.desempeño(1, institucion, aplicacion, proyecto, 5, 'M', 6, 12)

            # Posiciones para barras
            x = range(len(niveles))
            bar_width = 0.35

            # Crear gráfico
            plt.figure(figsize=(6, 5))
            bars1 = plt.bar([i - bar_width/2 for i in x], t, width=bar_width, label='Institución', color='#1B8830')
            bars2 = plt.bar([i + bar_width/2 for i in x], c, width=bar_width, label='Ciudad', color='#6FBF73')

            # Agregar etiquetas encima de las barras
            for i, bar in enumerate(bars1):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{t[i]}%', ha='center', va='bottom', fontsize=10)

            for i, bar in enumerate(bars2):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{c[i]}%', ha='center', va='bottom', fontsize=10)

            # Ajustes del gráfico
            plt.xticks(x, niveles)
            plt.title('Distribución por Niveles de Desempeño\n')
            plt.legend()
            plt.tight_layout()

            # QUITAR eje Y
            plt.gca().axes.get_yaxis().set_visible(False)

            # QUITAR TODOS LOS BORDES, excepto abajo
            for spine in ['top', 'right', 'left']:
                plt.gca().spines[spine].set_visible(False)

            # Guardar a un archivo temporal en memoria
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png')
            plt.close()
            img_buffer.seek(0)

            # Insertar imagen en el PDF (usando ReportLab Image)
            grafico = RLImage(img_buffer, width=400, height=300)
            elements.append(Spacer(1, 12))
            elements.append(grafico)
            elements.append(Spacer(1, 20))

            

            descripcion_texto = '<b>Significado de los niveles de desempeño – Matemáticas, quinto grado</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style)) 

            # Tabla descriptiva de niveles de desempeño
            niveles_data = [
                [
                    Paragraph("Nivel", parrafo_estilo3),
                    Paragraph("Descripción", parrafo_estilo3)
                ],
                [
                    Paragraph("<b>Bajo<br/>(entre 1 y 5 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Los estudiantes ubicados en este nivel de desempeño:</b><br/><br/>
                            • Describen relaciones entre cantidades.<br/>
                            • Aplican fórmulas estándar para cálculos geométricos (perímetro, área,
                            volumen).<br/>
                            • Resuelven problemas aditivos y multiplicativos rutinarios.<br/>
                            • Manejan fracciones, decimales y probabilidad simple (frecuencias o
                            razones).<br/>
                            • Reconocen semejanza o congruencia en figuras mediante ejemplos
                            concretos.<br/>
                            • Interpretan representaciones pictóricas y numéricas, pero su razonamiento
                            es guiado, con limitaciones en la argumentación y conexión de conceptos.
                            """, parrafo_estilo2)
                ],
                [
                    Paragraph("<b>Medio<br/>(entre 6 y 10 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Además de lo descrito en el nivel anterior, los estudiantes ubicados en
                            este nivel:</b><br/><br/>
                            • Resuelven problemas multiplicativos simples, no rutinarios (división,
                            proporcionalidad).<br/>
                            • Generan equivalencias entre expresiones numéricas.<br/>
                            • Establecen conjeturas sobre probabilidad.<br/>
                            • Utilizan medidas no estandarizadas para realizar cálculos geométricos.
                            • Ordenan objetos por volumen.<br/>
                            • Integran datos de múltiples gráficos estadísticos.<br/>
                            • Argumentan soluciones basadas en análisis de datos<br/>
                            • Representan relaciones entre magnitudes mediante expresiones
                            matemáticas o pictogramas, mostrando mayor capacidad para vincular
                            conceptos.
                            """, parrafo_estilo2)
                ],
                [
                    Paragraph("<b>Alto<br/>(entre 11 y 20 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Además de lo descrito en el nivel anterior, los estudiantes ubicados en
                            este nivel:</b><br/><br/>
                            • Resuelven problemas multiplicativos compuestos y no rutinarios (división,
                            agrupación, proporcionalidad).<br/>
                            • Generan equivalencias entre expresiones numéricas con precisión.<br/>
                            • Argumentan con rigor la mejor solución para situaciones problema,
                            vinculando datos de múltiples gráficos estadísticos.<br/>
                            • Determinan perímetros de polígonos irregulares con medidas no
                            estandarizadas.<br/>
                            • Ordenan objetos por volumen.<br/>
                            • Representan relaciones entre magnitudes mediante expresiones
                            matemáticas o pictogramas, demostrando pensamiento crítico y síntesis de
                            información.<br/>
                            • Establecen conjeturas fundamentadas sobre probabilidad.<br/>
                            • Aplican razonamiento proporcional en contextos diversos.
                            """, parrafo_estilo2)
                ],
            ]

            tabla_niveles = Table(niveles_data, colWidths=[80, 400])
            tabla_niveles.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10.5),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('LINEBELOW', (0, 0), (-1, -2), 0.25, colors.grey),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey)
            ]))

            elements.append(Spacer(1, 12))
            elements.append(tabla_niveles)

            parrafo_intro = Paragraph(
                "<b>Nota:</b> el Anexo 4 contiene las descripciones más detalladas de estos niveles de desempeño; por tanto, se recomienda su consulta y análisis.",
                parrafo_estilo
            )

            elements.append(Spacer(1, 12))
            elements.append(parrafo_intro) 
            
            #--------------------------------Anexos----------------------------------------
            elements.append(PageBreak())
            parrafo_titulo = Paragraph(
                "<b><font color='#1B8830'>Anexos</font></b>",
                titulo_style
            )
            parrafo_intro = Paragraph(
                "Tablas con las descripciones completas de los niveles de desempeño en cada área y grado.",
                parrafo_estilo
            )

            parrafo_anexo = Paragraph(
                "<font color='#1B8830'>Anexo 1. Descripción detallada de los niveles de desempeño en la prueba de Lenguaje, tercer grado</font>",
                parrafo_estilo2
            )

            elements.append(Spacer(1, 5))
            elements.append(parrafo_titulo)
            elements.append(Spacer(1, 5))
            elements.append(parrafo_intro)
            elements.append(Spacer(1, 5))
            elements.append(parrafo_anexo)

            # Tabla descriptiva de niveles de desempeño
            niveles_data = [
                [
                    Paragraph("Nivel", parrafo_estilo4),
                    Paragraph("Descripción", parrafo_estilo4)
                ],
                [
                    Paragraph("<b>Bajo<br/>(entre 1 y 4 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Los estudiantes ubicados en este nivel de desempeño:</b><br/><br/>
                            • Reconocen el uso de sinónimos y antónimos.<br/>
                            • Comparan textos de diferente formato y finalidad para dar cuenta de sus relaciones de contenido.
                            """, parrafo_estilo2)
                ],
                [
                    Paragraph("<b>Medio<br/>(entre 5 y 12 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Además de lo descrito en el nivel anterior, los estudiantes ubicados en
                            este nivel:</b><br/><br/>
                            • Reconocen el significado de una palabra en un enunciado dentro del texto.<br/>
                            • Identifican el significado del vocabulario dentro de una situación comunicativa.<br/>
                            • Identifican la voz que narra una historia.<br/>
                            • Identifican los diferentes personajes que se encuentran mencionados en el texto.<br/>
                            • Reconocen la secuencia y orden lógico de las acciones.<br/>
                            • Identifican cómo son los lugares en donde se desarrollan los hechos.<br/>
                            • Identifican la relación entre el título y el contenido de textos explicativos y argumentativos.<br/>
                            • Deducen el tema tratado a partir de la información implícita en una parte determinada de un texto narrativo.<br/>
                            • Parafrasean oraciones o proposiciones de textos explicativos y dialogales.<br/>
                            • Identifican las causas, consecuencias, problemas, soluciones, fases o características, en un texto argumentativo.<br/>
                            • Reconocen la diferencia entre una descripción literaria y una descripción técnica para reconocer el punto de vista de quien escribe, en un texto descriptivo.

                            """, parrafo_estilo2)
                ],
                [
                    Paragraph("<b>Alto<br/>(entre 13 y 20 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Además de lo descrito en el nivel anterior, los estudiantes ubicados en
                            este nivel:</b><br/><br/>
                            • Identifican la secuencia discursiva (tipo de texto) predominante en un texto a partir de su estructura.<br/>
                            • Identifican la relación entre el título y el contenido de un texto descriptivo, narrativo y dialogal.<br/>
                            • Identifican sobre quién se enfatiza la acción en determinadas partes de un texto narrativo.<br/> 
                            • Deducen el tema tratado a partir de la información implícita en una parte determinada de textos descriptivos y dialogales.<br/>
                            • Reconocen acciones (no lingüísticas) realizadas por personajes de una narración y les atribuye sentido.<br/>
                            • Parafrasean oraciones o proposiciones de un texto narrativo.<br/>
                            • Identifican el contexto en que se crea una obra literaria y lo relacionan con los conocimientos que tienen sobre la obra.<br/>
                            • Relacionan textos y movilizan saberes previos para ampliar referentes o contenidos ideológicos.<br/>
                            • Discriminan el tema e idea principal de un texto y lo relacionan con otro texto.<br/>
                            • Elaboran hipótesis de lectura para reconocer el sentido global de un texto.<br/>
                            • Identifican en el texto ideas que puedan considerarse un ejemplo de algo que ya se sabe.<br/>
                            • Relacionan textos que están compuestos por imágenes e interpretan su significado.<br/>
                            • Identifican el propósito general de un texto argumentativo a partir del reconocimiento de su estructura.

                            """, parrafo_estilo2)
                ],
            ]

            tabla_niveles = Table(niveles_data, colWidths=[80, 400])
            tabla_niveles.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10.5),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('LINEBELOW', (0, 0), (-1, -2), 0.25, colors.grey),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#33A652')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))

            elements.append(Spacer(1, 12))
            elements.append(tabla_niveles)


            parrafo_anexo = Paragraph(
                "<font color='#1B8830'>Anexo 2. Descripción detallada de los niveles de desempeño en la prueba de Lenguaje, quinto grado</font>",
                parrafo_estilo2
            )
            elements.append(PageBreak())
            elements.append(Spacer(1, 10))
            elements.append(parrafo_anexo)

            # Tabla descriptiva de niveles de desempeño
            niveles_data = [
                [
                    Paragraph("Nivel", parrafo_estilo4),
                    Paragraph("Descripción", parrafo_estilo4)
                ],
                [
                    Paragraph("<b>Bajo<br/>(entre 1 y 6 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Los estudiantes ubicados en este nivel de desempeño:</b><br/><br/>
                            •	Reconocen el uso de sinónimos y antónimos para enriquecer su vocabulario.<br/>
                            •	Identifican la relación entre el título y el contenido de un texto narrativo.<br/>
                            •	Relacionan textos que están compuestos por imágenes e interpretan su significado.<br/>

                            """, parrafo_estilo2)
                ],
                [
                    Paragraph("<b>Medio<br/>(entre 5 y 12 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Además de lo descrito en el nivel anterior, los estudiantes ubicados en
                            este nivel:</b><br/><br/>
                            •	Identifican los diferentes personajes que se encuentran mencionados en el texto.<br/>
                            •	Reconocen la secuencia y orden lógico de las acciones.<br/>
                            •	Identifican la secuencia discursiva (tipo de texto) predominante en un texto a partir de su estructura.<br/>
                            •	Identifican la relación entre el título y el contenido de textos explicativos, dialogales y argumentativos.<br/>
                            •	Identifican sobre quién se enfatiza la acción en determinadas partes de un texto narrativo. <br/>
                            •	Deducen el tema tratado a partir de la información implícita en una parte determinada de un texto descriptivo. <br/>
                            •	Parafrasean oraciones o proposiciones de textos explicativos y narrativos.<br/>
                            •	Relacionan textos y movilizan saberes previos para ampliar referentes o contenidos ideológicos.<br/>
                            •	Discriminan el tema e idea principal de un texto y lo relacionan con otro texto.<br/>
                            •	Elaboran hipótesis de lectura para reconocer el sentido global de un texto.<br/>
                            •	Comparan textos de diferente formato y finalidad para dar cuenta de sus relaciones de contenido.<br/>
                            •	Identifican las causas, consecuencias, problemas, soluciones, fases o características, en un texto argumentativo.<br/>
                            •	Reconocen la diferencia entre una descripción literaria y una descripción técnica para reconocer el punto de vista de quien escribe, en un texto descriptivo.

                            """, parrafo_estilo2)
                ],
                [
                    Paragraph("<b>Alto<br/>(entre 13 y 20 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Además de lo descrito en el nivel anterior, los estudiantes ubicados en
                            este nivel:</b><br/><br/>
                            •	Reconocen el significado de una palabra en un enunciado dentro del texto.<br/>
                            •	Identifican el significado del vocabulario dentro de una situación comunicativa.<br/>
                            •	Identifican la voz que narra una historia.<br/>
                            •	Identifican la relación entre el título y el contenido de un texto descriptivo.<br/>
                            •	Deducen el tema tratado a partir de la información implícita en una parte determinada de textos narrativos y dialogales.<br/>
                            •	Reconocen acciones (no lingüísticas) realizadas por personajes de una narración y les atribuye sentido.<br/>
                            •	Parafrasean oraciones o proposiciones de un texto dialogal.<br/>
                            •	Identifican el contexto en que se crea una obra literaria y lo relaciona con los conocimientos que tienen sobre la obra.
                            """, parrafo_estilo2)
                ],
            ]

            tabla_niveles = Table(niveles_data, colWidths=[80, 400])
            tabla_niveles.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10.5),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('LINEBELOW', (0, 0), (-1, -2), 0.25, colors.grey),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#33A652')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))

            elements.append(Spacer(1, 12))
            elements.append(tabla_niveles)


            parrafo_anexo = Paragraph(
                "<font color='#1B8830'>Anexo 3. Descripción detallada de los niveles de desempeño en la prueba de Matemáticas, tercer grado</font>",
                parrafo_estilo2
            )
            elements.append(PageBreak())
            elements.append(Spacer(1, 10))
            elements.append(parrafo_anexo)

            # Tabla descriptiva de niveles de desempeño
            niveles_data = [
                [
                    Paragraph("Nivel", parrafo_estilo4),
                    Paragraph("Descripción", parrafo_estilo4)
                ],
                [
                    Paragraph("<b>Bajo<br/>(entre 1 y 6 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Los estudiantes ubicados en este nivel de desempeño:</b><br/><br/>
                            •	Establecen el orden entre fracciones simples (1/2, 1/3, 1/4 …).<br/>
                            •	Reconocen el orden de las cantidades en una secuencia numérica.<br/>
                            •	Determinan la medida de una distancia utilizando una unidad de medida estandarizada.

                            """, parrafo_estilo2)
                ],
                [
                    Paragraph("<b>Medio<br/>(entre 7 y 13 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Además de lo descrito en el nivel anterior, los estudiantes ubicados en
                            este nivel:</b><br/><br/>
                            •	Utilizan las fracciones simples (1/2, 1/3, 1/4) para representar situaciones en contexto de medida.<br/>
                            •	Seleccionan la unidad de medida más pertinente en determinado contexto.<br/>
                            •	Reconocen el movimiento realizado a una figura para obtener otra.<br/>
                            •	Resuelven problemas multiplicativos en situaciones cotidianas en las que hay que hallar el cambio que produjo el resultado.<br/>
                            •	Determinan el área de un polígono regular dado el patrón de recubrimiento.<br/>
                            •	Expresan como un modelo multiplicativo un modelo aditivo dado. <br/>
                            •	Representan en una tabla una secuencia numérica dada. <br/>
                            •	Identifican el patrón de cambio y generan valores adicionales de la secuencia.<br/>
                            •	Determinan la posibilidad de ocurrencia de un evento aleatorio simple.<br/>
                            •	Resuelven problemas que implican comparar la posibilidad de ocurrencia de dos eventos aleatorios simples.
                            """, parrafo_estilo2)
                ],
                [
                    Paragraph("<b>Alto<br/>(entre 14 y 20 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Además de lo descrito en el nivel anterior, los estudiantes ubicados en
                            este nivel:</b><br/><br/>
                            •	Identifican el término siguiente en una secuencia numérica aditiva.<br/>
                            •	Identifican los aspectos comunes que son medibles de un conjunto de objetos.<br/>
                            •	Resuelven problemas de estructura aditiva de composición y de transformación.<br/>
                            •	Reconocen los datos y frecuencias de datos que cumplen condiciones específicas según el contexto.<br/>
                            •	Toman decisiones haciendo uso de la moda de un conjunto de datos en un contexto escolar.
                            """, parrafo_estilo2)
                ],
            ]

            tabla_niveles = Table(niveles_data, colWidths=[80, 400])
            tabla_niveles.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10.5),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('LINEBELOW', (0, 0), (-1, -2), 0.25, colors.grey),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#33A652')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))

            elements.append(Spacer(1, 12))
            elements.append(tabla_niveles)


            parrafo_anexo = Paragraph(
                "<font color='#1B8830'>Anexo 4. Descripción detallada de los niveles de desempeño en la prueba de Matemáticas, quinto grado</font>",
                parrafo_estilo2
            )
            elements.append(PageBreak())
            elements.append(Spacer(1, 10))
            elements.append(parrafo_anexo)

            # Tabla descriptiva de niveles de desempeño
            niveles_data = [
                [
                    Paragraph("Nivel", parrafo_estilo4),
                    Paragraph("Descripción", parrafo_estilo4)
                ],
                [
                    Paragraph("<b>Bajo<br/>(entre 1 y 5 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Los estudiantes ubicados en este nivel de desempeño:</b><br/><br/>
                            •	Describen propiedades y relaciones entre cantidades y magnitudes y sus operaciones.<br/>
                            •	Expresan el grado de probabilidad de un evento, usando frecuencias o razones.<br/>
                            •	Utilizan estrategias estandarizadas (fórmulas) para encontrar perímetro, área o superficie, o volumen o capacidad de diferentes objetos, en contextos escolares y extraescolares.<br/>
                            •	Establecen equivalencias a partir de las relaciones, propiedades o dependencia entre magnitudes y expresiones numéricas.<br/>
                            •	Determinan figuras semejantes o las condiciones para que se dé la semejanza.

                            """, parrafo_estilo2)
                ],
                [
                    Paragraph("<b>Medio<br/>(entre 6 y 10 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Además de lo descrito en el nivel anterior, los estudiantes ubicados en
                            este nivel:</b><br/><br/>
                            •	Determinan la representación numérica correspondiente a una representación pictórica.<br/>
                            •	Determinan la correspondencia entre un número fraccionario y un número decimal.<br/>
                            •	Expresan la probabilidad de un evento haciendo uso de las fracciones o un número decimal.<br/>
                            •	Resuelven problemas aditivos rutinarios de composición o transformación.<br/>
                            •	Resuelven problemas multiplicativos rutinarios de razón.<br/>
                            •	Determinan el área de un polígono no regular dado el patrón de recubrimiento.<br/>
                            •	Determinan el volumen de un sólido dadas las caras del objeto que lo constituyen.<br/>
                            •	Identifican el patrón de cambio dada una secuencia numérica, representada en una tabla, y generan valores adicionales de la secuencia.<br/>
                            •	Explican las condiciones necesarias para que dos o más figuras sean congruentes, usando ejemplos y argumentos geométricos simples.<br/>
                            •	Determinan si dos o más figuras son semejantes, utilizando ejemplos y conceptos básicos de proporcionalidad y geometría.

                            """, parrafo_estilo2)
                ],
                [
                    Paragraph("<b>Alto<br/>(entre 11 y 20 puntos)</b>", parrafo_estilo2),
                    Paragraph("""
                            <b>Además de lo descrito en el nivel anterior, los estudiantes ubicados en
                            este nivel:</b><br/><br/>
                            •	Generan equivalencias entre expresiones numéricas.<br/>
                            •	Establecen conjeturas acerca de la posibilidad de ocurrencia de eventos.<br/>
                            •	Resuelven problemas multiplicativos rutinarios de división o agrupación.<br/>
                            •	Resuelven problemas multiplicativos rutinarios de proporcionalidad.<br/>
                            •	Determinan el perímetro de polígonos no regulares utilizando unidades de medidas no estandarizadas.<br/>
                            •	Ordenan objetos de acuerdo con su volumen.<br/>
                            •	Representan la relación entre magnitudes utilizando expresiones matemáticas o pictogramas.<br/>
                            •	Identifican el conjunto de datos de una tabla de acuerdo con los datos de dos o más gráficos estadísticos.<br/>
                            •	Determinan la mejor opción para una situación problema argumentando la representación de uno o más conjuntos de datos.

                            """, parrafo_estilo2)
                ],
            ]

            tabla_niveles = Table(niveles_data, colWidths=[80, 400])
            tabla_niveles.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10.5),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('LINEBELOW', (0, 0), (-1, -2), 0.25, colors.grey),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#33A652')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))

            elements.append(Spacer(1, 12))
            elements.append(tabla_niveles)

            #-----------------------------------------------------------------------------------------------------------------------

            # Crear documento base
            doc.build(elements, onFirstPage=self.portada_con_logo, onLaterPages=self.agregar_numero_pagina)

            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            
            response['Content-Disposition'] = f'attachment; filename=\"Reporte.pdf\"'

            return response

        except Exception as e:
            print("ERROR:", format_exc())
            return Response({
                "error": "Error interno al generar el PDF.",
                "detalle": str(e)
            }, status=500)

    def portada_con_logo(self, canvas_obj, doc):
        width, height = letter
        canvas_obj.saveState()

        logo_superior = os.path.join(BASE_DIR, "LogoFundacionTerpel.jpg")
        canvas_obj.drawImage(logo_superior, x=40, y=height - 80, width=120, height=60, preserveAspectRatio=True, mask='auto')

        logo_inferior = os.path.join(BASE_DIR, "LogoVisionSocial.png")
        canvas_obj.drawImage(logo_inferior, x=40, y=40, width=120, height=60, preserveAspectRatio=True, mask='auto')

        canvas_obj.setFont("Helvetica", 10)
        canvas_obj.setFillColor(colors.black)
        canvas_obj.drawRightString(
            width - 40,
            60,
            "El programa Escuelas que Aprenden® es propiedad de la Fundación Terpel"
        )

        canvas_obj.restoreState()


    def tabla(self, modo, institucion, aplicacion, proyecto, grado, materia):
        
        if grado == 3:
            grado_str = 'Tercero'
        else:
            grado_str = 'Quinto'
        
        if materia == 'M':
            prueba = 'Matemáticas'
        else:
            prueba = 'Lenguaje'

        if modo == 0:   
            encuestas = Encuesta.objects.filter(
                aplicacion=aplicacion,
                nombre_institucion=institucion,
                nombre=proyecto,
                grado=grado_str,
                prueba=prueba
            )
        else:
            encuestas = Encuesta.objects.filter(
                aplicacion=aplicacion,
                nombre=proyecto,
                grado=grado_str,
                prueba=prueba
            )

        data = []
        maxi = 0
        mini = 20
        for encuesta in encuestas:
            if encuesta.correctos is None:
                continue
            if maxi < encuesta.correctos:
                maxi = encuesta.correctos
            if mini > encuesta.correctos:
                mini = encuesta.correctos
            data.append(encuesta.correctos)

        if not data:
            return [0, 0, 0, 0, 0]

        media = sum(data)/len(data)

        suma_cuadrados = sum((x - media) ** 2 for x in data)
        desviacion_estandar = math.sqrt(suma_cuadrados / (len(data) - 1))

        return [
            len(data),
            round(float(media), 1),
            round(float(desviacion_estandar), 1),
            mini,
            maxi
        ]
    
    def desempeño(self, modo, institucion, aplicacion, proyecto, grado, materia, a, b):
        bajo = 0
        medio = 0
        alto = 0
        if grado == 3:
            grado_str = 'Tercero'
        else:
            grado_str = 'Quinto'
        
        if materia == 'M':
            prueba = 'Matemáticas'
        else:
            prueba = 'Lenguaje'

        if modo == 0:   
            encuestas = Encuesta.objects.filter(
                aplicacion=aplicacion,
                nombre_institucion=institucion,
                nombre=proyecto,
                grado=grado_str,
                prueba=prueba
            )
        else:
            encuestas = Encuesta.objects.filter(
                aplicacion=aplicacion,
                nombre=proyecto,
                grado=grado_str,
                prueba=prueba
            )
        
        total = encuestas.count()
        if total == 0:
            return [0, 0, 0]  # Evita división por cero

        for encuesta in encuestas:
            if encuesta.correctos is None:
                continue
            if encuesta.correctos < a:
                bajo+=1
            elif encuesta.correctos < b:
                medio+=1
            else:
                alto+=1
        
        total = bajo + medio + alto

        if total == 0:
            total = 1

        return [int((bajo/total)*100), int((medio/total)*100), int((alto/total)*100)]

    def agregar_numero_pagina(self, canvas, doc):
        page_num = canvas.getPageNumber()
        text = f"{page_num}"
        canvas.setFont('Helvetica', 9)

        # Obtiene el ancho de la página para posicionar a la derecha
        width, height = letter

        # Ajusta la posición: derecha (margen derecho - ancho del texto)
        text_width = canvas.stringWidth(text, 'Helvetica', 12)
        x = width - inch * 0.5 # Una pulgada del borde derecho
        y = 0.5 * inch  # Desde el borde inferior

        canvas.drawString(x, y, text)
    
    def tabla_inicial(self, M3, E3, M5, E5):
        p = []

        p.append(round(float((E3/M3)*100), 1))
        p.append(round(float((E5/M5)*100), 1))
        p.append(round(float(((E3 + E5)/(M3 + M5))*100), 1))

        return p

    def comma_dot(self, x):
        res = str(x)
        res = res.replace('.',',')
        return res

class GenerarReporte2APIIew(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            institucion = request.GET.get('institucion')
            proyecto = request.GET.get('proyecto')
            tercero_entrada = int(request.GET.get('tercero_entrada'))
            quinto_entrada = int(request.GET.get('quinto_entrada'))
            tercero_salida = int(request.GET.get('tercero_salida'))
            quinto_salida = int(request.GET.get('quinto_salida'))
            res = request.GET.get('dane')

            if not institucion or not proyecto:
                return Response({
                    "error": "Faltan parámetros: institucion y proyecto son requeridos"
                }, status=400)

            encuestas = Encuesta.objects.filter(
                nombre_institucion=institucion,
                nombre=proyecto
            )

            if not encuestas.exists():
                return Response({
                    "error": "No se encontraron encuestas para los filtros proporcionados."
                }, status=404)

            ciudad = ''
            fecha_aplicacion = ''
            # Preparar los datos
            ter1 = []
            ter2 = []
            quin1 = []
            quin2 = []
            for encuesta in encuestas:
                grado = encuesta.grado or "N/A"
                if grado == 'Tercero' and encuesta.aplicacion == 'entrada':
                    ter1.append(grado)
                elif grado == 'Tercero' and encuesta.aplicacion == 'salida':
                    ter2.append(grado)
                elif grado == 'Quinto' and encuesta.aplicacion == 'entrada':
                    quin1.append(grado)
                else:
                    quin2.append(grado)
                ciudad = encuesta.ciudad
                fecha_aplicacion = encuesta.fecha

            buffer = BytesIO()

            # Crear el documento
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []

            # Estilo verde centrado
            titulo_style = ParagraphStyle(
                name="TituloVerdeCentrado",
                alignment=TA_CENTER,
                fontSize=18,
                textColor=HexColor("#1B8830"),
                leading=22,
                spaceAfter=12
            )

            subtitulo_style = ParagraphStyle(
                name="SubtituloVerdeCentrado",
                alignment=TA_CENTER,
                fontSize=14,
                textColor=HexColor("#1B8830"),
                leading=20,
                spaceAfter=6
            )

            descripcion_style = ParagraphStyle(
                name="DescripcionVerdeCentrada",
                alignment=TA_CENTER,
                fontSize=12,
                textColor=HexColor("#1B8830"),
                leading=16
            )

            parrafo_estilo = ParagraphStyle(
                name='IntroJustificado',
                fontName='Helvetica',
                fontSize=10.5,
                leading=14,
                textColor=colors.black,
                alignment=4,  # Justificado
                spaceAfter=20,
                leftIndent=10,
                rightIndent=10,
            )

            parrafo_estilo2 = ParagraphStyle(
                name='IntroIzquierda',
                fontName='Helvetica',
                fontSize=10.5,
                leading=14,
                textColor=colors.black,
                alignment=TA_LEFT,
                spaceAfter=20,
                leftIndent=10,
                rightIndent=10,
            )

            parrafo_estilo3 = ParagraphStyle(
                name='IntroCentradoVerde',
                fontName='Helvetica',
                fontSize=10.5,
                leading=14,
                textColor=HexColor("#33A652"),  # Color verde personalizado
                alignment=TA_CENTER,            # Texto centrado
                spaceAfter=20,
                leftIndent=10,
                rightIndent=10,
            )

            parrafo_estilo4 = ParagraphStyle(
                name='IntroCentradoVerde',
                fontName='Helvetica',
                fontSize=10.5,
                leading=14,
                textColor=HexColor("#ffffff"),  # Color verde personalizado
                alignment=TA_CENTER,            # Texto centrado
                spaceAfter=20,
                leftIndent=10,
                rightIndent=10,
            )

            descripcion_izq_style = ParagraphStyle(
                name="DescripcionIzquierda",
                alignment=TA_LEFT,
                fontSize=12,
                textColor=HexColor("#1B8830"),
                leading=16,
                spaceBefore=12,
                spaceAfter=8,
            )

            recuadro_style = ParagraphStyle(
                name="RecuadroJustificado",
                fontSize=10.5,
                leading=14,
                alignment=4,  # Justificado
                textColor=colors.black,
            )

            # Contenido
            titulo_texto = f"""
            <b>Reporte de resultados para la</b><br/>
            <b>{institucion} - Comparativo de las aplicaciones de entrada y de salida</b>
            """

            subtitulo_texto = "<b>Programa Escuelas que Aprenden®</b>"
            descripcion_texto = f"<b>Reporte de resultados de la institución educativa {institucion} en las pruebas de Lenguaje y Matemáticas – comparación de resultados entrada y de salida</b>"
            
            # Insertar en elementos
            elements.append(Spacer(1, 200))  # Centrar verticalmente
            elements.append(Paragraph(titulo_texto, titulo_style))
            elements.append(Spacer(1, 12))
            elements.append(PageBreak())  #Inicia nueva página para la tabla
            elements.append(Paragraph(subtitulo_texto, subtitulo_style))
            elements.append(Paragraph(descripcion_texto, descripcion_style))
            
            parrafo_intro = Paragraph(
                f"""Este informe presenta los resultados obtenidos por los estudiantes de la institución
                {institucion}, correspondientes a la aplicación de entrada y salida del programa educativo. 
                Los datos aquí consignados reflejan el desempeño en las áreas de Lenguaje y Matemáticas, 
                y constituyen un insumo valioso para orientar estrategias pedagógicas y fortalecer 
                los procesos de enseñanza y aprendizaje.""",
                parrafo_estilo
            )

            elements.append(Spacer(1, 12))
            elements.append(parrafo_intro)    

            descripcion_texto = '<b>1. Datos de identificación de la institución educativa</b>'

            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))

            # Cambio de formato fecha 
            nFecha = fecha_aplicacion.strftime("%d-%m-%Y")

            # Datos de la tabla
            resumen_data = [
                ['Ciudad:', ciudad],
                ['Institución educativa:', institucion],
                ['Código DANE:', res],
                ['Fecha de aplicación:', nFecha],
            ]

            # Crear tabla de resumen
            tabla_resumen = Table(resumen_data, colWidths=[200, 300])
            tabla_resumen.setStyle(TableStyle([
                ('TEXTCOLOR', (0, 0), (0, -1), HexColor("#1B8830")),  # columna izquierda verde
                ('TEXTCOLOR', (1, 0), (1, -1), colors.black),         # columna derecha negra
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                # Optional borders:
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey)
            ]))

            # Añadir a los elementos después del texto introductorio
            elements.append(tabla_resumen)
            elements.append(Spacer(1, 20))

            descripcion_texto = '<b>2. Ficha técnica: número de estudiantes matriculados y evaluados</b>'

            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))

            c = self.tabla_inicial(tercero_entrada, len(ter1), tercero_salida, len(ter2), quinto_entrada, len(quin1), quinto_salida, len(quin2))

            tabla_datos = [
                ["Grado", "Entrada", "", "", "Salida", "", ""],  # Encabezados
                ["", "Total\nmatriculados", "Total\nevaluados", "%", "Total\nmatriculados", "Total\nevaluados", "%"], # Encabezados 2
                ["Tercero", tercero_entrada, len(ter1), f"{self.comma_dot(c[0])}%", tercero_salida, len(ter2), f"{self.comma_dot(c[3])}%"],  # Fila 1
                ["Quinto ", quinto_entrada, len(quin1), f"{self.comma_dot(c[1])}%", quinto_salida, len(quin2), f"{self.comma_dot(c[4])}%"],  # Fila 2
                ["Total", tercero_entrada+quinto_entrada , len(ter1)+len(quin1), f"{self.comma_dot(c[2])}%", tercero_salida+quinto_salida, len(ter2)+len(quin2), f"{self.comma_dot(c[5])}%"],  # Fila 3
            ]

            # Crear la tabla
            tabla_estadistica = Table(tabla_datos, colWidths=[100, 70, 70, 60, 70, 70, 60])
            tabla_estadistica.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 1), HexColor("#1B8830")),
                ('TEXTCOLOR', (0, 0), (-1, 1), colors.white),

                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),

                ('SPAN', (0, 0), (0, 1)),  # Unir "Grado" de encabezado principal y subencabezado
                ('SPAN', (1, 0), (3, 0)),  # Unir "Entrada" (total matriculados, evaluados, %)
                ('SPAN', (4, 0), (6, 0)),  # Unir "Salida" (total matriculados, evaluados, %)
                ('VALIGN', (0, 0), (-1, 1), 'MIDDLE'),  # Centrar verticalmente los encabezados (primera y segunda fila)
            ]))

            elements.append(Spacer(1, 12))
            elements.append(tabla_estadistica)
            elements.append(Spacer(1, 20))
            elements.append(PageBreak())  #Inicia nueva página para la tabla

            #----------------------------------------------------------------------------------------------------------------------------

            descripcion_texto = '<b>3. Resultados en la prueba de Lenguaje</b>'

            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))

            contenido = """
            <b><font color='#1B8830'>Qué se evalúa:</font></b><br/><br/>
            Las pruebas de Lenguaje evalúan las habilidades de los estudiantes de tercero y quinto grados para interpretar y comprender diversos tipos y formatos de textos orientados a diferentes propósitos.<br/><br/>
            Los tipos de textos evaluados son los siguientes: narrativos, descriptivos, dialogales, explicativos y argumentativos.<br/><br/>
            Los formatos de textos evaluados son los siguientes: continuos (organizados en forma de párrafos) y discontinuos (organizados de manera gráfica y no lineal).<br/><br/>
            Las pruebas abordan tres niveles de comprensión textual:.<br/><br/>
            • <b>Literal:</b> implica reconocer el significado explícito dentro de un texto.<br/>
            • <b>Inferencial:</b> implica reconocer el significado implícito de los contenidos en un texto.<br/>
            • <b>Crítica:</b> implica evaluar los contenidos y las formas de los textos, así como hacer una valoración de argumentos.<br/><br/>
            Los puntajes en esta prueba se presentan en una escala de 0 a 20 puntos. 
            """

            contenido_parrafo = Paragraph(contenido, recuadro_style)

            recuadro_tabla = Table([[contenido_parrafo]], colWidths=[460])

            # Estilos de la tabla
            recuadro_tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#A4D7B2")),
                ('BOX', (0, 0), (0, 0), 0.5, colors.HexColor("#1B8830")),  # Borde más delgado y color personalizado
                ('LEFTPADDING', (0, 0), (0, 0), 10),
                ('RIGHTPADDING', (0, 0), (0, 0), 10),
                ('TOPPADDING', (0, 0), (0, 0), 6),
                ('BOTTOMPADDING', (0, 0), (0, 0), 6),
            ]))

            # Añádelo a la lista de elementos
            elements.append(Spacer(1, 12))
            elements.append(recuadro_tabla)
            elements.append(Spacer(1, 20))

            #-----------------------------------------------------------------------------------------------------------------------

            descripcion_texto = '<b>3.1.	Tercer grado </b><br/><b>a. Puntaje</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))

            parrafo_intro = Paragraph(
                "Espacio estático para incluir un texto, pendiente de construir, para explicar que el puntaje se presenta en una escala de 0 a 20 puntos, qué es el promedio y la desviación estándar (dos párrafos cortos como máximo).",
                parrafo_estilo
            )

            elements.append(Spacer(1, 12))
            elements.append(parrafo_intro) 
              
            t = self.tabla(0, institucion, 'entrada',proyecto, 3, 'L')
            c = self.tabla(1, ciudad, 'entrada',proyecto, 3, 'L')
            t2 = self.tabla(0, institucion, 'salida',proyecto, 3, 'L')
            c2 = self.tabla(1, ciudad, 'salida',proyecto, 3, 'L')
            
            tabla_datos = [
                ["", "Aplicación", "# evaluados", "Media", "Desv. est.", "Mínimo", "Máximo"],  # Encabezados
                ["Institución", "Entrada",t[0], self.comma_dot(t[1]), self.comma_dot(t[2]), t[3], t[4]],  # Fila 1
                ['', "Salida",t2[0], self.comma_dot(t2[1]), self.comma_dot(t2[2]), t2[3], t2[4]],  # Fila 2
                ["Municipio", "Entrada",c[0], self.comma_dot(c[1]), self.comma_dot(c[2]), c[3], c[4]],  # Fila 3
                ['', "Salida",c2[0], self.comma_dot(c2[1]), self.comma_dot(c2[2]), c2[3], c2[4]],  # Fila 4
            ]

            # Crear la tabla
            tabla_estadistica = Table(tabla_datos, colWidths=[130, 80, 80, 60, 80, 60, 60])
            tabla_estadistica.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor("#1B8830")),  # Fondo verde para encabezados
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),          # Texto blanco en encabezados
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),          # Líneas de tabla
                # Unir columna 0 de fila 1 y 2 (índices 1 y 2)
                ('SPAN', (0, 1), (0, 2)),

                # Unir columna 0 de fila 3 y 4 (índices 3 y 4)
                ('SPAN', (0, 3), (0, 4)),

                # Alineación vertical centrada en las celdas unidas
                ('VALIGN', (0, 1), (0, 2), 'MIDDLE'),
                ('VALIGN', (0, 3), (0, 4), 'MIDDLE'),
            ]))

            elements.append(Spacer(1, 12))
            elements.append(tabla_estadistica)
            elements.append(Spacer(1, 20))
            
            descripcion_texto = '<b>b. Descripción</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))

            parrafo_intro = Paragraph(
                "Espacio estático para incluir un texto, pendiente de construir, para explicar qué es y cómo interpretar los niveles de desempeño (dos párrafos cortos como máximo).",
                parrafo_estilo
            )

            elements.append(Spacer(1, 12))
            elements.append(parrafo_intro)   

            # Datos del gráfico
            niveles = ['Bajo', 'Medio', 'Alto']
            t = self.desempeño(0, institucion, "entrada", proyecto, 3, 'L', 5, 13)
            t2 = self.desempeño(0, institucion, "salida", proyecto, 3, 'L', 5, 13)
            c = self.desempeño(1, ciudad, "entrada", proyecto, 3, 'L', 5, 13)
            c2 = self.desempeño(1, ciudad, "salida", proyecto, 3, 'L', 5, 13)

            # ================== GRÁFICO ENTRADA ==================
            x = range(len(niveles))
            bar_width = 0.35

            plt.figure(figsize=(5, 4))
            bars1 = plt.bar([i - bar_width/2 for i in x],  t, width=bar_width, label='Entrada', color='#1B8830')
            bars2 = plt.bar([i + bar_width/2 for i in x], t2, width=bar_width, label='Salida', color='#6FBF73')

            for i, bar in enumerate(bars1):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{t[i]}%', ha='center', va='bottom', fontsize=10)

            for i, bar in enumerate(bars2):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{t2[i]}%', ha='center', va='bottom', fontsize=10)

            plt.xticks(x, niveles)
            plt.title('Distribución por Niveles de Desempeño - Institución\n')
            plt.legend()
            plt.tight_layout()

            # QUITAR eje Y
            plt.gca().axes.get_yaxis().set_visible(False)

            # QUITAR TODOS LOS BORDES, excepto abajo
            for spine in ['top', 'right', 'left']:
                plt.gca().spines[spine].set_visible(False)

            img_buffer1 = BytesIO()
            plt.savefig(img_buffer1, format='png')
            plt.close()
            img_buffer1.seek(0)
            grafico_entrada = RLImage(img_buffer1, width=260, height=200)

            # ================== GRÁFICO SALIDA ==================
            plt.figure(figsize=(5, 4))
            bars1 = plt.bar([i - bar_width/2 for i in x],  c, width=bar_width, label='Entrada', color='#1B8830')
            bars2 = plt.bar([i + bar_width/2 for i in x], c2, width=bar_width, label='Salida', color='#6FBF73')

            for i, bar in enumerate(bars1):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{c[i]}%', ha='center', va='bottom', fontsize=10)

            for i, bar in enumerate(bars2):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{c2[i]}%', ha='center', va='bottom', fontsize=10)

            plt.xticks(x, niveles)
            plt.title('Distribución por Niveles de Desempeño - Ciudad\n')
            plt.legend()
            plt.tight_layout()

            # QUITAR eje Y
            plt.gca().axes.get_yaxis().set_visible(False)

            # QUITAR TODOS LOS BORDES, excepto abajo
            for spine in ['top', 'right', 'left']:
                plt.gca().spines[spine].set_visible(False)

            img_buffer2 = BytesIO()
            plt.savefig(img_buffer2, format='png')
            plt.close()
            img_buffer2.seek(0)
            grafico_salida = RLImage(img_buffer2, width=260, height=200)

            # ================== AGREGAR AMBOS AL PDF ==================
            tabla_graficos = Table([[grafico_entrada, grafico_salida]], colWidths=[270, 270])
            elements.append(Spacer(1, 12))
            elements.append(tabla_graficos)
            elements.append(Spacer(1, 20))



            descripcion_texto = '<b>Significado de los niveles de desempeño – Lenguaje, tercer grado</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style)) 

            # Tabla descriptiva de niveles de desempeño
            niveles_data = [
                [
                    Paragraph("<b>Bajo<br/>(entre 1 y 4 puntos)</b>", parrafo_estilo),
                    Paragraph("El estudiante ubicado en este nivel de desempeño: <br/>"
                            "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", parrafo_estilo)
                ],
                [
                    Paragraph("<b>Medio<br/>(entre 5 y 12 puntos)</b>", parrafo_estilo),
                    Paragraph("Además de lo descrito en el nivel anterior, el estudiante ubicado en este nivel: <br/>"
                            "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", parrafo_estilo)
                ],
                [
                    Paragraph("<b>Alto<br/>(entre 13 y 20 puntos)</b>", parrafo_estilo),
                    Paragraph("Además de lo descrito en los niveles anteriores, el estudiante ubicado en este nivel: <br/>"
                            "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", parrafo_estilo)
                ],
            ]

            tabla_niveles = Table(niveles_data, colWidths=[180, 300])
            tabla_niveles.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10.5),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('LINEBELOW', (0, 0), (-1, -2), 0.25, colors.grey),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey)
            ]))

            elements.append(Spacer(1, 12))
            elements.append(tabla_niveles)

            #-----------------------------------------------------------------------------------------------------------------------

            descripcion_texto = '<b>3.2.	Quinto grado </b><br/><b>a. Puntaje</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))

            parrafo_intro = Paragraph(
                "Espacio estático para incluir un texto, pendiente de construir, para explicar que el puntaje se presenta en una escala de 0 a 20 puntos, qué es el promedio y la desviación estándar (dos párrafos cortos como máximo).",
                parrafo_estilo
            )

            elements.append(Spacer(1, 12))
            elements.append(parrafo_intro)   
            
            t = self.tabla(0, institucion, 'entrada',proyecto, 5, 'L')
            c = self.tabla(1, ciudad, 'entrada',proyecto, 5, 'L')
            t2 = self.tabla(0, institucion, 'salida',proyecto, 5, 'L')
            c2 = self.tabla(1, ciudad, 'salida',proyecto, 5, 'L')
            
            tabla_datos = [
                ["", "Aplicación", "# evaluados", "Media", "Desv. est.", "Mínimo", "Máximo"],  # Encabezados
                ["Institución", "Entrada",t[0], self.comma_dot(t[1]), self.comma_dot(t[2]), t[3], t[4]],  # Fila 1
                ['', "Salida",t2[0], self.comma_dot(t2[1]), self.comma_dot(t2[2]), t2[3], t2[4]],  # Fila 2
                ["Municipio", "Entrada",c[0], self.comma_dot(c[1]), self.comma_dot(c[2]), c[3], c[4]],  # Fila 3
                ['', "Salida",c2[0], self.comma_dot(c2[1]), self.comma_dot(c2[2]), c2[3], c2[4]],  # Fila 4
            ]

            # Crear la tabla
            tabla_estadistica = Table(tabla_datos, colWidths=[130, 80, 80, 60, 80, 60, 60])
            tabla_estadistica.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor("#1B8830")),  # Fondo verde para encabezados
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),          # Texto blanco en encabezados
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),          # Líneas de tabla
                # Unir columna 0 de fila 1 y 2 (índices 1 y 2)
                ('SPAN', (0, 1), (0, 2)),

                # Unir columna 0 de fila 3 y 4 (índices 3 y 4)
                ('SPAN', (0, 3), (0, 4)),

                # Alineación vertical centrada en las celdas unidas
                ('VALIGN', (0, 1), (0, 2), 'MIDDLE'),
                ('VALIGN', (0, 3), (0, 4), 'MIDDLE'),
            ]))

            elements.append(Spacer(1, 12))
            elements.append(tabla_estadistica)
            elements.append(Spacer(1, 20))

            descripcion_texto = '<b>b. Descripción</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))

            parrafo_intro = Paragraph(
                "Espacio estático para incluir un texto, pendiente de construir, para explicar qué es y cómo interpretar los niveles de desempeño (dos párrafos cortos como máximo).",
                parrafo_estilo
            )

            elements.append(Spacer(1, 12))
            elements.append(parrafo_intro)   

            # Datos del gráfico
            niveles = ['Bajo', 'Medio', 'Alto']
            t = self.desempeño(0, institucion, "entrada", proyecto, 5, 'L', 5, 13)
            t2 = self.desempeño(0, institucion, "salida", proyecto, 5, 'L', 5, 13)
            c = self.desempeño(1, institucion, "entrada", proyecto, 5, 'L', 5, 13)
            c2 = self.desempeño(1, institucion, "salida", proyecto, 5, 'L', 5, 13)

            # ================== GRÁFICO ENTRADA ==================
            x = range(len(niveles))
            bar_width = 0.35

            plt.figure(figsize=(5, 4))
            bars1 = plt.bar([i - bar_width/2 for i in x], t, width=bar_width, label='Entrada', color='#1B8830')
            bars2 = plt.bar([i + bar_width/2 for i in x], t2, width=bar_width, label='Salida', color='#6FBF73')

            for i, bar in enumerate(bars1):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{t[i]}%', ha='center', va='bottom', fontsize=10)

            for i, bar in enumerate(bars2):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{t2[i]}%', ha='center', va='bottom', fontsize=10)

            plt.xticks(x, niveles)
            plt.title('Distribución por Niveles de Desempeño - Institución\n')
            plt.legend()
            plt.tight_layout()

            # QUITAR eje Y
            plt.gca().axes.get_yaxis().set_visible(False)

            # QUITAR TODOS LOS BORDES, excepto abajo
            for spine in ['top', 'right', 'left']:
                plt.gca().spines[spine].set_visible(False)

            img_buffer1 = BytesIO()
            plt.savefig(img_buffer1, format='png')
            plt.close()
            img_buffer1.seek(0)
            grafico_entrada = RLImage(img_buffer1, width=260, height=200)

            # ================== GRÁFICO CIUDAD ==================
            plt.figure(figsize=(5, 4))
            bars1 = plt.bar([i - bar_width/2 for i in x], c, width=bar_width, label='Entrada', color='#1B8830')
            bars2 = plt.bar([i + bar_width/2 for i in x], c2, width=bar_width, label='Salida', color='#6FBF73')

            for i, bar in enumerate(bars1):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{c[i]}%', ha='center', va='bottom', fontsize=8)

            for i, bar in enumerate(bars2):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{c2[i]}%', ha='center', va='bottom', fontsize=8)

            plt.xticks(x, niveles)
            plt.title('Distribución por Niveles de Desempeño - Ciudad\n')
            plt.legend()
            plt.tight_layout()

            # QUITAR eje Y
            plt.gca().axes.get_yaxis().set_visible(False)

            # QUITAR TODOS LOS BORDES, excepto abajo
            for spine in ['top', 'right', 'left']:
                plt.gca().spines[spine].set_visible(False)

            img_buffer2 = BytesIO()
            plt.savefig(img_buffer2, format='png')
            plt.close()
            img_buffer2.seek(0)
            grafico_salida = RLImage(img_buffer2, width=260, height=200)

            # ================== AGREGAR AMBOS AL PDF ==================
            tabla_graficos = Table([[grafico_entrada, grafico_salida]], colWidths=[270, 270])
            elements.append(Spacer(1, 12))
            elements.append(tabla_graficos)
            elements.append(Spacer(1, 20))

            descripcion_texto = '<b>Significado de los niveles de desempeño – Lenguaje, quinto grado</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style)) 

            # Tabla descriptiva de niveles de desempeño
            niveles_data = [
                [
                    Paragraph("<b>Bajo<br/>(entre 1 y 6 puntos)</b>", parrafo_estilo),
                    Paragraph("El estudiante ubicado en este nivel de desempeño: <br/>"
                            "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", parrafo_estilo)
                ],
                [
                    Paragraph("<b>Medio<br/>(entre 7 y 13 puntos)</b>", parrafo_estilo),
                    Paragraph("Además de lo descrito en el nivel anterior, el estudiante ubicado en este nivel: <br/>"
                            "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", parrafo_estilo)
                ],
                [
                    Paragraph("<b>Alto<br/>(entre 14 y 20 puntos)</b>", parrafo_estilo),
                    Paragraph("Además de lo descrito en los niveles anteriores, el estudiante ubicado en este nivel: <br/>"
                            "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", parrafo_estilo)
                ],
            ]

            tabla_niveles = Table(niveles_data, colWidths=[180, 300])
            tabla_niveles.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10.5),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('LINEBELOW', (0, 0), (-1, -2), 0.25, colors.grey),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey)
            ]))

            elements.append(Spacer(1, 12))
            elements.append(tabla_niveles)

            #-----------------------------------------------------------------------------------------------------------------------
            
            descripcion_texto = '<b>4. Resultados en la prueba de Matemáticas</b>'

            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))

            contenido = """
            <b><font color='#1B8830'>Qué se evalúa:</font></b><br/><br/>
            Las pruebas de Matemáticas evalúan las habilidades de los estudiantes de tercero y quinto grados para plantear y resolver 
            diferentes tipos de problemas matemáticos teniendo en cuenta las siguientes competencias y componentes, establecidos en los 
            estándares básicos de competencias del Ministerio de Educación Nacional:.<br/><br/>
            <b><font color='#1B8830'>Competencias:</font></b><br/><br/>
            • <b><font color='#1B8830'>Comunicación, modelación y representación:</font></b>implica comprender cómo se presenta una información matemática y elaborar representaciones que permitan hacer comprensible dicha información a otros.<br/>
            • <b><font color='#1B8830'>Planteamiento y resolución de problemas:</font></b>implica comprender la utilidad del conocimiento disponible.<br/>
            • <b><font color='#1B8830'>Razonamiento y argumentación:</font></b>implica hacer una valoración sobre la adecuación de unos pasos realizados o para establecer la veracidad de lo que se afirma, entre otros.<br/><br/>
            <b><font color='#1B8830'>Componentes:</font></b><br/><br/>
            • Númerico - variacional<br/>
            • Espacial - métrico<br/>
            • Aleatorio<br/><br/>
            """

            contenido_parrafo = Paragraph(contenido, recuadro_style)
            recuadro_tabla = Table([[contenido_parrafo]], colWidths=[460])

            # Estilos de la tabla
            recuadro_tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#A4D7B2")),
                ('BOX', (0, 0), (0, 0), 0.5, colors.HexColor("#1B8830")),  # Borde más delgado y color personalizado
                ('LEFTPADDING', (0, 0), (0, 0), 10),
                ('RIGHTPADDING', (0, 0), (0, 0), 10),
                ('TOPPADDING', (0, 0), (0, 0), 6),
                ('BOTTOMPADDING', (0, 0), (0, 0), 6),
            ]))

            # Añádelo a la lista de elementos
            elements.append(Spacer(1, 12))
            elements.append(recuadro_tabla)
            elements.append(Spacer(1, 20))
            
            #-----------------------------------------------------------------------------------------------------------------------

            descripcion_texto = '<b>4.1.	Tercer grado </b><br/><b>a. Puntaje</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))

            parrafo_intro = Paragraph(
                "Espacio estático para incluir un texto, pendiente de construir, para explicar que el puntaje se presenta en una escala de 0 a 20 puntos, qué es el promedio y la desviación estándar (dos párrafos cortos como máximo).",
                parrafo_estilo
            )

            elements.append(Spacer(1, 12))
            elements.append(parrafo_intro)   
            
            t = self.tabla(0, institucion, 'entrada',proyecto, 3, 'M')
            c = self.tabla(1, ciudad, 'entrada',proyecto, 3, 'M')
            t2 = self.tabla(0, institucion, 'salida',proyecto, 3, 'M')
            c2 = self.tabla(1, ciudad, 'salida',proyecto, 3, 'M')
            
            tabla_datos = [
                ["", "Aplicación", "# evaluados", "Media", "Desv. est.", "Mínimo", "Máximo"],  # Encabezados
                ["Institución", "Entrada",t[0], self.comma_dot(t[1]), self.comma_dot(t[2]), t[3], t[4]],  # Fila 1
                ['', "Salida",t2[0], self.comma_dot(t2[1]), self.comma_dot(t2[2]), t2[3], t2[4]],  # Fila 2
                ["Municipio", "Entrada",c[0], self.comma_dot(c[1]), self.comma_dot(c[2]), c[3], c[4]],  # Fila 3
                ['', "Salida",c2[0], self.comma_dot(c2[1]), self.comma_dot(c2[2]), c2[3], c2[4]],  # Fila 4
            ]

            # Crear la tabla
            tabla_estadistica = Table(tabla_datos, colWidths=[130, 80, 80, 60, 80, 60, 60])
            tabla_estadistica.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor("#1B8830")),  # Fondo verde para encabezados
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),          # Texto blanco en encabezados
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),          # Líneas de tabla
                # Unir columna 0 de fila 1 y 2 (índices 1 y 2)
                ('SPAN', (0, 1), (0, 2)),

                # Unir columna 0 de fila 3 y 4 (índices 3 y 4)
                ('SPAN', (0, 3), (0, 4)),

                # Alineación vertical centrada en las celdas unidas
                ('VALIGN', (0, 1), (0, 2), 'MIDDLE'),
                ('VALIGN', (0, 3), (0, 4), 'MIDDLE'),
            ]))

            elements.append(Spacer(1, 12))
            elements.append(tabla_estadistica)
            elements.append(Spacer(1, 20))

            descripcion_texto = '<b>b. Descripción</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))

            parrafo_intro = Paragraph(
                "Espacio estático para incluir un texto, pendiente de construir, para explicar qué es y cómo interpretar los niveles de desempeño (dos párrafos cortos como máximo).",
                parrafo_estilo
            )

            elements.append(Spacer(1, 12))
            elements.append(parrafo_intro)   

            # Datos del gráfico
            niveles = ['Bajo', 'Medio', 'Alto']
            t = self.desempeño(0, institucion, "entrada", proyecto, 3, 'M', 5, 13)
            t2 = self.desempeño(0, institucion, "salida", proyecto, 3, 'M', 5, 13)
            c = self.desempeño(1, institucion, "entrada", proyecto, 3, 'M', 5, 13)
            c2 = self.desempeño(1, institucion, "salida", proyecto, 3, 'M', 5, 13)

            # ================== GRÁFICO ENTRADA ==================
            x = range(len(niveles))
            bar_width = 0.35

            plt.figure(figsize=(5, 4))
            bars1 = plt.bar([i - bar_width/2 for i in x], t, width=bar_width, label='Entrada', color='#1B8830')
            bars2 = plt.bar([i + bar_width/2 for i in x], t2, width=bar_width, label='Salida', color='#6FBF73')

            for i, bar in enumerate(bars1):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{t[i]}%', ha='center', va='bottom', fontsize=10)

            for i, bar in enumerate(bars2):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{t2[i]}%', ha='center', va='bottom', fontsize=10)

            plt.xticks(x, niveles)
            plt.title('Distribución por Niveles de Desempeño - Institución\n')
            plt.legend()
            plt.tight_layout()

            # QUITAR eje Y
            plt.gca().axes.get_yaxis().set_visible(False)

            # QUITAR TODOS LOS BORDES, excepto abajo
            for spine in ['top', 'right', 'left']:
                plt.gca().spines[spine].set_visible(False)

            img_buffer1 = BytesIO()
            plt.savefig(img_buffer1, format='png')
            plt.close()
            img_buffer1.seek(0)
            grafico_entrada = RLImage(img_buffer1, width=260, height=200)

            # ================== GRÁFICO CIUDAD ==================
            plt.figure(figsize=(5, 4))
            bars1 = plt.bar([i - bar_width/2 for i in x], c, width=bar_width, label='Entrada', color='#1B8830')
            bars2 = plt.bar([i + bar_width/2 for i in x], c2, width=bar_width, label='Salida', color='#6FBF73')

            for i, bar in enumerate(bars1):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{c[i]}%', ha='center', va='bottom', fontsize=10)

            for i, bar in enumerate(bars2):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{c2[i]}%', ha='center', va='bottom', fontsize=10)

            plt.xticks(x, niveles)
            plt.title('Distribución por Niveles de Desempeño - Ciudad\n')
            plt.legend()
            plt.tight_layout()

            # QUITAR eje Y
            plt.gca().axes.get_yaxis().set_visible(False)

            # QUITAR TODOS LOS BORDES, excepto abajo
            for spine in ['top', 'right', 'left']:
                plt.gca().spines[spine].set_visible(False)

            img_buffer2 = BytesIO()
            plt.savefig(img_buffer2, format='png')
            plt.close()
            img_buffer2.seek(0)
            grafico_salida = RLImage(img_buffer2, width=260, height=200)

            # ================== AGREGAR AMBOS AL PDF ==================
            tabla_graficos = Table([[grafico_entrada, grafico_salida]], colWidths=[270, 270])
            elements.append(Spacer(1, 12))
            elements.append(tabla_graficos)
            elements.append(Spacer(1, 20))           

            descripcion_texto = '<b>Significado de los niveles de desempeño – Matemáticas, tercer grado</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style)) 

            # Tabla descriptiva de niveles de desempeño
            niveles_data = [
                [
                    Paragraph("<b>Bajo<br/>(entre 1 y 6 puntos)</b>", parrafo_estilo),
                    Paragraph("El estudiante ubicado en este nivel de desempeño: <br/>"
                            "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", parrafo_estilo)
                ],
                [
                    Paragraph("<b>Medio<br/>(entre 7 y 13 puntos)</b>", parrafo_estilo),
                    Paragraph("Además de lo descrito en el nivel anterior, el estudiante ubicado en este nivel: <br/>"
                            "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", parrafo_estilo)
                ],
                [
                    Paragraph("<b>Alto<br/>(entre 14 y 20 puntos)</b>", parrafo_estilo),
                    Paragraph("Además de lo descrito en los niveles anteriores, el estudiante ubicado en este nivel: <br/>"
                            "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", parrafo_estilo)
                ],
            ]

            tabla_niveles = Table(niveles_data, colWidths=[180, 300])
            tabla_niveles.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10.5),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('LINEBELOW', (0, 0), (-1, -2), 0.25, colors.grey),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey)
            ]))

            elements.append(Spacer(1, 12))
            elements.append(tabla_niveles)
            
            #-----------------------------------------------------------------------------------------------------------------------

            descripcion_texto = '<b>4.2.	Quinto grado</b><br/><b>a. Puntaje</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))

            parrafo_intro = Paragraph(
                "Espacio estático para incluir un texto, pendiente de construir, para explicar que el puntaje se presenta en una escala de 0 a 20 puntos, qué es el promedio y la desviación estándar (dos párrafos cortos como máximo).",
                parrafo_estilo
            )

            elements.append(Spacer(1, 12))
            elements.append(parrafo_intro)   
            
            t = self.tabla(0, institucion, 'entrada',proyecto, 5, 'M')
            c = self.tabla(1, ciudad, 'entrada',proyecto, 5, 'M')
            t2 = self.tabla(0, institucion, 'salida',proyecto, 5, 'M')
            c2 = self.tabla(1, ciudad, 'salida',proyecto, 5, 'M')
            
            tabla_datos = [
                ["", "Aplicación", "# evaluados", "Media", "Desv. est.", "Mínimo", "Máximo"],  # Encabezados
                ["Institución", "Entrada",t[0], self.comma_dot(t[1]), self.comma_dot(t[2]), t[3], t[4]],  # Fila 1
                ['', "Salida",t2[0], self.comma_dot(t2[1]), self.comma_dot(t2[2]), t2[3], t2[4]],  # Fila 2
                ["Municipio", "Entrada",c[0], self.comma_dot(c[1]), self.comma_dot(c[2]), c[3], c[4]],  # Fila 3
                ['', "Salida",c2[0], self.comma_dot(c2[1]), self.comma_dot(c2[2]), c2[3], c2[4]],  # Fila 4
            ]

            # Crear la tabla
            tabla_estadistica = Table(tabla_datos, colWidths=[130, 80, 80, 60, 80, 60, 60])
            tabla_estadistica.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor("#1B8830")),  # Fondo verde para encabezados
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),          # Texto blanco en encabezados
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),          # Líneas de tabla
                # Unir columna 0 de fila 1 y 2 (índices 1 y 2)
                ('SPAN', (0, 1), (0, 2)),

                # Unir columna 0 de fila 3 y 4 (índices 3 y 4)
                ('SPAN', (0, 3), (0, 4)),

                # Alineación vertical centrada en las celdas unidas
                ('VALIGN', (0, 1), (0, 2), 'MIDDLE'),
                ('VALIGN', (0, 3), (0, 4), 'MIDDLE'),
            ]))

            elements.append(Spacer(1, 12))
            elements.append(tabla_estadistica)
            elements.append(Spacer(1, 20))

            descripcion_texto = '<b>b. Descripción</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style))

            parrafo_intro = Paragraph(
                "Espacio estático para incluir un texto, pendiente de construir, para explicar qué es y cómo interpretar los niveles de desempeño (dos párrafos cortos como máximo).",
                parrafo_estilo
            )

            elements.append(Spacer(1, 12))
            elements.append(parrafo_intro)   

            # Datos del gráfico
            niveles = ['Bajo', 'Medio', 'Alto']
            t = self.desempeño(0, institucion, "entrada", proyecto, 3, 'M', 5, 13)
            t2 = self.desempeño(0, institucion, "salida", proyecto, 3, 'M', 5, 13)
            c = self.desempeño(1, institucion, "entrada", proyecto, 3, 'M', 5, 13)
            c2 = self.desempeño(1, institucion, "salida", proyecto, 3, 'M', 5, 13)

            # ================== GRÁFICO CIUDAD ==================
            x = range(len(niveles))
            bar_width = 0.35

            plt.figure(figsize=(5, 4))
            bars1 = plt.bar([i - bar_width/2 for i in x], t, width=bar_width, label='Entrada', color='#1B8830')
            bars2 = plt.bar([i + bar_width/2 for i in x], t2, width=bar_width, label='Salida', color='#6FBF73')

            for i, bar in enumerate(bars1):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{t[i]}%', ha='center', va='bottom', fontsize=10)

            for i, bar in enumerate(bars2):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{t2[i]}%', ha='center', va='bottom', fontsize=10)

            plt.xticks(x, niveles)
            plt.title('Distribución por Niveles de Desempeño - Institución\n')
            plt.legend()
            plt.tight_layout()

            # QUITAR eje Y
            plt.gca().axes.get_yaxis().set_visible(False)

            # QUITAR TODOS LOS BORDES, excepto abajo
            for spine in ['top', 'right', 'left']:
                plt.gca().spines[spine].set_visible(False)

            img_buffer1 = BytesIO()
            plt.savefig(img_buffer1, format='png')
            plt.close()
            img_buffer1.seek(0)
            grafico_entrada = RLImage(img_buffer1, width=260, height=200)

            # ================== GRÁFICO SALIDA ==================
            plt.figure(figsize=(5, 4))
            bars1 = plt.bar([i - bar_width/2 for i in x], c, width=bar_width, label='Entrada', color='#1B8830')
            bars2 = plt.bar([i + bar_width/2 for i in x], c2, width=bar_width, label='Salida', color='#6FBF73')

            for i, bar in enumerate(bars1):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{c[i]}%', ha='center', va='bottom', fontsize=10)

            for i, bar in enumerate(bars2):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{c2[i]}%', ha='center', va='bottom', fontsize=10)

            plt.xticks(x, niveles)
            plt.ylabel('')
            plt.title('Distribución por Niveles de Desempeño - Ciudad\n')
            plt.legend()
            plt.tight_layout()

            # QUITAR eje Y
            plt.gca().axes.get_yaxis().set_visible(False)

            # QUITAR TODOS LOS BORDES, excepto abajo
            for spine in ['top', 'right', 'left']:
                plt.gca().spines[spine].set_visible(False)

            img_buffer2 = BytesIO()
            plt.savefig(img_buffer2, format='png')
            plt.close()
            img_buffer2.seek(0)
            grafico_salida = RLImage(img_buffer2, width=260, height=200)

            # ================== AGREGAR AMBOS AL PDF ==================
            tabla_graficos = Table([[grafico_entrada, grafico_salida]], colWidths=[270, 270])
            elements.append(Spacer(1, 12))
            elements.append(tabla_graficos)
            elements.append(Spacer(1, 20))    

            descripcion_texto = '<b>Significado de los niveles de desempeño – Matemáticas, quinto grado</b>'
            elements.append(Paragraph(descripcion_texto, descripcion_izq_style)) 

            # Tabla descriptiva de niveles de desempeño
            niveles_data = [
                [
                    Paragraph("<b>Bajo<br/>(entre 1 y 5 puntos)</b>", parrafo_estilo),
                    Paragraph("El estudiante ubicado en este nivel de desempeño: <br/>"
                            "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", parrafo_estilo)
                ],
                [
                    Paragraph("<b>Medio<br/>(entre 6 y 10 puntos)</b>", parrafo_estilo),
                    Paragraph("Además de lo descrito en el nivel anterior, el estudiante ubicado en este nivel: <br/>"
                            "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", parrafo_estilo)
                ],
                [
                    Paragraph("<b>Alto<br/>(entre 11 y 20 puntos)</b>", parrafo_estilo),
                    Paragraph("Además de lo descrito en los niveles anteriores, el estudiante ubicado en este nivel: <br/>"
                            "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", parrafo_estilo)
                ],
            ]

            tabla_niveles = Table(niveles_data, colWidths=[180, 300])
            tabla_niveles.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10.5),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('LINEBELOW', (0, 0), (-1, -2), 0.25, colors.grey),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey)
            ]))

            elements.append(Spacer(1, 12))
            elements.append(tabla_niveles)
            
            #-----------------------------------------------------------------------------------------------------------------------

            # Crear documento base
            doc.build(elements, onFirstPage=self.agregar_marca_agua, onLaterPages=self.agregar_numero_pagina)

            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename=\"reporte_comparativo.pdf\"'
            return response

        except Exception as e:
            print("ERROR:", format_exc())
            return Response({
                "error": "Error interno al generar el PDF.",
                "detalle": str(e)
            }, status=500)

    def agregar_marca_agua(self, canvas_obj, doc):
        width, height = letter
        canvas_obj.saveState()
        canvas_obj.setFont("Helvetica-Bold", 80)
        canvas_obj.setFillColorRGB(1, 1, 1)
        canvas_obj.translate(width / 2, height / 2)
        canvas_obj.rotate(45)
        canvas_obj.drawCentredString(0, 0, "CONFIDENCIAL")
        canvas_obj.restoreState()

    def tabla(self, modo, institucion, aplicacion, proyecto, grado, materia):
        
        if grado == 3:
            grado_str = 'Tercero'
        else:
            grado_str = 'Quinto'
        
        if materia == 'M':
            prueba = 'Matemáticas'
        else:
            prueba = 'Lenguaje'

        if modo == 0:   
            encuestas = Encuesta.objects.filter(
                aplicacion=aplicacion,
                nombre_institucion=institucion,
                nombre=proyecto,
                grado=grado_str,
                prueba=prueba
            )
        else:
            encuestas = Encuesta.objects.filter(
                aplicacion=aplicacion,
                nombre=proyecto,
                grado=grado_str,
                prueba=prueba
            )

        data = []
        maxi = 0
        mini = 20
        for encuesta in encuestas:
            if maxi < encuesta.correctos:
                maxi = encuesta.correctos
            if mini > encuesta.correctos:
                mini = encuesta.correctos
            data.append(encuesta.correctos)

        if not data:
            return [0, 0, 0, 0, 0]

        media = sum(data)/len(data)

        suma_cuadrados = sum((x - media) ** 2 for x in data)
        desviacion_estandar = math.sqrt(suma_cuadrados / (len(data) - 1))

        return [
            len(data),
            round(float(media), 1),
            round(float(desviacion_estandar), 1),
            mini,
            maxi
        ]
    
    def desempeño(self, modo, institucion, aplicacion, proyecto, grado, materia, a, b):
        bajo = 0
        medio = 0
        alto = 0
        if grado == 3:
            grado_str = 'Tercero'
        else:
            grado_str = 'Quinto'
        
        if materia == 'M':
            prueba = 'Matemáticas'
        else:
            prueba = 'Lenguaje'

        if modo == 0:   
            encuestas = Encuesta.objects.filter(
                aplicacion=aplicacion,
                nombre_institucion=institucion,
                nombre=proyecto,
                grado=grado_str,
                prueba=prueba
            )
        else:
            encuestas = Encuesta.objects.filter(
                aplicacion=aplicacion,
                nombre=proyecto,
                grado=grado_str,
                prueba=prueba
            )
        
        total = encuestas.count()
        if total == 0:
            return [0, 0, 0]  # Evita división por cero

        for encuesta in encuestas:
            if encuesta.correctos is None:
                continue
            if encuesta.correctos < a:
                bajo+=1
            elif encuesta.correctos < b:
                medio+=1
            else:
                alto+=1
        
        total = bajo + medio + alto

        return [int((bajo/total)*100), int((medio/total)*100), int((alto/total)*100)]
    
    def agregar_numero_pagina(self, canvas, doc):
        page_num = canvas.getPageNumber()
        text = f"{page_num}"
        canvas.setFont('Helvetica', 9)

        # Obtiene el ancho de la página para posicionar a la derecha
        width, height = letter

        # Ajusta la posición: derecha (margen derecho - ancho del texto)
        text_width = canvas.stringWidth(text, 'Helvetica', 9)
        x = width - inch * 0.5 # Una pulgada del borde derecho
        y = 0.5 * inch  # Desde el borde inferior

        canvas.drawString(x, y, text)


    def tabla_inicial(self, M3_E, E3_E, M3_S, E3_S, M5_E, E5_E, M5_S, E5_S):
        p = []

        p.append(round(float((E3_E/M3_E)*100), 1))
        p.append(round(float((E5_E/M5_E)*100), 1))
        p.append(round(float(((E3_E + E5_E)/(M3_E + M5_E))*100), 1))
        p.append(round(float((E3_S/M3_S)*100), 1))
        p.append(round(float((E5_S/M5_S)*100), 1))
        p.append(round(float(((E3_S + E5_S)/(M3_S + M5_S))*100), 1))

        return p
    
    def comma_dot(self, x):
        res = str(x)
        res = res.replace('.',',')
        return res

class CrearInstitucionAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = InstitucionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
