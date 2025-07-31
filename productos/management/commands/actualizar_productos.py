from django.core.management.base import BaseCommand
import csv
from productos.models import Producto




class Command(BaseCommand):
    help = 'Actualiza precios y stock de productos desde un archivo CSV'

    def add_arguments(self, parser):
        parser.add_argument('archivo_csv', type=str, help='Ruta del archivo CSV a procesar')

    def handle(self, *args, **kwargs):
        archivo_csv = kwargs['archivo_csv']
        actualizados = 0
        nuevos = 0
        no_encontrados = 0

        with open(archivo_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for fila in reader:
                codigo = fila.get('CODIGO', '').strip()

                try:
                    producto = Producto.objects.get(codigo=codigo)

                    # Verificamos si cambió algo
                    precio = float(fila.get('PRECIO', 0) or 0)
                    precio_final = float(fila.get('PRECIO FINAL', 0) or 0)
                    precio_utilidad = float(fila.get('PRECIO CON UTILIDAD (USD)', 0) or 0)
                    stock = int(fila.get('STOCK', 0) or 0)

                    cambios = False
                    if producto.precio != precio:
                        producto.precio = precio
                        cambios = True
                    if producto.precio_final != precio_final:
                        producto.precio_final = precio_final
                        cambios = True
                    if producto.precio_utilidad != precio_utilidad:
                        producto.precio_utilidad = precio_utilidad
                        cambios = True
                    if producto.stock != stock:
                        producto.stock = stock
                        cambios = True

                    if cambios:
                        producto.save()
                        actualizados += 1

                except Producto.DoesNotExist:
                    no_encontrados += 1
                    # Opcional: crear el producto si no existe
                    # Producto.objects.create(codigo=codigo, ...)
                    # nuevos += 1

        self.stdout.write(self.style.SUCCESS(
            f'Actualización completada: {actualizados} productos modificados, {no_encontrados} no encontrados.'
        ))
