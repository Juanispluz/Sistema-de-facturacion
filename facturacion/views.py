from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from django.utils import timezone
from django.db.models import Case, When, IntegerField
from django.db import transaction

# Vista del index
def index(request):
    if "logueado" in request.session:
        cedula = request.session["logueado"]["cedula"]
        servicios = Usuarios_servicios.objects.filter(usuario_ID_id=cedula)
        servicios_activos = servicios.filter(tiene_servicio=True)
        servicios_inactivos = servicios.filter(tiene_servicio=False)
        sin_servicios = not (servicios_activos.exists() or servicios_inactivos.exists())
        context = {
            'servicios_activos': servicios_activos,
            'servicios_inactivos': servicios_inactivos,
            'sin_servicios': sin_servicios
        }
        return render(request, 'index.html', context)
    messages.warning(request, "Por favor inicie sesión")
    return redirect("login")

# -----------------------------------------------------------------------------------
# Sesion
def login(request):
    if "logueado" in request.session:
        return redirect("index")
    if request.method == "POST":
        cedula = request.POST.get("cedula")
        clave = request.POST.get("password")
        try:
            usuario = Usuario.objects.get(cedula=cedula)
            if check_password(clave, usuario.password):  # Esto está correcto
                request.session["logueado"] = {
                    "cedula": usuario.cedula,
                    "nombre": f"{usuario.nombre} {usuario.apellido}",
                    "rol": usuario.rol
                }
                return redirect("index")
            messages.error(request, "Usuario o contraseña incorrecta")
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado")
    return render(request, "login/login.html")

def register(request):
    if "logueado" in request.session:
        return redirect("index")
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        celular = request.POST.get('celular')  
        cedula = request.POST.get('cedula')
        direccion = request.POST.get('direccion')
        password = request.POST.get('passwd')
        password_confirm = request.POST.get('passwd_confirm')
        if Usuario.objects.filter(cedula=cedula).exists():
            messages.info(request, "Ya está registrado este usuario")
            return render(request, "login/register.html")
        if password != password_confirm:
            messages.warning(request, "Las contraseñas deben coincidir")
            return render(request, "login/register.html")

        # Hashea la contraseña aquí
        hashed_password = make_password(password)
        
        # Crea el registro con la contraseña hasheada
        registro = Usuario(
            nombre=nombre, 
            apellido=apellido,
            celular=celular,
            cedula=cedula,
            direccion=direccion,
            password=hashed_password,  # Usa la contraseña hasheada
            rol='U'
        )
        registro.save()
        messages.success(request, "Registro exitoso. Por favor, inicie sesión.")
        return redirect('login')
    return render(request, "login/register.html")

def logout(request):
    if "logueado" in request.session:
        del request.session["logueado"]
        messages.success(request, "Has cerrado sesión exitosamente")
    else:
        messages.info(request, "No había una sesión activa")
    
    return redirect("login")

# -----------------------------------------------------------------------------------
# Usuarios
def usuario(request):
    if "logueado" not in request.session:
        messages.warning(request, "Por favor inicie sesión para ver su información.")
        return redirect("login")
    cedula = request.session["logueado"]["cedula"]
    usuario_info = Usuario.objects.get(cedula=cedula)
    contratos = Contratos.objects.filter(usuario_ID_id=usuario_info.cedula)
    context = {
        'usuario': usuario_info,
        'contratos': contratos
    }
    return render(request, "usuarios/usuario.html", context)

# Vista del administrador
def administrador(request):
    return render(request, "admin/index.html")
    
# -----------------------------------------------------------------------------------
# Facturas
def ver_facturas(request, servicio_ID):
    if "logueado" not in request.session:
        messages.warning(request, "Por favor inicie sesión.")
        return redirect("login")
    cedula = request.session["logueado"]["cedula"]
    contratos_usuario = Contratos.objects.filter(usuario_ID_id=cedula)
    facturas = Facturas.objects.filter(
        numero_contrato_ID__in=contratos_usuario,
        servicio_ID_id=servicio_ID
    ).exclude(
        estado='P'
    ).annotate(
        prioridad_estado=Case(
            When(estado='V', then=1),
            When(estado='PE', then=2),
            default=3,
            output_field=IntegerField()
        )
    ).order_by('prioridad_estado')
    context = {
        'facturas': facturas
    }
    return render(request, "facturas/ver_facturas.html", context)

def pagar_facturas(request, servicio_id):
    if not request.session.get('logueado'):
        return redirect('login')
    cedula = request.session['logueado']['cedula']
    contratos_usuario = Contratos.objects.filter(usuario_ID_id=cedula)
    factura = Facturas.objects.filter(
        numero_contrato_ID__in=contratos_usuario,
        servicio_ID_id=servicio_id,
        estado__in=['PE', 'V']
    ).first()
    if not factura:
        messages.error(request, 'No se encontró la factura especificada.')
        return redirect('index')
    if request.method == 'POST':
        metodo_pago = request.POST.get('metodo_pago')
        valor_factura = factura.valor
        with transaction.atomic():
            Historial_facturas.objects.create(
                usuario_ID_id=cedula,
                facturas_ID=factura,
                valor=valor_factura,
                metodo_pago=metodo_pago,
                fecha_pago=timezone.now()
            )
            factura.estado = 'P'
            factura.save()
            messages.success(request, 'Pago realizado con éxito.')
            return redirect('ver_facturas', servicio_ID=servicio_id)
    
    return render(request, 'facturas/pagar_facturas.html', {'factura': factura})

def historial_facturas(request):
    if "logueado" not in request.session:
        messages.warning(request, "Por favor inicie sesión.")
        return redirect("login")
    cedula = request.session["logueado"]["cedula"]
    contratos_usuario = Contratos.objects.filter(usuario_ID_id=cedula)
    facturas_pagadas = Facturas.objects.filter(
        numero_contrato_ID__in=contratos_usuario,
        estado='P'
    ).select_related('servicio_ID', 'numero_contrato_ID')
    historiales = Historial_facturas.objects.filter(
        facturas_ID__in=facturas_pagadas
    ).select_related('facturas_ID')
    context = {
        'historiales': historiales
    }
    return render(request, "facturas/historial_facturas.html", context)

def contrato(request):
    if "logueado" not in request.session:
        messages.warning(request, "Por favor inicie sesión.")
        return redirect("login")
    cedula = request.session["logueado"]["cedula"]
    usuario = Usuario.objects.get(cedula=cedula)
    servicios_usuario = Usuarios_servicios.objects.filter(usuario_ID=usuario, tiene_servicio=True)
    servicios_adquiridos_ids = servicios_usuario.values_list('servicios_ID', flat=True)
    servicios_disponibles = Servicios.objects.exclude(id__in=servicios_adquiridos_ids)
    if request.method == "POST":
        servicios_seleccionados = request.POST.getlist("servicios")
        if servicios_seleccionados:
            for servicio_id in servicios_seleccionados:
                servicio = Servicios.objects.get(id=servicio_id)
                Usuarios_servicios.objects.create(
                    usuario_ID=usuario,
                    servicios_ID=servicio,
                    tiene_servicio=True
                )
                nuevo_contrato = Contratos.objects.create(
                    usuario_ID=usuario,
                    estado="A",
                    fecha_contrato=timezone.now()
                )
                Facturas.objects.create(
                    servicio_ID=servicio,
                    numero_contrato_ID=nuevo_contrato,
                    fecha_emision=timezone.now(),
                    fecha_vencimiento=timezone.now() + timezone.timedelta(days=30),
                    valor=10000.32,
                    estado='PE'
                )
            messages.success(request, "Servicios contratados exitosamente y facturas generadas.")
            return redirect("index")
    context = {
        "servicios_usuario": servicios_usuario,
        "servicios_disponibles": servicios_disponibles
    }
    return render(request, "facturas/contrato.html", context)

def cancelar_servicio(request):
    pass