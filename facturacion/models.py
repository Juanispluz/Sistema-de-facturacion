# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Usuario(models.Model):
        cedula = models.IntegerField(primary_key=True)
        password = models.CharField(max_length=254) 
        nombre = models.CharField(max_length=100)
        apellido = models.CharField(max_length=100)
        celular = models.CharField(max_length=100)
        direccion= models.CharField(max_length=254)
        ROLES = (
            ('A', 'Administrador'),
            ('U', 'Usuario')
        )
        rol = models.CharField(max_length=1, choices=ROLES, default='U')

class Servicios(models.Model):
    # ForeignKey para relacionar con Usuario
    usuario_ID = models.ForeignKey(Usuario, on_delete=models.CASCADE, to_field='cedula')

    agua =  models.BooleanField(default=False)
    luz = models.BooleanField(default=False)
    gas = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    telefonia = models.BooleanField(default=False)
    cable = models.BooleanField(default=False)

class Contrato(models.Model):
    # ForeignKey para relacionar con Usuario
    servicios_ID = models.ForeignKey(Servicios, on_delete=models.CASCADE)

    C_ESTADO = (
        (1, "Activo"),
        (2, "Supendido"),
        (3, "Inactivo"),
        (4, "Finalizado")
    )
    estado = models.IntegerField(choices=C_ESTADO)
    fecha_contrato = models.DateField(help_text="Fecha del inicio del contrato")

class Factura(models.Model):
    # ForeignKey para relacionar con Usuario
    contrato_ID = models.ForeignKey(Contrato, on_delete=models.CASCADE)

    fecha_emision = models.DateField(help_text="Fecha de emision de la factura")
    fecha_vencimineto = models.DateField(help_text="Fecha de vencimiento de la factura")
    valor = models.BigIntegerField(default=0)

    C_FACTURA = (
        (1, "Pagada"),
        (2, "Pendiente"),
        (3, "Vencida")
    )
    estado =  models.IntegerField(choices=C_FACTURA)

class Pago(models.Model):
    # ForeignKey para relacionar con Usuario
    factura_ID = models.ForeignKey(Factura, on_delete=models.CASCADE)

    M_PAGO = (
        (1, "Transferencia Banaacaria"),
        (2, "Tarjeta de crédito"),
        (3, "Trajeta de débito"),
        (4, "Efectivo"),
        (5, "Billetera electronica"),
        (6, "Cheque"),
        (7, "Codígo QR")
    )
    metodo_pago =models.IntegerField(choices=M_PAGO)
    verificacion = models.BooleanField(default=False)
    fecha_pago = models.DateField(help_text="Fecha del pago de la factura")