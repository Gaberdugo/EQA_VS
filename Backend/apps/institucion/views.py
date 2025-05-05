from rest_framework import permissions
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import InstitutoSerializer
from rest_framework.permissions import AllowAny

class CrearInstitucionAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = InstitutoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
