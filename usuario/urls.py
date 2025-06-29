from django.urls import path

from .views import RolesView, RolViewDetail, UsuariosView, UsuariosViewDetail, LoginAPIView

urlpatterns = [
    path('roles/', RolesView.as_view(), name='roles'),
    path('rol/<str:pk>/', RolViewDetail.as_view(), name='rol'),
    
    path('usuarios/', UsuariosView.as_view(), name='usuarios'),
    path('usuario/<str:pk>/', UsuariosViewDetail.as_view(), name='usuario'),
    
    path('login/', LoginAPIView.as_view(), name='login'),
    
]
