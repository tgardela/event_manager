from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from auth.views import (
    MyObtainTokenPairView,
    RegisterView,
    UserView,
    )


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('user/', UserView.as_view({'get': 'list'}), name='auth_user'),
    path('user/<int:pk>', UserView.as_view({'get': 'retrieve'}), name='auth_user'),
    ]
