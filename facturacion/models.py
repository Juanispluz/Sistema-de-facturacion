# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.hashers import make_password


class Usuario(models.Model):
    cedula = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=254)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    celular = models.CharField(max_length=100)
    direccion = models.CharField(max_length=254)
    ROLES = (
        ('A', 'Administrador'),
        ('U', 'Usuario')
    )
    rol = models.CharField(max_length=1, choices=ROLES, default='U')

    # Antes de guardar la clave la hashea/encripta
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Servicios(models.Model):
    nombre_servicio = models.CharField(max_length=50)


class Usuarios_servicios(models.Model):
    usuario_ID = models.ForeignKey(Usuario, on_delete=models.CASCADE, to_field='cedula')
    servicios_ID = models.ForeignKey(Servicios, on_delete=models.CASCADE)
    tiene_servicio = models.BooleanField(default=False)


class Contratos(models.Model):
    # ForeignKey
    usuario_ID = models.ForeignKey(Usuario, on_delete=models.CASCADE, to_field='cedula')
    usuarios_servicios_ID = models.ForeignKey(Servicios, on_delete=models.CASCADE)

    C_ESTADO = (
        ('A', "Activo"),
        ('I', "Inactivo"),
        ('R', 'Reportado')
    )
    estado = models.CharField(max_length=1, choices=C_ESTADO)
    fecha_contrato = models.DateField(help_text="Fecha del contrato")


class Facturas(models.Model):
    # ForeignKey
    usuario_ID = models.ForeignKey(Usuario, on_delete=models.CASCADE, to_field='cedula')
    servicio_ID = models.ForeignKey(Servicios, on_delete=models.CASCADE)

    fecha_emision = models.DateField(help_text="Fecha de emision de la factura")
    fecha_vencimiento = models.DateField(help_text="Fecha de vencimiento de la factura")
    valor = models.DecimalField(default=0, max_digits=20, decimal_places=2)

    C_FACTURA = (
        ('P', "Pagada"),
        ('PE', "Pendiente"),
        ('V', "Vencida")
    )
    estado = models.CharField(max_length=2, choices=C_FACTURA, default='PE')


class Historial_facturas(models.Model):
    # ForeignKey para relacionar con Usuario
    usuario_ID = models.ForeignKey(Usuario, on_delete=models.CASCADE, to_field='cedula')
    facturas_ID = models.ForeignKey(Facturas, on_delete=models.CASCADE,)
    valor = models.DecimalField(default=0, max_digits=20, decimal_places=2)

    M_PAGO = (
        (1, "Transferencia Bancaria"),
        (2, "Tarjeta de crédito"),
        (3, "Tarjeta de débito"),
        (4, "Efectivo"),
        (5, "Billetera electrónica"),
        (6, "Cheque"),
        (7, "Código QR")
    )
    metodo_pago = models.IntegerField(choices=M_PAGO)
    fecha_pago = models.DateField(help_text="Fecha del pago de la factura")