from django.urls import path

from .views import (ClienteView, ClienteViewDetail, 

)

urlpatterns = [
    path('clientes/', ClienteView.as_view(), name='clientes-list-create'),
    path('clientes/<uuid:pk>/', ClienteViewDetail.as_view(), name='clientes-detail'),

]
