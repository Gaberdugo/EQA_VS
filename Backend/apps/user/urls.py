from django.urls import path
from .views import MyTokenObtainPairView, UserProfileView, CreateUserAccountView, ListDigitadoresView

urlpatterns = [
    path('jwt/create/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/me/', UserProfileView.as_view(), name='user-profile'),
    path('create-user/', CreateUserAccountView.as_view(), name='create-user'),
    path('digitadores/', ListDigitadoresView.as_view(), name='List-digitadores'),
]