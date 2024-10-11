from django.db import models
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

class Contratos(models.Model):
    numero_contrato = models.AutoField(primary_key=True)  # Cambia a AutoField para generar automáticamente el número
    usuario_ID = models.ForeignKey(Usuario, on_delete=models.CASCADE, to_field='cedula')
    
    C_ESTADO = (
        ('A', "Activo"),
        ('I', "Inactivo"),
        ('R', 'Reportado')
    )
    estado = models.CharField(max_length=1, choices=C_ESTADO)
    fecha_contrato = models.DateField(help_text="Fecha del contrato")


class Servicios(models.Model):
    id = models.AutoField(primary_key=True)  # Cambia a AutoField
    nombre_servicio = models.CharField(max_length=50)


class Usuarios_servicios(models.Model):
    id = models.AutoField(primary_key=True)  # Cambia a AutoField
    usuario_ID = models.ForeignKey(Usuario, on_delete=models.CASCADE, to_field='cedula')
    servicios_ID = models.ForeignKey(Servicios, on_delete=models.CASCADE)
    tiene_servicio = models.BooleanField(default=False)


class Facturas(models.Model):
    id = models.AutoField(primary_key=True)  # Cambia a AutoField
    servicio_ID = models.ForeignKey(Servicios, on_delete=models.CASCADE)
    numero_contrato_ID = models.ForeignKey(Contratos, on_delete=models.CASCADE)  # Cambiado a FK de Contratos
    fecha_emision = models.DateField(help_text="Fecha de emisión de la factura")
    fecha_vencimiento = models.DateField(help_text="Fecha de vencimiento de la factura")
    
    C_FACTURA = (
        ('P', "Pagada"),
        ('PE', "Pendiente"),
        ('V', "Vencida")
    )
    estado = models.CharField(max_length=2, choices=C_FACTURA, default='PE')
    valor = models.DecimalField(default=0, max_digits=20, decimal_places=2)


class Historial_facturas(models.Model):
    id = models.AutoField(primary_key=True)  # Cambia a AutoField
    usuario_ID = models.ForeignKey(Usuario, on_delete=models.CASCADE, to_field='cedula')
    facturas_ID = models.ForeignKey(Facturas, on_delete=models.CASCADE)
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
