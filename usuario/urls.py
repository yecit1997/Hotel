from django.urls import path

from .views import Roles, RolDetail, Usuarios, UsuariosDetail

urlpatterns = [
    path('roles/', Roles.as_view(), name='roles'),
    path('rol/<str:pk>/', RolDetail.as_view(), name='rol'),
    
    path('usuarios/', Usuarios.as_view(), name='usuarios'),
    path('usuario/<str:pk>/', UsuariosDetail.as_view(), name='usuario'),
    
]
