from django.core.management.base import BaseCommand
import csv
import os
import codecs
from productos.models import Producto

class Command(BaseCommand):
    help = 'Actualiza precios y stock de productos desde un archivo CSV (versión estable)'

    def add_arguments(self, parser):
        parser.add_argument('archivo_csv', type=str, help='Ruta del archivo CSV a procesar')

    def handle(self, *args, **kwargs):
        archivo_csv = kwargs['archivo_csv']
        actualizados = 0
        no_encontrados = 0
        errores = 0

        # ✅ Leer el CSV eliminando BOM y comillas solo en encabezados
        with codecs.open(archivo_csv, 'r', encoding='utf-8-sig', errors='ignore') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            reader.fieldnames = [h.strip().replace('"', '') for h in reader.fieldnames]
            self.stdout.write(self.style.NOTICE(f"Encabezados detectados: {reader.fieldnames}"))

            for fila in reader:
                try:
                    # Limpiar claves vacías
                    fila = {k.strip(): (v.strip() if v else '') for k, v in fila.items() if k and k.strip()}

                    codigo = fila.get('CODIGO', '').strip()
                    if not codigo:
                        continue  # ignorar filas sin código

                    producto = Producto.objects.filter(codigo=codigo).first()
                    if not producto:
                        no_encontrados += 1
                        continue

                    # Función segura para números
                    def num(v):
                        try:
                            return float(v.replace(',', '.')) if v else 0
                        except:
                            return 0

                    precio = num(fila.get('PRECIO'))
                    precio_final = num(fila.get('PRECIO FINAL'))
                    precio_utilidad = num(fila.get('PRECIO USD CON UTILIDAD'))
                    stock = int(num(fila.get('STOCK')))

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

                except Exception as e:
                    errores += 1
                    self.stdout.write(self.style.ERROR(f"Error en fila con código {codigo}: {e}"))

        self.stdout.write(self.style.SUCCESS(f'✅ Actualización completada'))
        self.stdout.write(self.style.SUCCESS(f'   ➜ Productos actualizados: {actualizados}'))
        self.stdout.write(self.style.WARNING(f'   ➜ No encontrados: {no_encontrados}'))
        self.stdout.write(self.style.ERROR(f'   ➜ Filas con errores: {errores}'))
