from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import UserAccount
from .serializers import UserAccountSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
    
        try:
            user = UserAccount.objects.get(email=request.data['email'])
            if (user.is_admin):
                response.data['role'] = 'admin' 
            elif (user.is_digi):
                response.data['role'] = 'digitador'
            elif (user.is_val):
                response.data['role'] = 'val'
            else:
                response.data['role'] = 'SIN'
        except UserAccount.DoesNotExist:
            response.data['role'] = 'undefined'
        
        response.data['correo'] = user.email

        return response

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_info = {
            'email': user.email,
            'is_admin': user.is_admin,
            'is_digi': user.is_digi,
            'is_val': user.is_val,
            'is_terpel': user.is_terpel,
            'role': self.get_user_role(user), 
        }
        return Response(user_info)

    def get_user_role(self, user):
        if user.is_admin:
            return 'admin'
        elif user.is_digi:
            return 'digitador'
        else:
            return 'user'

class CreateUserAccountView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        datos = request.data
        password = datos.pop("password", None)  # Extrae la contraseña
        role = datos.pop("role", None)  # Extrae el rol
        if not password:
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Define permisos basados en el rol
        if role == 'digitador':
            datos.update({'is_digi': True})
        elif role == 'validador':
            datos.update({'is_val': True})
        elif role == 'terpel':
            datos.update({'is_terpel': True})

        try:
            user = UserAccount.objects.create_user(**datos, password=password)
            return Response({"email": user.email, "message": "User created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ListDigitadoresView(APIView):
    permission_classes = (permissions.AllowAny,)  # Ajusta según tu necesidad

    def get(self, request):
        try:
            # Filtra usuarios con is_digi=True
            digitadores = UserAccount.objects.filter(is_digi=True)
            serializer = UserAccountSerializer(digitadores, many=True)  # Serializa los resultados
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
