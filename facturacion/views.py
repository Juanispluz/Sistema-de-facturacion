from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *


# Create your views here.

# El index
def index(request):
    return render(request, 'index.html')

# Admin
def administrador(request):
    return render(request, "admin/index.html")


# Facturas - Usuarios
def ver_servicios(request):
    query = Servicios.objects.all()
    messages.info(request, "La consulta esta ok")
    contexto = {"servicios": query}
    return render(request, "facturas/index.html")