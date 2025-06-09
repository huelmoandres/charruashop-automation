import requests
import csv
import os
from datetime import datetime

# Importar configuración desde archivo seguro
try:
    from config.secrets import SHOPIFY_CONFIG
    API_VERSION = SHOPIFY_CONFIG["API_VERSION"]
    SHOP = SHOPIFY_CONFIG["SHOP"]
    TOKEN = SHOPIFY_CONFIG["TOKEN"]
except ImportError:
    print("❌ Error: No se pudo importar config/secrets.py")
    print("💡 Copia config/secrets.py.template como config/secrets.py y configura tus credenciales")
    exit(1)

HEADERS = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": TOKEN
}

# Archivo CSV con números de orden cortos
ORDERS_CSV_FILE = "orders_export.csv"  # El usuario proporcionará este archivo

# Carpeta donde se guardarán los CSVs
OUTPUT_DIR = "src/orders/output"

# FUNCIONES

def ensure_output_directory():
    """Crea la carpeta de salida si no existe"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"📁 Carpeta creada: {OUTPUT_DIR}")

def get_order(order_id):
    """Obtiene información completa de un pedido"""
    url = f"https://{SHOP}.myshopify.com/admin/api/{API_VERSION}/orders/{order_id}.json"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()["order"]

def get_product_metafields(product_id):
    """Obtiene los metafields de un producto"""
    url = f"https://{SHOP}.myshopify.com/admin/api/{API_VERSION}/products/{product_id}/metafields.json"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()["metafields"]

def extract_fda_id(metafields):
    """Extrae el FDA ID de los metafields"""
    for mf in metafields:
        if mf["namespace"] == "custom" and mf["key"] == "fda_id":
            return mf["value"]
    return ""

def extract_simplified_product_data(order, item):
    """Extrae solo los campos específicos requeridos"""
    # Información de shipping
    shipping_address = order.get("shipping_address", {})
    
    # Datos básicos del producto
    product_data = {
        "order_number": order.get("order_number", ""),
        "line_item_quantity": item.get("quantity", ""),
        "line_item_name": item.get("title", ""),
        "line_item_weight": item.get("grams", ""),  # Peso en gramos
        "guia_aerea": "01",  # Valor por defecto para completar manualmente
        "shipping_name": f"{shipping_address.get('first_name', '')} {shipping_address.get('last_name', '')}".strip(),
        "shipping_address_1": shipping_address.get("address1", ""),
        "shipping_address_2": shipping_address.get("address2", ""),
        "shipping_city": shipping_address.get("city", ""),
        "shipping_zip": shipping_address.get("zip", ""),
        "shipping_province": shipping_address.get("province", ""),
        "shipping_country": shipping_address.get("country", ""),
    }
    
    # Obtener FDA ID si el producto existe
    product_id = item.get("product_id")
    if product_id:
        try:
            metafields = get_product_metafields(product_id)
            fda_id = extract_fda_id(metafields)
            product_data["fda_id"] = fda_id
        except Exception as e:
            print(f"⚠️ Error obteniendo metafields para producto {product_id}: {e}")
            product_data["fda_id"] = ""
    else:
        product_data["fda_id"] = ""
    
    return product_data

def generate_order_csv(order_id):
    """Genera un CSV simplificado para un pedido específico"""
    try:
        print(f"📦 Procesando pedido: {order_id}")
        
        # Obtener información del pedido
        order = get_order(order_id)
        
        # Preparar datos de productos
        products_data = []
        
        for item in order["line_items"]:
            product_data = extract_simplified_product_data(order, item)
            products_data.append(product_data)
        
        # Generar nombre del archivo
        order_number = order.get("order_number", order_id)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"order_{order_number}_{timestamp}.csv"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Escribir CSV con campos específicos
        if products_data:
            # Campos en el orden específico requerido
            fieldnames = [
                "order_number",
                "line_item_quantity", 
                "line_item_name",
                "line_item_weight",
                "guia_aerea",
                "shipping_name",
                "shipping_address_1",
                "shipping_address_2", 
                "shipping_city",
                "shipping_zip",
                "shipping_province",
                "shipping_country",
                "fda_id"
            ]
            
            with open(filepath, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(products_data)
            
            print(f"✅ CSV generado: {filepath}")
            print(f"   📊 {len(products_data)} productos exportados")
            
            # Mostrar preview de los datos
            print(f"   📋 Preview de campos:")
            for field in fieldnames:
                sample_value = products_data[0].get(field, "")
                print(f"      • {field}: {sample_value}")
            
            return filepath
        else:
            print(f"⚠️ No se encontraron productos en el pedido {order_id}")
            return None
            
    except Exception as e:
        print(f"❌ Error procesando pedido {order_id}: {e}")
        return None

def export_all_orders(csv_file=ORDERS_CSV_FILE):
    """Exporta todos los pedidos desde archivo CSV con campos simplificados"""
    print("🚀 Iniciando exportación de pedidos (campos simplificados)")
    print("="*50)
    print("📋 Campos incluidos:")
    print("   • order_number")
    print("   • line_item_quantity") 
    print("   • line_item_name")
    print("   • line_item_weight")
    print("   • guia_aerea")
    print("   • shipping_name")
    print("   • shipping_address_1")
    print("   • shipping_address_2")
    print("   • shipping_city") 
    print("   • shipping_zip")
    print("   • shipping_province")
    print("   • shipping_country")
    print("   • fda_id")
    print("-"*50)
    
    # Leer y exportar desde CSV
    return export_orders_from_csv(csv_file)

def export_single_order(order_id):
    """Exporta un solo pedido a CSV simplificado"""
    ensure_output_directory()
    return generate_order_csv(order_id)

def export_orders_with_fda():
    """Función original - mantener compatibilidad"""
    print("⚠️ Función deprecated. Usa export_all_orders() para CSVs separados")
    return export_all_orders()

def get_order_id_from_number(order_number):
    """
    Convierte un número de orden corto (#1001) al ID largo de Shopify
    Args:
        order_number: Número de orden corto (ej: "1001" o "#1001")
    Returns:
        ID largo del pedido o None si no se encuentra
    """
    # Limpiar el número de orden (quitar # si existe)
    clean_number = str(order_number).replace("#", "").strip()
    
    try:
        # Buscar pedidos por nombre (Shopify usa formato #1001, #1002, etc.)
        url = f"https://{SHOP}.myshopify.com/admin/api/{API_VERSION}/orders.json"
        params = {
            "name": f"#{clean_number}",  # Shopify busca por nombre exacto
            "status": "any",
            "limit": 1
        }
        
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        
        orders = response.json()["orders"]
        
        if orders:
            order_id = orders[0]["id"]
            print(f"✅ Orden #{clean_number} encontrada → ID: {order_id}")
            return order_id
        else:
            print(f"❌ Orden #{clean_number} no encontrada")
            return None
            
    except Exception as e:
        print(f"❌ Error buscando orden #{clean_number}: {e}")
        return None

def get_multiple_order_ids(order_numbers):
    """
    Convierte múltiples números de orden cortos a IDs largos
    Args:
        order_numbers: Lista de números de orden cortos
    Returns:
        Diccionario {numero_corto: id_largo} para órdenes encontradas
    """
    print(f"🔍 Buscando IDs para {len(order_numbers)} órdenes...")
    
    order_mapping = {}
    
    for order_number in order_numbers:
        order_id = get_order_id_from_number(order_number)
        if order_id:
            order_mapping[order_number] = order_id
    
    print(f"✅ Se encontraron {len(order_mapping)} de {len(order_numbers)} órdenes")
    
    return order_mapping

def export_orders_by_short_numbers(short_numbers):
    """
    Exporta órdenes usando sus números cortos (#1001, #1002, etc.)
    Args:
        short_numbers: Lista de números cortos de órdenes
    Returns:
        Lista de archivos CSV generados
    """
    print("🚀 EXPORTACIÓN POR NÚMEROS DE ORDEN CORTOS")
    print("="*50)
    
    ensure_output_directory()
    
    # Convertir números cortos a IDs largos
    order_mapping = get_multiple_order_ids(short_numbers)
    
    if not order_mapping:
        print("❌ No se encontraron órdenes válidas")
        return []
    
    # Exportar cada orden encontrada
    generated_files = []
    
    for short_number, order_id in order_mapping.items():
        print(f"\n📦 Exportando orden #{short_number} (ID: {order_id})...")
        
        csv_file = generate_order_csv(order_id)
        if csv_file:
            generated_files.append(csv_file)
    
    # Resumen final
    print(f"\n🎉 EXPORTACIÓN COMPLETADA")
    print(f"   📊 {len(generated_files)} archivos CSV generados")
    print(f"   📁 Ubicación: {OUTPUT_DIR}")
    
    return generated_files

def read_short_order_numbers_from_csv(csv_file=ORDERS_CSV_FILE):
    """
    Lee números de orden cortos desde un archivo CSV
    Busca en las columnas: order_number, Name, order_name
    """
    if not os.path.exists(csv_file):
        print(f"❌ Archivo no encontrado: {csv_file}")
        print("💡 Asegúrate de tener el archivo orders_export.csv en la carpeta raíz")
        return []
    
    print(f"📖 Leyendo órdenes desde: {csv_file}")
    
    order_numbers = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            # Detectar el delimitador automáticamente
            sample = file.read(1024)
            file.seek(0)
            
            # Intentar detectar el delimitador
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
            
            reader = csv.DictReader(file, delimiter=delimiter)
            
            # Mostrar headers disponibles para debug
            headers = reader.fieldnames
            print(f"📋 Headers encontrados: {headers}")
            
            # Buscar la columna correcta de números de orden
            order_column = None
            possible_columns = ['order_number', 'Name', 'order_name', 'Order', 'Pedido']
            
            for col in possible_columns:
                if col in headers:
                    order_column = col
                    break
            
            if not order_column:
                print("❌ No se encontró columna de números de orden")
                print(f"   Columnas disponibles: {headers}")
                print(f"   Columnas esperadas: {possible_columns}")
                return []
            
            print(f"✅ Usando columna: '{order_column}'")
            
            # Leer números de orden
            for row in reader:
                order_number = row.get(order_column, '').strip()
                if order_number and order_number != '':
                    # Limpiar el número (quitar #, espacios, etc.)
                    clean_number = order_number.replace('#', '').strip()
                    if clean_number.isdigit():
                        order_numbers.append(clean_number)
            
            print(f"📊 Se encontraron {len(order_numbers)} números de orden válidos")
            if order_numbers:
                print(f"   Ejemplos: {order_numbers[:5]}{'...' if len(order_numbers) > 5 else ''}")
            
            return order_numbers
            
    except Exception as e:
        print(f"❌ Error leyendo archivo CSV: {e}")
        return []

def export_orders_from_csv(csv_file=ORDERS_CSV_FILE):
    """
    Exporta órdenes leyendo números desde un archivo CSV
    """
    print("🚀 EXPORTACIÓN DESDE ARCHIVO CSV")
    print("="*50)
    
    # Leer números de orden del CSV
    order_numbers = read_short_order_numbers_from_csv(csv_file)
    
    if not order_numbers:
        print("❌ No se pudieron leer números de orden del CSV")
        return []
    
    # Exportar usando los números encontrados
    return export_orders_by_short_numbers(order_numbers)

# FUNCIONES PRINCIPALES PARA EL MENÚ

def main_menu():
    """Menú principal interactivo"""
    print("\n🚀 GENERADOR DE CSV PARA FDA")
    print("="*40)
    print("1. Exportar desde archivo CSV (orders_export.csv)")
    print("2. Exportar órdenes específicas por número")
    print("3. Exportar una sola orden")
    print("4. Salir")
    
    while True:
        try:
            choice = input("\n🔍 Selecciona una opción (1-4): ").strip()
            
            if choice == "1":
                files = export_all_orders()
                if files:
                    print(f"\n✅ {len(files)} archivos generados exitosamente")
                break
                
            elif choice == "2":
                numbers_input = input("📝 Ingresa números de orden (separados por coma): ").strip()
                if numbers_input:
                    order_numbers = [n.strip() for n in numbers_input.split(',')]
                    files = export_orders_by_short_numbers(order_numbers)
                    if files:
                        print(f"\n✅ {len(files)} archivos generados exitosamente")
                break
                
            elif choice == "3":
                order_id = input("📝 Ingresa el ID largo del pedido: ").strip()
                if order_id:
                    file = export_single_order(order_id)
                    if file:
                        print(f"\n✅ Archivo generado: {file}")
                break
                
            elif choice == "4":
                print("👋 ¡Hasta luego!")
                break
                
            else:
                print("❌ Opción inválida. Por favor selecciona 1-4.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Proceso cancelado por el usuario")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main_menu() 