from django.urls import path
from . import views

# Urls de la aplicación facturación

urlpatterns = [
    # Inicio
    path("", views.index, name="index"),

    # Admin
    path("admon/", views.administrador, name="administrador"),

    # Login
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),

    # Usuario
    path("usuario/", views.usuario, name="usuario"),

    # Facturas - Usuarios
    path("facturas/<int:servicio_ID>/", views.ver_facturas, name="ver_facturas"),
    path('pagar_facturas/<int:servicio_id>/', views.pagar_facturas, name='pagar_facturas'),
    path("historial/", views.historial_facturas, name='historial'),
    path("contrato/", views.contrato, name="contratos"),
]