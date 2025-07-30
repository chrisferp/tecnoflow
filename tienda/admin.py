from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'detalle', 'precio', 'stock', 'moneda')
    search_fields = ('codigo', 'detalle')
