"""
Herramienta para actualizar la columna 'guia_aerea' en archivos CSV existentes
Busca archivos por número de pedido corto y permite modificar valores
"""

import csv
import os
import glob
import re
from datetime import datetime
from src.core.logger import AutomationLogger

# Inicializar logger
logger = AutomationLogger.get_instance()

# Configuración
OUTPUT_DIR = "src/orders/output"

def find_csv_files_by_order(order_number):
    """
    Busca archivos CSV en la carpeta output que correspondan a un número de pedido
    Los archivos tienen formato: order_1001_20231215_143022.csv
    """
    logger.shopify_logger.info("=== BUSCANDO ARCHIVOS CSV POR NÚMERO DE PEDIDO ===", extra={"order_number": order_number})
    
    # Limpiar el número de pedido (quitar # si existe)
    clean_number = str(order_number).replace("#", "").strip()
    
    if not os.path.exists(OUTPUT_DIR):
        logger.shopify_logger.error("Carpeta output no encontrada", extra={"directory": OUTPUT_DIR})
        return []
    
    # Buscar archivos que contengan el número de pedido en el nombre
    pattern = os.path.join(OUTPUT_DIR, f"order_{clean_number}_*.csv")
    matching_files = glob.glob(pattern)
    
    logger.shopify_logger.info("Ejecutando búsqueda de archivos", extra={
        "clean_number": clean_number,
        "search_pattern": f"order_{clean_number}_*.csv",
        "search_directory": OUTPUT_DIR
    })
    
    if matching_files:
        logger.shopify_logger.info("Archivos CSV encontrados", extra={
            "files_count": len(matching_files),
            "order_number": clean_number
        })
        
        for i, filepath in enumerate(matching_files, 1):
            filename = os.path.basename(filepath)
            file_size = os.path.getsize(filepath)
            modified_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            
            logger.shopify_logger.debug("Archivo encontrado", extra={
                "index": i,
                "filename": filename,
                "file_size_bytes": file_size,
                "modified_time": modified_time.strftime('%Y-%m-%d %H:%M:%S')
            })
            
            print(f"  {i}. {filename}")
            print(f"     📊 Tamaño: {file_size:,} bytes")
            print(f"     🕐 Modificado: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print()
    else:
        logger.shopify_logger.warning("No se encontraron archivos CSV", extra={
            "order_number": clean_number,
            "search_directory": OUTPUT_DIR
        })
        print(f"❌ No se encontraron archivos para el pedido #{clean_number}")
        print(f"💡 Asegúrate de que existen archivos CSV en {OUTPUT_DIR}")
    
    return matching_files

def analyze_csv_guia_aerea(csv_file):
    """
    Analiza el contenido actual de la columna guia_aerea en un CSV
    """
    logger.shopify_logger.info("=== ANALIZANDO CONTENIDO CSV ===", extra={"csv_file": csv_file})
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
            if not rows:
                logger.shopify_logger.warning("Archivo CSV está vacío", extra={"csv_file": csv_file})
                return None
            
            # Información del pedido
            first_row = rows[0]
            order_info = {
                "order_number": first_row.get('order_number'),
                "shipping_name": first_row.get('shipping_name'),
                "total_products": len(rows)
            }
            
            logger.shopify_logger.info("Información del pedido extraída", extra=order_info)
            
            # Análisis de valores actuales de guia_aerea
            guia_values = [row.get('guia_aerea', '') for row in rows]
            unique_values = list(set(guia_values))
            
            guia_analysis = {}
            for value in unique_values:
                count = guia_values.count(value)
                guia_analysis[value] = count
            
            logger.shopify_logger.info("Análisis de valores guía aérea", extra={
                "unique_values": guia_analysis,
                "total_products": len(rows)
            })
            
            # Log detallado de productos
            for i, row in enumerate(rows, 1):
                product_info = {
                    "index": i,
                    "name": row.get('line_item_name', 'Sin nombre')[:40],
                    "quantity": row.get('line_item_quantity', '1'),
                    "current_guia": row.get('guia_aerea', '')
                }
                logger.shopify_logger.debug("Producto analizado", extra=product_info)
                
                print(f"   {i:2d}. {product_info['quantity']}x {product_info['name']}... -> Guía: '{product_info['current_guia']}'")
            
            logger.shopify_logger.info("Análisis CSV completado exitosamente")
            return rows
            
    except Exception as e:
        logger.shopify_logger.error("Error analizando archivo CSV", extra={
            "csv_file": csv_file,
            "error": str(e)
        })
        logger.error_logger.error("CSV analysis failed", extra={
            "source_module": "orders_update_guia_aerea",
            "function": "analyze_csv_guia_aerea",
            "csv_file": csv_file,
            "error": str(e)
        })
        return None

def update_guia_aerea_in_csv(csv_file, new_guia_value, specific_products=None):
    """
    Actualiza la columna guia_aerea en un archivo CSV
    
    Args:
        csv_file: Ruta del archivo CSV
        new_guia_value: Nuevo valor para guia_aerea
        specific_products: Lista de índices de productos a actualizar (None = todos)
    """
    logger.shopify_logger.info("=== ACTUALIZANDO GUÍA AÉREA EN CSV ===", extra={
        "csv_file": csv_file,
        "new_guia_value": new_guia_value,
        "specific_products": specific_products
    })
    
    try:
        # Leer archivo original
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            fieldnames = reader.fieldnames
        
        if not rows:
            logger.shopify_logger.warning("Archivo CSV está vacío, no se puede actualizar")
            return False
        
        logger.shopify_logger.debug("Archivo CSV leído exitosamente", extra={
            "rows_count": len(rows),
            "fieldnames": list(fieldnames) if fieldnames else []
        })
        
        # Actualizar valores
        updated_count = 0
        
        if specific_products is None:
            # Actualizar todos los productos
            for row in rows:
                row['guia_aerea'] = new_guia_value
                updated_count += 1
            logger.shopify_logger.info("Actualizando todos los productos", extra={"updated_count": updated_count})
        else:
            # Actualizar solo productos específicos
            for index in specific_products:
                if 0 <= index < len(rows):
                    rows[index]['guia_aerea'] = new_guia_value
                    updated_count += 1
            logger.shopify_logger.info("Actualizando productos específicos", extra={
                "specific_products": specific_products,
                "updated_count": updated_count
            })
        
        # Escribir archivo actualizado
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        logger.shopify_logger.info("=== ACTUALIZACIÓN CSV COMPLETADA EXITOSAMENTE ===", extra={
            "csv_file": csv_file,
            "updated_count": updated_count,
            "new_guia_value": new_guia_value
        })
        
        print(f"✅ Archivo actualizado exitosamente")
        print(f"📊 {updated_count} producto(s) actualizados con guía aérea: '{new_guia_value}'")
        
        return True
        
    except Exception as e:
        logger.shopify_logger.error("Error actualizando archivo CSV", extra={
            "csv_file": csv_file,
            "new_guia_value": new_guia_value,
            "error": str(e)
        })
        logger.error_logger.error("CSV update failed", extra={
            "source_module": "orders_update_guia_aerea",
            "function": "update_guia_aerea_in_csv",
            "csv_file": csv_file,
            "error": str(e)
        })
        return False

def interactive_update():
    """
    Función interactiva principal para actualizar guía aérea
    """
    logger.shopify_logger.info("=== INICIANDO ACTUALIZADOR INTERACTIVO DE GUÍA AÉREA ===")
    
    print("🛠️ ACTUALIZADOR DE GUÍA AÉREA")
    print("=" * 50)
    
    while True:
        print("\n📝 Ingresa el número de pedido corto (o 'x' para salir)")
        order_input = input("Número de pedido: ").strip()
        
        if order_input.lower() in ['x', 'exit', 'quit', '']:
            logger.shopify_logger.info("Usuario salió del actualizador interactivo")
            print("👋 ¡Hasta luego!")
            break
        
        # Buscar archivos para este pedido
        matching_files = find_csv_files_by_order(order_input)
        
        if not matching_files:
            print("⚠️ No se encontraron archivos para este pedido")
            continue
        
        # Si hay múltiples archivos, permitir seleccionar
        if len(matching_files) > 1:
            print(f"\n📂 Se encontraron {len(matching_files)} archivos. ¿Cuál quieres actualizar?")
            for i, filepath in enumerate(matching_files, 1):
                print(f"  {i}. {os.path.basename(filepath)}")
            
            while True:
                try:
                    choice_input = input("Selecciona número de archivo (1-{}): ".format(len(matching_files))).strip()
                    
                    # Extraer solo el primer número de la entrada
                    import re
                    numbers = re.findall(r'\d+', choice_input)
                    
                    if numbers:
                        choice = int(numbers[0])
                        if 1 <= choice <= len(matching_files):
                            selected_file = matching_files[choice - 1]
                            break
                        else:
                            print(f"❌ Selección inválida. Por favor ingresa un número entre 1 y {len(matching_files)}")
                    else:
                        print(f"❌ No se encontró un número válido. Por favor ingresa un número entre 1 y {len(matching_files)}")
                except ValueError:
                    print(f"❌ Entrada inválida. Por favor ingresa un número entre 1 y {len(matching_files)}")
                except KeyboardInterrupt:
                    print("\n👋 Selección cancelada")
                    continue
        else:
            selected_file = matching_files[0]
        
        print(f"\n📄 Archivo seleccionado: {os.path.basename(selected_file)}")
        
        # Analizar contenido actual
        rows = analyze_csv_guia_aerea(selected_file)
        
        if not rows:
            continue
        
        # Pedir nuevo valor de guía aérea
        print(f"\n📝 Ingresa el nuevo valor para 'guia_aerea':")
        new_guia_value = input("Nuevo valor: ").strip()
        
        if not new_guia_value:
            print("⚠️ Valor vacío, cancelando actualización")
            continue
        
        # Opción de actualizar todos o productos específicos
        print(f"\n🎯 ¿Qué productos quieres actualizar?")
        print("1. Todos los productos")
        print("2. Productos específicos")
        
        while True:
            try:
                update_input = input("Selecciona opción (1 o 2): ").strip()
                
                # Extraer solo el primer número de la entrada
                import re
                numbers = re.findall(r'\d+', update_input)
                
                if numbers:
                    update_choice = int(numbers[0])
                    
                    if update_choice == 1:
                        # Actualizar todos
                        specific_products = None
                        break
                    elif update_choice == 2:
                        # Seleccionar productos específicos
                        print("📋 Ingresa los números de productos separados por comas (ej: 1,3,5):")
                        product_input = input("Números de productos: ").strip()
                        
                        try:
                            # Extraer todos los números de la entrada
                            product_numbers_raw = re.findall(r'\d+', product_input)
                            # Convertir a índices (1-based input to 0-based index)
                            product_numbers = [int(x) - 1 for x in product_numbers_raw]
                            specific_products = [i for i in product_numbers if 0 <= i < len(rows)]
                            
                            if not specific_products:
                                print("❌ No se seleccionaron productos válidos")
                                continue
                            
                            print(f"✅ Se actualizarán {len(specific_products)} producto(s)")
                            break
                            
                        except ValueError:
                            print("❌ Formato inválido")
                            continue
                    else:
                        print("❌ Opción inválida. Por favor ingresa 1 o 2")
                else:
                    print("❌ No se encontró un número válido. Por favor ingresa 1 o 2")
            except ValueError:
                print("❌ Entrada inválida. Por favor ingresa 1 o 2")
            except KeyboardInterrupt:
                print("\n👋 Operación cancelada")
                return
        
        # Confirmar actualización
        print(f"\n⚠️ ¿Confirmas actualizar la guía aérea a '{new_guia_value}'?")
        confirmation = input("Confirmar (s/n): ").strip().lower()
        
        if confirmation in ['s', 'si', 'sí', 'y', 'yes']:
            # Realizar actualización
            success = update_guia_aerea_in_csv(selected_file, new_guia_value, specific_products)
            
            if success:
                print(f"\n🎉 ¡Actualización completada!")
                
                # Mostrar resumen final
                print(f"\n📊 Verificando cambios...")
                analyze_csv_guia_aerea(selected_file)
            else:
                print(f"\n❌ Error en la actualización")
        else:
            print("❌ Actualización cancelada")
        
        print("\n" + "="*50)

def batch_update_by_order_list():
    """
    Actualización por lotes para múltiples pedidos
    """
    print("\n🚀 ACTUALIZACIÓN POR LOTES")
    print("-" * 50)
    print("Ingresa números de pedido separados por comas")
    print("Ejemplo: 1001, 1002, 1003")
    
    orders_input = input("Números de pedido: ").strip()
    
    if not orders_input:
        return
    
    # Procesar lista de pedidos
    order_numbers = [num.strip().replace('#', '') for num in orders_input.split(',')]
    order_numbers = [num for num in order_numbers if num]
    
    if not order_numbers:
        print("❌ No se ingresaron números válidos")
        return
    
    # Pedir valor común de guía aérea
    new_guia_value = input("Valor de guía aérea para todos: ").strip()
    
    if not new_guia_value:
        print("❌ Valor vacío")
        return
    
    # Procesar cada pedido
    for order_num in order_numbers:
        print(f"\n📦 Procesando pedido #{order_num}...")
        matching_files = find_csv_files_by_order(order_num)
        
        for csv_file in matching_files:
            print(f"  📄 Actualizando: {os.path.basename(csv_file)}")
            update_guia_aerea_in_csv(csv_file, new_guia_value)

if __name__ == "__main__":
    print("🛠️ HERRAMIENTA DE ACTUALIZACIÓN DE GUÍA AÉREA")
    print("=" * 60)
    print("Esta herramienta permite actualizar la columna 'guia_aerea' en archivos CSV existentes")
    print("Los archivos se buscan por número de pedido en la carpeta:", OUTPUT_DIR)
    print()
    
    print("🎯 Opciones disponibles:")
    print("1. Actualización interactiva (un pedido a la vez)")
    print("2. Actualización por lotes (múltiples pedidos)")
    
    while True:
        try:
            choice_input = input("\nSelecciona opción (1 o 2): ").strip()
            
            # Extraer solo el primer número de la entrada
            import re
            numbers = re.findall(r'\d+', choice_input)
            
            if numbers:
                choice = int(numbers[0])
                
                if choice == 1:
                    interactive_update()
                    break
                elif choice == 2:
                    batch_update_by_order_list()
                    break
                else:
                    print("❌ Opción inválida. Por favor ingresa 1 o 2")
            else:
                print("❌ No se encontró un número válido. Por favor ingresa 1 o 2")
                
        except ValueError:
            print("❌ Entrada inválida. Por favor ingresa 1 o 2")
        except KeyboardInterrupt:
            print("\n\n👋 Operación cancelada por el usuario")
            break 