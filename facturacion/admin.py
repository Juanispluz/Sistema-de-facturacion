from django.contrib import admin
from .models import *

# Register your models here.
class Usuario_Admin(admin.ModelAdmin):
    list_display = ["cedula", "nombre", "apellido", "celular", "direccion", 'rol']

class Servicios_Admin(admin.ModelAdmin):
    list_display = ["id", "nombre_servicio"]

class Usuarios_servicios_Admin(admin.ModelAdmin):
    list_display = ["id", "usuario_ID", "servicios_ID", "tiene_servicio"]

class Contratos_Admin(admin.ModelAdmin):
    list_display = ["numero_contrato", "usuario_ID", "estado", "fecha_contrato"]

class Facturas_Admin(admin.ModelAdmin):
    list_display = ["id", "servicio_ID", "numero_contrato_ID", "fecha_emision", "fecha_vencimiento", "estado", "valor"]

class Historial_facturas_Admin(admin.ModelAdmin):
    list_display = ["id", "usuario_ID", "facturas_ID", "valor", "metodo_pago", "fecha_pago"]

admin.site.register(Usuario, Usuario_Admin)
admin.site.register(Servicios, Servicios_Admin)
admin.site.register(Usuarios_servicios, Usuarios_servicios_Admin)
admin.site.register(Contratos, Contratos_Admin)
admin.site.register(Facturas, Facturas_Admin)
admin.site.register(Historial_facturas, Historial_facturas_Admin)