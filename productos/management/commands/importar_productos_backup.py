from django.core.management.base import BaseCommand
import csv
from productos.models import Producto

class Command(BaseCommand):
    help = 'Importa productos desde un archivo CSV al modelo Producto'

    def add_arguments(self, parser):
        parser.add_argument('archivo_csv', type=str, help='Ruta del archivo CSV a importar')

    def handle(self, *args, **kwargs):
        archivo_csv = kwargs['archivo_csv']

        # Contadores para el reporte final
        creados = 0
        actualizados = 0
        errores = 0

        # Abrimos el archivo CSV
        with open(archivo_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            self.stdout.write(self.style.NOTICE(f"Encabezados detectados: {reader.fieldnames}"))

            for fila in reader:
                try:
                    # Validar que el producto tenga código
                    codigo = fila.get('CODIGO', '').strip()
                    if not codigo:
                        errores += 1
                        self.stdout.write(self.style.WARNING("Fila ignorada: sin código"))
                        continue

                    # Validar y convertir campos numéricos
                    def num(valor):
                        try:
                            return float(valor)
                        except:
                            return 0

                    stock = int(num(fila.get('STOCK', 0)))
                    precio = num(fila.get('PRECIO', 0))
                    precio_final = num(fila.get('PRECIO FINAL', 0))
                    precio_utilidad = num(fila.get('PRECIO USD CON UTILIDAD', 0))
                    peso = num(fila.get('PESO', 0))
                    alto = num(fila.get('ALTO', 0))
                    ancho = num(fila.get('ANCHO', 0))
                    largo = num(fila.get('LARGO', 0))
                    impuesto_interno = num(fila.get('IMPUESTO_INTERNO', 0))

                    # Crear o actualizar producto
                    producto, creado = Producto.objects.update_or_create(
                        codigo=codigo,
                        defaults={
                            'id_fabricante': fila.get('ID FABRICANTE', '').strip() or None,
                            'detalle': fila.get('DETALLE', '').strip(),
                            'iva': fila.get('IVA', '').strip() or None,
                            'stock': stock,
                            'garantia': fila.get('GARANTIA', '').strip() or None,
                            'moneda': fila.get('MONEDA', '').strip() or 'USD',
                            'precio': precio,
                            'precio_final': precio_final,
                            'precio_utilidad': precio_utilidad,
                            'imagen': fila.get('IMAGEN', '').strip() or None,
                            'detalle_usuario': fila.get('DETALLE_USUARIO', '').strip() or None,
                            'ean': fila.get('EAN', '').strip() or None,
                            'upc': fila.get('UPC', '').strip() or None,
                            'peso': peso,
                            'alto': alto,
                            'ancho': ancho,
                            'largo': largo,
                            'impuesto_interno': impuesto_interno,
                            'galeria': fila.get('GALERIA', '').strip() or None,
                        }
                    )

                    if creado:
                        creados += 1
                    else:
                        actualizados += 1

                except Exception as e:
                    errores += 1
                    self.stdout.write(self.style.ERROR(f"Error en fila {fila}: {e}"))

        # Mostrar el resultado final
        self.stdout.write(self.style.SUCCESS(f'✅ Importación completada'))
        self.stdout.write(self.style.SUCCESS(f'   ➜ Productos creados: {creados}'))
        self.stdout.write(self.style.SUCCESS(f'   ➜ Productos actualizados: {actualizados}'))
        self.stdout.write(self.style.WARNING(f'   ➜ Filas con errores: {errores}'))
