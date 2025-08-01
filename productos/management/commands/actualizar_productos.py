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
        no_encontrados = 0
        errores = 0

        with open(archivo_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            self.stdout.write(self.style.NOTICE(f"Encabezados detectados: {reader.fieldnames}"))

            for fila in reader:
                try:
                    codigo = fila.get('CODIGO', '').strip()
                    if not codigo:
                        continue  # ignorar filas sin código

                    producto = Producto.objects.filter(codigo=codigo).first()
                    if not producto:
                        no_encontrados += 1
                        continue

                    # Convertir valores numéricos
                    def num(v):
                        try:
                            return float(v)
                        except:
                            return 0

                    precio = num(fila.get('PRECIO', 0))
                    precio_final = num(fila.get('PRECIO FINAL', 0))
                    precio_utilidad = num(fila.get('PRECIO USD CON UTILIDAD', 0))
                    stock = int(num(fila.get('STOCK', 0)))

                    # Verificar cambios
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
