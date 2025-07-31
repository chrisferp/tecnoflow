from django.db import models

class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    id_fabricante = models.CharField(max_length=50, blank=True, null=True)
    detalle = models.CharField(max_length=255)
    iva = models.CharField(max_length=10, blank=True, null=True)
    stock = models.IntegerField(default=0)
    garantia = models.CharField(max_length=50, blank=True, null=True)
    moneda = models.CharField(max_length=10, default="USD")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)
    precio_utilidad = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    imagen = models.URLField(max_length=500, blank=True, null=True)
    detalle_usuario = models.TextField(blank=True, null=True)
    ean = models.CharField(max_length=50, blank=True, null=True)
    upc = models.CharField(max_length=50, blank=True, null=True)
    peso = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    alto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ancho = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    largo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    impuesto_interno = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    galeria = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.codigo} - {self.detalle}"
# Create your models here.
