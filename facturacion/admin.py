from django.contrib import admin
from .models import *

# Register your models here.
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ["cedula", "nombre", "apellido", "celular", "direccion"]

class ServiciosAdmin(admin.ModelAdmin):
    list_display = ["usuario_ID", "agua", "luz", "gas", "internet", "telefonia", "cable"]

class ContratoAdmin(admin.ModelAdmin):
    list_display = ["id", "servicios_ID", "estado", "fecha_contrato"]

class FacturaAdmin(admin.ModelAdmin):
    list_display = ["id", "contrato_ID", "fecha_emision", "fecha_vencimineto", "valor", "estado"]

class PagoAdmin(admin.ModelAdmin):
    list_display = ["id", "factura_ID", "metodo_pago", "verificacion", "fecha_pago"]

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Servicios, ServiciosAdmin)
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Factura, FacturaAdmin)
admin.site.register(Pago, PagoAdmin)