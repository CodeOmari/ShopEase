from django.urls import path, include
from .views import CustomUserCreateView, current_user
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', CustomUserCreateView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh'),

    path('current-user/', current_user),
    
    path('api-auth/', include('rest_framework.urls')),
]