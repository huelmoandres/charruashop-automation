"""
Utilidades adicionales para manejo de CSVs de pedidos simplificados
"""

import csv
import os
import glob
from datetime import datetime
from collections import defaultdict

def list_generated_csvs(output_dir="src/orders/output"):
    """Lista todos los CSVs generados en la carpeta de salida"""
    if not os.path.exists(output_dir):
        print(f"❌ Carpeta no encontrada: {output_dir}")
        return []
    
    csv_files = glob.glob(os.path.join(output_dir, "*.csv"))
    csv_files.sort(key=os.path.getmtime, reverse=True)  # Más recientes primero
    
    print(f"📁 Archivos CSV encontrados en {output_dir}:")
    for i, filepath in enumerate(csv_files, 1):
        filename = os.path.basename(filepath)
        file_size = os.path.getsize(filepath)
        modified_time = datetime.fromtimestamp(os.path.getmtime(filepath))
        
        print(f"  {i:2d}. {filename}")
        print(f"      📊 Tamaño: {file_size:,} bytes")
        print(f"      🕐 Modificado: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    return csv_files

def analyze_csv_content(csv_file):
    """Analiza el contenido de un CSV específico (versión simplificada)"""
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
            if not rows:
                print(f"⚠️ El archivo {csv_file} está vacío")
                return None
            
            print(f"📋 Análisis de: {os.path.basename(csv_file)}")
            print("-" * 50)
            print(f"📊 Total de productos: {len(rows)}")
            
            # Información del pedido (primera fila)
            first_row = rows[0]
            print(f"📦 Order Number: {first_row.get('order_number')}")
            print(f"📍 Envío a: {first_row.get('shipping_name')}")
            print(f"🏠 Dirección: {first_row.get('shipping_address_1')}, {first_row.get('shipping_city')}")
            print(f"🌍 País: {first_row.get('shipping_country')}")
            
            # Análisis de productos
            products_with_fda = sum(1 for row in rows if row.get('fda_id'))
            products_without_fda = len(rows) - products_with_fda
            
            print(f"\n🧬 Productos con FDA ID: {products_with_fda}")
            print(f"⚠️ Productos sin FDA ID: {products_without_fda}")
            
            # Lista de productos con FDA ID
            if products_with_fda > 0:
                print(f"\n✅ Productos con FDA ID:")
                for row in rows:
                    if row.get('fda_id'):
                        quantity = row.get('line_item_quantity', '1')
                        name = row.get('line_item_name', 'Sin nombre')
                        weight = row.get('line_item_weight', '0')
                        fda_id = row.get('fda_id')
                        print(f"   • {quantity}x {name} ({weight}g) - FDA: {fda_id}")
            
            # Lista de productos sin FDA ID
            if products_without_fda > 0:
                print(f"\n❌ Productos sin FDA ID:")
                for row in rows:
                    if not row.get('fda_id'):
                        quantity = row.get('line_item_quantity', '1')
                        name = row.get('line_item_name', 'Sin nombre')
                        weight = row.get('line_item_weight', '0')
                        print(f"   • {quantity}x {name} ({weight}g)")
            
            return {
                'total_products': len(rows),
                'products_with_fda': products_with_fda,
                'products_without_fda': products_without_fda,
                'order_info': {
                    'number': first_row.get('order_number'),
                    'shipping_name': first_row.get('shipping_name'),
                    'shipping_country': first_row.get('shipping_country')
                }
            }
            
    except Exception as e:
        print(f"❌ Error analizando {csv_file}: {e}")
        return None

def filter_products_by_fda_status(csv_file, has_fda=True, output_suffix="_filtered"):
    """Filtra productos según si tienen FDA ID o no"""
    try:
        base_name = os.path.splitext(csv_file)[0]
        suffix = "_with_fda" if has_fda else "_without_fda"
        output_file = f"{base_name}{output_suffix}{suffix}.csv"
        
        with open(csv_file, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            filtered_rows = []
            
            for row in reader:
                fda_id = row.get('fda_id', '').strip()
                if has_fda and fda_id:  # Productos CON FDA ID
                    filtered_rows.append(row)
                elif not has_fda and not fda_id:  # Productos SIN FDA ID
                    filtered_rows.append(row)
        
        if filtered_rows:
            fieldnames = filtered_rows[0].keys()
            with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(filtered_rows)
            
            status_text = "CON" if has_fda else "SIN"
            print(f"✅ Archivo filtrado creado: {output_file}")
            print(f"📊 Productos {status_text} FDA ID: {len(filtered_rows)}")
            return output_file
        else:
            status_text = "con" if has_fda else "sin"
            print(f"⚠️ No se encontraron productos {status_text} FDA ID")
            return None
            
    except Exception as e:
        print(f"❌ Error filtrando {csv_file}: {e}")
        return None

def generate_summary_report(output_dir="src/orders/output"):
    """Genera un reporte resumen de todos los CSVs simplificados"""
    csv_files = glob.glob(os.path.join(output_dir, "order_*.csv"))
    
    if not csv_files:
        print(f"❌ No se encontraron archivos CSV en {output_dir}")
        return
    
    summary_data = []
    total_products = 0
    total_with_fda = 0
    total_without_fda = 0
    
    print("📊 Generando reporte resumen...")
    print("=" * 60)
    
    for csv_file in csv_files:
        analysis = analyze_csv_content(csv_file)
        if analysis:
            summary_data.append({
                'file': os.path.basename(csv_file),
                'order_number': analysis['order_info']['number'],
                'shipping_name': analysis['order_info']['shipping_name'],
                'shipping_country': analysis['order_info']['shipping_country'],
                'total_products': analysis['total_products'],
                'products_with_fda': analysis['products_with_fda'],
                'products_without_fda': analysis['products_without_fda'],
                'fda_percentage': f"{(analysis['products_with_fda']/analysis['total_products']*100):.1f}%" if analysis['total_products'] > 0 else "0%"
            })
            
            total_products += analysis['total_products']
            total_with_fda += analysis['products_with_fda']
            total_without_fda += analysis['products_without_fda']
        
        print("-" * 60)
    
    # Guardar reporte resumen
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_file = os.path.join(output_dir, f"summary_report_{timestamp}.csv")
    
    if summary_data:
        fieldnames = summary_data[0].keys()
        with open(summary_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(summary_data)
    
    print("\n🎉 REPORTE RESUMEN FINAL")
    print("=" * 60)
    print(f"📁 Total de pedidos procesados: {len(summary_data)}")
    print(f"📦 Total de productos: {total_products}")
    print(f"✅ Productos con FDA ID: {total_with_fda}")
    print(f"❌ Productos sin FDA ID: {total_without_fda}")
    print(f"📊 Porcentaje con FDA: {(total_with_fda/total_products*100):.1f}%" if total_products > 0 else "N/A")
    print(f"📄 Reporte guardado en: {summary_file}")
    
    return summary_file

def validate_csv_structure(csv_file):
    """Valida que el CSV tenga la estructura esperada de campos simplificados"""
    expected_fields = [
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
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            actual_fields = reader.fieldnames
            
            print(f"🔍 Validando estructura de: {os.path.basename(csv_file)}")
            print("-" * 50)
            
            missing_fields = set(expected_fields) - set(actual_fields)
            extra_fields = set(actual_fields) - set(expected_fields)
            
            if not missing_fields and not extra_fields:
                print("✅ Estructura correcta - todos los campos esperados presentes")
                return True
            else:
                if missing_fields:
                    print(f"❌ Campos faltantes: {', '.join(missing_fields)}")
                if extra_fields:
                    print(f"⚠️ Campos adicionales: {', '.join(extra_fields)}")
                return False
                
    except Exception as e:
        print(f"❌ Error validando {csv_file}: {e}")
        return False

def show_sample_data(csv_file, num_rows=3):
    """Muestra una muestra de los datos del CSV"""
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
            if not rows:
                print(f"⚠️ El archivo {csv_file} está vacío")
                return
            
            print(f"📋 Muestra de datos de: {os.path.basename(csv_file)}")
            print("-" * 80)
            
            for i, row in enumerate(rows[:num_rows], 1):
                print(f"📦 Producto {i}:")
                print(f"   • Pedido: {row.get('order_number')}")
                print(f"   • Cantidad: {row.get('line_item_quantity')}")
                print(f"   • Producto: {row.get('line_item_name')}")
                print(f"   • Peso: {row.get('line_item_weight')} gramos")
                print(f"   • Guía Aérea: {row.get('guia_aerea')}")
                print(f"   • Cliente: {row.get('shipping_name')}")
                print(f"   • País: {row.get('shipping_country')}")
                print(f"   • FDA ID: {row.get('fda_id') or 'No asignado'}")
                print()
                
    except Exception as e:
        print(f"❌ Error mostrando muestra de {csv_file}: {e}")

# Funciones de conveniencia
def show_latest_csvs(count=5):
    """Muestra los últimos CSVs generados"""
    csv_files = list_generated_csvs()
    if csv_files:
        print(f"\n📋 Últimos {min(count, len(csv_files))} CSVs:")
        for i, csv_file in enumerate(csv_files[:count], 1):
            print(f"  {i}. {os.path.basename(csv_file)}")

def quick_analyze_latest():
    """Analiza rápidamente el CSV más reciente"""
    csv_files = list_generated_csvs()
    if csv_files:
        print(f"\n🔍 Análisis rápido del archivo más reciente:")
        analyze_csv_content(csv_files[0])
        print(f"\n📊 Muestra de datos:")
        show_sample_data(csv_files[0], 2)
    else:
        print("❌ No se encontraron archivos CSV")

if __name__ == "__main__":
    # Ejemplos de uso
    print("🔧 Utilidades CSV para pedidos simplificados")
    print("=" * 50)
    
    # Listar archivos
    list_generated_csvs()
    
    # Análisis rápido
    quick_analyze_latest()
    
    # Generar reporte resumen
    generate_summary_report() 