from django.core.management.base import BaseCommand
import csv
from productos.models import Producto

class Command(BaseCommand):
    help = 'Importa productos desde un archivo CSV al modelo Producto'

    def add_arguments(self, parser):
        parser.add_argument('archivo_csv', type=str, help='Ruta del archivo CSV a importar')

    def handle(self, *args, **kwargs):
        archivo_csv = kwargs['archivo_csv']
        contador = 0
        errores = 0

        with open(archivo_csv, newline='', encoding='utf-8-sig') as csvfile:
            # Forzar delimitador en base al archivo NB
            reader = csv.DictReader(csvfile, delimiter=';')
            print("Encabezados detectados:", reader.fieldnames)  # DEBUG

            for fila in reader:
                codigo = (fila.get('CODIGO') or '').strip()

                if not codigo:
                    errores += 1
                    continue

                try:
                    producto, creado = Producto.objects.update_or_create(
                        codigo=codigo,
                        defaults={
                            'id_fabricante': (fila.get('ID FABRICANTE') or '').strip() or None,
                            'detalle': (fila.get('DETALLE') or '').strip(),
                            'iva': (fila.get('IVA') or '').strip() or None,
                            'stock': int(fila.get('STOCK') or 0),
                            'garantia': (fila.get('GARANTIA') or '').strip() or None,
                            'moneda': (fila.get('MONEDA') or '').strip() or 'USD',
                            'precio': float(fila.get('PRECIO') or 0),
                            'precio_final': float(fila.get('PRECIO FINAL') or 0),
                            'precio_utilidad': float(fila.get('PRECIO USD CON UTILIDAD') or 0),
                            'detalle_usuario': (fila.get('DETALLE_USUARIO') or '').strip() or None,
                            'peso': float(fila.get('PESO') or 0),
                            'alto': float(fila.get('ALTO') or 0),
                            'ancho': float(fila.get('ANCHO') or 0),
                            'largo': float(fila.get('LARGO') or 0),
                            'impuesto_interno': float(fila.get('IMPUESTO_INTERNO') or 0),
                        }
                    )
                    contador += 1
                except Exception as e:
                    errores += 1
                    print(f"⚠️ Error en la fila {fila.get('CODIGO')}: {e}")

        self.stdout.write(self.style.SUCCESS(f'✅ Importación completada: {contador} productos procesados, {errores} errores.'))
