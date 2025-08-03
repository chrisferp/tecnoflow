import os
import time
import django
import schedule
import requests
from django.core.management import call_command
from datetime import datetime

# Colores para la consola
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tecnoflow.settings")
django.setup()

# URL del CSV
CSV_URL = "https://api.nb.com.ar/v1/priceListCsv/e7fb3a2be525b29436592d190abe6b"
CSV_LOCAL_PATH = "NB-Lista-Precios.csv"

def descargar_csv():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ⬇️  Descargando archivo CSV...")
    response = requests.get(CSV_URL)
    if response.status_code == 200:
        with open(CSV_LOCAL_PATH, "wb") as f:
            f.write(response.content)
        print(f"{GREEN}[{datetime.now().strftime('%H:%M:%S')}] ✅ Archivo CSV descargado correctamente{RESET}")
        return True
    else:
        print(f"{RED}[{datetime.now().strftime('%H:%M:%S')}] ❌ Error al descargar archivo ({response.status_code}){RESET}")
        return False

def actualizar_productos():
    if descargar_csv():
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔄 Ejecutando actualización de productos...")

        # Capturar la salida del comando y mostrar solo el resumen
        from io import StringIO
        import sys

        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        call_command("actualizar_productos", CSV_LOCAL_PATH)

        sys.stdout = old_stdout
        output = mystdout.getvalue()

        # Filtrar el resumen
        for line in output.splitlines():
            if "Productos actualizados:" in line:
                print(f"{GREEN}[{datetime.now().strftime('%H:%M:%S')}] {line}{RESET}")
            elif "No encontrados:" in line:
                print(f"{YELLOW}[{datetime.now().strftime('%H:%M:%S')}] {line}{RESET}")
            elif "Filas con errores:" in line:
                color = RED if not line.endswith("0") else GREEN
                print(f"{color}[{datetime.now().strftime('%H:%M:%S')}] {line}{RESET}")

# Ejecutar cada 5 minutos
schedule.every(13).minutes.do(actualizar_productos)

print(f"{GREEN}✅ Script de actualización automática iniciado (Ctrl + C para detener){RESET}")
while True:
    schedule.run_pending()
    time.sleep(1)
