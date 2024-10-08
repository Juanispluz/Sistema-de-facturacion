from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages


# Create your views here.

# El index
def index(request):
    return render(request, 'index.html')

# Admin
def administrador(request):
    return render(request, "admin/index.html")


# Facturas - Usuarios
def ver_facturas(request):
    return render(request, "facturas/index.html")