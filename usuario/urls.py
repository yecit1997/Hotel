from django.urls import path

from .views import Roles

urlpatterns = [
    path('roles/', Roles.as_view(), name='lista_roles')
]
