from django.core.management.base import BaseCommand
import csv
import os
from datetime import datetime
from productos.models import Producto

class Command(BaseCommand):
    help = 'Importa productos desde un archivo CSV al modelo Producto'

    def add_arguments(self, parser):
        parser.add_argument('archivo_csv', type=str, help='Ruta del archivo CSV a importar')

    def handle(self, *args, **kwargs):
        archivo_csv = kwargs['archivo_csv']

        # Crear carpeta de logs si no existe
        os.makedirs("logs", exist_ok=True)
        log_file = f"logs/import_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

        with open(log_file, 'w', encoding='utf-8') as log:
            log.write(f"📦 Importación de productos - {datetime.now()}\n")
            log.write("="*60 + "\n\n")

            creados = 0
            actualizados = 0
            sin_cambios = 0
            errores = 0

            with open(archivo_csv, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                self.stdout.write(self.style.NOTICE(f"Encabezados detectados: {reader.fieldnames}"))

                for fila in reader:
                    try:
                        codigo = fila.get('CODIGO', '').strip()
                        if not codigo:
                            errores += 1
                            log.write(f"[IGNORADO] Fila sin código -> {fila}\n")
                            continue

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
                                'peso': peso,
                                'alto': alto,
                                'ancho': ancho,
                                'largo': largo,
                                'impuesto_interno': impuesto_interno,
                            }
                        )

                        if creado:
                            creados += 1
                            log.write(f"[CREADO] {codigo}\n")
                        else:
                            # Detectar cambios
                            cambios = []
                            for campo, valor in producto.__dict__.items():
                                if campo in fila and str(valor).strip() != str(fila[campo]).strip():
                                    cambios.append(campo)

                            if cambios:
                                actualizados += 1
                                log.write(f"[ACTUALIZADO] {codigo} -> {cambios}\n")
                            else:
                                sin_cambios += 1
                                log.write(f"[SIN CAMBIOS] {codigo}\n")

                    except Exception as e:
                        errores += 1
                        log.write(f"[ERROR] Fila {fila} -> {e}\n")

            # Resumen final
            log.write("\n" + "="*60 + "\n")
            log.write(f"✅ Productos creados: {creados}\n")
            log.write(f"🔄 Productos actualizados: {actualizados}\n")
            log.write(f"⚪ Filas sin cambios: {sin_cambios}\n")
            log.write(f"❌ Filas con errores: {errores}\n")

        self.stdout.write(self.style.SUCCESS('✅ Importación completada'))
        self.stdout.write(self.style.SUCCESS(f'   ➜ Productos creados: {creados}'))
        self.stdout.write(self.style.SUCCESS(f'   ➜ Productos actualizados: {actualizados}'))
        self.stdout.write(self.style.WARNING(f'   ➜ Filas sin cambios: {sin_cambios}'))
        self.stdout.write(self.style.ERROR(f'   ➜ Filas con errores: {errores}'))
        self.stdout.write(self.style.NOTICE(f'📄 Log guardado en: {log_file}'))
