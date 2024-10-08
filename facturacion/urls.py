from django.urls import path
from . import views

# Urls de la aplicación facturación

urlpatterns = [
    path("", views.index, name="index"),
]