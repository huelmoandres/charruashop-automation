import os
import sys
import pandas as pd
import requests

# Cargar configuración de Shopify desde config/secrets.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
try:
    from config.secrets import SHOPIFY_CONFIG
except ImportError:
    print("No se pudo importar SHOPIFY_CONFIG. Verifica config/secrets.py")
    sys.exit(1)

SHOP = SHOPIFY_CONFIG["SHOP"]
TOKEN = SHOPIFY_CONFIG["TOKEN"]
API_VERSION = SHOPIFY_CONFIG.get("API_VERSION", "2023-07")

# Leer el Excel de mapeo
input_path = os.path.join("data/shopify", "shopify_productos_para_mapeo_fda.xlsx")
if not os.path.exists(input_path):
    print(f"No se encontró el archivo {input_path}. Ejecuta primero el exportador y completa los datos.")
    sys.exit(1)

df = pd.read_excel(input_path)

# Subir metafields a Shopify
headers = {"X-Shopify-Access-Token": TOKEN}
count = 0
for idx, row in df.iterrows():
    variant_id = row["variant_id"]
    fda_code = str(row["FDA_Code"]).strip()
    fabricante_code = str(row["Codigo_fabricante"]).strip()
    metafields = []
    if fda_code and fda_code.lower() != 'nan':
        metafields.append({
            "namespace": "custom",
            "key": "fda_code",
            "value": fda_code,
            "type": "single_line_text_field"
        })
    if fabricante_code and fabricante_code.lower() != 'nan':
        metafields.append({
            "namespace": "custom",
            "key": "fda_manufacturer_code",
            "value": fabricante_code,
            "type": "single_line_text_field"
        })
    for metafield in metafields:
        url = f"https://{SHOP}.myshopify.com/admin/api/{API_VERSION}/variants/{variant_id}/metafields.json"
        data = {"metafield": metafield}
        resp = requests.post(url, headers=headers, json=data)
        if resp.status_code in (200, 201):
            print(f"✅ Metafield {metafield['key']} actualizado para variante {variant_id}")
            count += 1
        else:
            print(f"❌ Error actualizando metafield {metafield['key']} para variante {variant_id}: {resp.status_code} {resp.text}")
print(f"Proceso finalizado. Metafields creados/actualizados: {count}") 