from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import UserAccount
from .serializers import UserAccountSerializer

User = get_user_model()

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
            elif (user.is_terpel):
                response.data['role'] = 'terpel'
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
        elif user.is_terpel:
            return 'terpel'
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

class ChangePasswordView(APIView):
    permission_classes = (permissions.AllowAny,) 

    def post(self, request):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not new_password:
            return Response({"error": "Debes enviar la contraseña la nueva."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(current_password):
            return Response({"error": "La contraseña actual es incorrecta."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Contraseña actualizada correctamente."}, status=status.HTTP_200_OK)

class AdminChangeUserPasswordView(APIView):
    permission_classes = (permissions.AllowAny,) 
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')

        if not email or not new_password:
            return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserAccount.objects.get(email=email)
            if user.is_admin:
                return Response({'error': 'No se puede cambiar la contraseña de un administrador.'}, status=status.HTTP_403_FORBIDDEN)

            user.set_password(new_password)
            user.save()
            return Response({'message': 'Contraseña actualizada correctamente.'}, status=status.HTTP_200_OK)
        except UserAccount.DoesNotExist:
            return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

class ListAllNonAdminUsersView(APIView):
    permission_classes = (permissions.AllowAny,) 

    def get(self, request):
        try:
            users = UserAccount.objects.filter(is_admin=False)
            serializer = UserAccountSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)