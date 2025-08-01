import os
import time
import django
import schedule
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tecnoflow.settings")
django.setup()

from django.core.management import call_command

# URL del CSV (ejemplo)
CSV_URL = "https://api.nb.com.ar/v1/priceListCsv/e7fb3a2be525b29436592d190abe6b"
CSV_LOCAL_PATH = "NB-Lista-Precios.csv"

def descargar_csv():
    print("⬇️ Descargando archivo CSV...")
    response = requests.get(CSV_URL)
    if response.status_code == 200:
        with open(CSV_LOCAL_PATH, "wb") as f:
            f.write(response.content)
        print("✅ Archivo CSV descargado correctamente")
        return True
    else:
        print(f"❌ Error al descargar archivo ({response.status_code})")
        return False

def actualizar_productos():
    if descargar_csv():
        print("🔄 Ejecutando actualización de productos...")
        call_command("actualizar_productos", CSV_LOCAL_PATH)
        print("✅ Actualización completada.")

# Ejecutar cada 10 minutos
schedule.every(5).minutes.do(actualizar_productos)

print("✅ Script de actualización automática iniciado (Ctrl + C para detener)")
while True:
    schedule.run_pending()
    time.sleep(1)
