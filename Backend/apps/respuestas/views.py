import random
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from traceback import format_exc

from rest_framework import permissions
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Encuesta, CuadernilloMate, CuadernilloLengua
from .serializers import EncuestaSerializer, CuadernilloMateSerializer, PreguntaMateSerializer, PreguntaLenguaSerializer, Encuesta2Serializer
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

            # Preparar los datos
            data = []
            for encuesta in encuestas:
                estudiante = encuesta.nombre_estudiante or "N/A"
                grado = encuesta.grado or "N/A"
                correctos = encuesta.correctos if encuesta.correctos is not None else 0
                data.append([estudiante, grado, correctos])

            df = pd.DataFrame(data, columns=["Estudiante", "Grado", "Correctas"])

            buffer = BytesIO()

            # Crear el documento
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []

            # Estilos
            styles = getSampleStyleSheet()
            title = Paragraph(f"<b>Reporte Institución:</b> {institucion}<br/><b>Proyecto:</b> {proyecto} | <b>Aplicación:</b> {aplicacion}", styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 20))

            # Tabla
            table_data = [df.columns.tolist()] + df.values.tolist()
            tabla = Table(table_data)
            tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(tabla)

            # Crear documento base
            doc.build(elements, onFirstPage=self.agregar_marca_agua, onLaterPages=self.agregar_marca_agua)

            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename=\"reporte_{institucion}_{proyecto}.pdf\"'
            return response

        except Exception as e:
            print("🔴 ERROR:", format_exc())
            return Response({
                "error": "Error interno al generar el PDF.",
                "detalle": str(e)
            }, status=500)

    def agregar_marca_agua(self, canvas_obj, doc):
        width, height = letter
        canvas_obj.saveState()
        canvas_obj.setFont("Helvetica-Bold", 80)
        canvas_obj.setFillColorRGB(0.83, 0.83, 0.83)
        canvas_obj.translate(width / 2, height / 2)
        canvas_obj.rotate(45)
        canvas_obj.drawCentredString(0, 0, "CONFIDENCIAL")
        canvas_obj.restoreState()
