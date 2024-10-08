from django.urls import path
from . import views

# Urls de la aplicación facturación

urlpatterns = [
    # Inicio
    path("", views.index, name="index"),

    # Admin
    path("administrador/", views.administrador, name="administrador"),


    # Facturas - Usuarios
    path("facturas/", views.ver_facturas, name="ver_facturas"),
]