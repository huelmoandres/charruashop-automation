import sys
import os
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

# Descargar todos los productos y variantes de Shopify
products = []
page_info = None
base_url = f"https://{SHOP}.myshopify.com/admin/api/{API_VERSION}/products.json"
headers = {"X-Shopify-Access-Token": TOKEN}

print("Descargando productos de Shopify...")
while True:
    params = {"limit": 250}
    if page_info:
        params["page_info"] = page_info
    resp = requests.get(base_url, headers=headers, params=params)
    if resp.status_code != 200:
        print(f"Error al obtener productos: {resp.status_code} {resp.text}")
        sys.exit(1)
    data = resp.json()
    products.extend(data["products"])
    # Manejo de paginación
    link = resp.headers.get('Link')
    if link and 'rel="next"' in link:
        import re
        match = re.search(r'<([^>]+)>; rel="next"', link)
        if match:
            from urllib.parse import urlparse, parse_qs
            next_url = match.group(1)
            page_info = parse_qs(urlparse(next_url).query)["page_info"][0]
            continue
    break

print(f"Productos descargados: {len(products)}")

# Preparar datos para exportar
rows = []
for product in products:
    product_id = product["id"]
    title = product["title"]
    for variant in product["variants"]:
        variant_id = variant["id"]
        sku = variant["sku"]
        rows.append({
            "product_id": product_id,
            "variant_id": variant_id,
            "sku": sku,
            "title": title,
            "fda_code": "",
            "fabricante_code": ""
        })

# Exportar a Excel
df = pd.DataFrame(rows)
output_path = os.path.join("data/shopify", "shopify_productos_para_mapeo_fda.xlsx")
df.to_excel(output_path, index=False)
print(f"Archivo de mapeo exportado: {output_path}")
print("Completa las columnas FDA_Code y Codigo_fabricante manualmente y luego podrás automatizar la carga de metafields.") 