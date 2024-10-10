from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *

# Create your views here.

# El index
def index(request):
    # Verifica si el usuario está logueado
    if "logueado" in request.session:
        cedula = request.session["logueado"]["cedula"]  # Obtiene la cédula del usuario logueado
        # Busca los servicios que tiene el usuario
        servicios = Usuarios_servicios.objects.filter(usuario_ID=cedula)

        # Servicios activos
        servicios_activos = servicios.filter(tiene_servicio=True)

        # Servicios inactivos
        servicios_inactivos = servicios.filter(tiene_servicio=False)

        sin_servicios = not (servicios_activos.exists() or servicios_inactivos.exists())

        context = {
            'servicios_activos': servicios_activos,
            'servicios_inactivos': servicios_inactivos,
            'sin_servicios': sin_servicios  # Pasa esta variable a la plantilla
        }

        return render(request, 'index.html', context)

    else:
        messages.warning(request, "Por favor inicie sesión")
        return redirect("login")

# Sesion
def login(request):
    # Si el usuario ya está logueado, no lo deja acceder al login
    if "logueado" in request.session:
        return redirect("index")
    
    if request.method == "POST":
        cedula = request.POST.get("cedula")
        clave = request.POST.get("password")

        try:
            usuario = Usuario.objects.get(cedula=cedula)
            
            if check_password(clave, usuario.password):
                # Iniciar sesión guardando los datos
                request.session["logueado"] = {
                    "cedula": usuario.cedula,
                    "nombre": f"{usuario.nombre} {usuario.apellido}",
                    "rol": usuario.rol
                }
                return redirect("index")
            else:
                messages.error(request, "Contraseña incorrecta")
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

        # Verificación de cédula
        if Usuario.objects.filter(cedula=cedula).exists():
            messages.info(request, "Ya está registrado este usuario")  
            return render(request, "login/register.html")

        # Verificación de contraseñas
        if password != password_confirm:
            messages.warning(request, "Las contraseñas deben coincidir")
            return render(request, "login/register.html", {'error': 'Las contraseñas no coinciden.'})

        registro = Usuario(
            nombre=nombre, 
            apellido=apellido,
            celular=celular,
            cedula=cedula,
            direccion=direccion,
            password=password,
            rol='U'
        )

        registro.save()
        return redirect('login')
    
    return render(request, "login/register.html")

def logout(request):
    if "logueado" in request.session:
        # Elimina la variable de sesión
        del request.session["logueado"]
        # También puedes usar request.session.flush() para eliminar todas las variables de sesión
        
        messages.success(request, "Has cerrado sesión exitosamente")
    else:
        messages.info(request, "No había una sesión activa")
    
    # Redirige al usuario a la página de inicio o login
    return redirect("login")

# Usuario
def usuario(request):
    # Verifica si el usuario está logueado
    if "logueado" not in request.session:
        messages.warning(request, "Por favor inicie sesión para ver su información.")
        return redirect("login")

    cedula = request.session["logueado"]["cedula"]
    usuario_info = Usuario.objects.get(cedula=cedula)

    context = {
        'usuario': usuario_info
    }

    return render(request, "usuarios/usuario.html", context)


# Admin
def administrador(request):
    return render(request, "admin/index.html")

# Facturas  - Usuarios
def ver_facturas(request, servicio_ID):
# Verifica si el usuario está logueado
    if "logueado" not in request.session:
        messages.warning(request, "Por favor inicie sesión.")
        return redirect("login")

    # Obtener las facturas del usuario
    cedula = request.session["logueado"]["cedula"]
    facturas = Facturas.objects.filter(usuario_ID__cedula=cedula)

    context = {
        'facturas': facturas
    }

    return render(request, "facturas/ver_facturas.html", context)

def pagar_facturas(request, servicio_id):
    return render(request, "facturas/pagar_facturas.html", {'servicio_id': servicio_id})
