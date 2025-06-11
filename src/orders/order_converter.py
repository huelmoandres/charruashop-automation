import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

"""
Herramienta para convertir números de orden cortos de Shopify a IDs largos
y exportar pedidos usando números cortos
"""

from generate_csv import (
    get_order_id_from_number, 
    get_multiple_order_ids, 
    export_orders_by_short_numbers
)
from src.core.logger import AutomationLogger

# Inicializar logger
logger = AutomationLogger.get_instance()

def demo_conversion():
    """Ejemplo de conversión de números cortos a largos"""
    logger.shopify_logger.info("=== INICIANDO DEMO DE CONVERSIÓN DE NÚMEROS ===")
    
    print("🎯 DEMO: Conversión de números de orden")
    print("=" * 50)
    
    # Ejemplo: convertir un solo número
    print("1️⃣ Conversión individual:")
    test_number = "1001"
    
    logger.shopify_logger.debug("Convirtiendo número individual", extra={"order_number": test_number})
    order_id = get_order_id_from_number(test_number)
    
    if order_id:
        logger.shopify_logger.info("Conversión individual exitosa", extra={
            "short_number": test_number,
            "long_id": order_id
        })
        print(f"   Número corto #{test_number} = ID largo: {order_id}")
    else:
        logger.shopify_logger.warning("No se pudo convertir número individual", extra={"order_number": test_number})
    
    print("\n2️⃣ Conversión múltiple:")
    # Ejemplo: convertir varios números
    short_numbers = ["1001", "1002", "1003"]
    
    logger.shopify_logger.info("Iniciando conversión múltiple", extra={
        "short_numbers": short_numbers,
        "count": len(short_numbers)
    })
    
    long_ids = get_multiple_order_ids(short_numbers)
    
    print(f"\n📋 Resultados:")
    conversion_results = {}
    for i, short_num in enumerate(short_numbers):
        if i < len(long_ids):
            conversion_results[short_num] = long_ids[i]
            print(f"   #{short_num} -> {long_ids[i]}")
        else:
            conversion_results[short_num] = "No encontrado"
            print(f"   #{short_num} -> No encontrado")
    
    logger.shopify_logger.info("=== DEMO CONVERSIÓN COMPLETADO ===", extra={
        "conversion_results": conversion_results,
        "successful_conversions": len(long_ids),
        "total_attempts": len(short_numbers)
    })

def export_by_short_numbers_example():
    """Ejemplo de exportación usando números cortos"""
    logger.shopify_logger.info("=== INICIANDO DEMO DE EXPORTACIÓN ===")
    
    print("\n🚀 DEMO: Exportación por números cortos")
    print("=" * 50)
    
    # Lista de números de orden cortos que quieres exportar
    orders_to_export = ["1001", "1002", "1003"]
    
    logger.shopify_logger.info("Ejecutando exportación de ejemplo", extra={
        "orders_to_export": orders_to_export,
        "count": len(orders_to_export)
    })
    
    # Exportar directamente usando números cortos
    generated_files = export_orders_by_short_numbers(orders_to_export)
    
    if generated_files:
        logger.shopify_logger.info("=== EXPORTACIÓN DEMO COMPLETADA ===", extra={
            "generated_files": generated_files,
            "files_count": len(generated_files)
        })
        print(f"\n✅ Se generaron {len(generated_files)} archivos CSV")
    else:
        logger.shopify_logger.error("Error en exportación demo")
        print("\n❌ No se pudieron generar archivos")

def interactive_converter():
    """Conversor interactivo para que el usuario ingrese números"""
    logger.shopify_logger.info("=== INICIANDO CONVERSOR INTERACTIVO ===")
    
    print("\n🎯 CONVERSOR INTERACTIVO")
    print("=" * 50)
    print("Ingresa números de orden cortos separados por comas")
    print("Ejemplo: 1001, 1002, 1003")
    print("(Presiona Enter sin texto para salir)")
    
    while True:
        user_input = input("\n📝 Números de orden: ").strip()
        
        if not user_input:
            logger.shopify_logger.info("Usuario salió del conversor interactivo")
            print("👋 ¡Hasta luego!")
            break
        
        try:
            # Procesar entrada del usuario
            short_numbers = [num.strip().replace("#", "") for num in user_input.split(",")]
            short_numbers = [num for num in short_numbers if num]  # Filtrar vacíos
            
            if not short_numbers:
                logger.shopify_logger.warning("Usuario ingresó números inválidos", extra={"user_input": user_input})
                print("⚠️ No se ingresaron números válidos")
                continue
            
            logger.shopify_logger.info("Procesando entrada del usuario", extra={
                "raw_input": user_input,
                "processed_numbers": short_numbers,
                "count": len(short_numbers)
            })
            
            print(f"\n🔍 Buscando {len(short_numbers)} pedidos...")
            
            # Convertir números
            long_ids = get_multiple_order_ids(short_numbers)
            
            if long_ids:
                logger.shopify_logger.info("Conversión interactiva exitosa", extra={
                    "converted_ids": long_ids,
                    "conversion_count": len(long_ids)
                })
                
                print(f"\n✅ ¿Quieres exportar estos {len(long_ids)} pedidos a CSV? (s/n)")
                export_choice = input("Respuesta: ").strip().lower()
                
                if export_choice in ['s', 'si', 'sí', 'y', 'yes']:
                    logger.shopify_logger.info("Usuario eligió exportar pedidos")
                    print("\n📦 Exportando pedidos...")
                    generated_files = export_orders_by_short_numbers(short_numbers)
                    
                    if generated_files:
                        logger.shopify_logger.info("Exportación interactiva completada", extra={
                            "generated_files": generated_files,
                            "files_count": len(generated_files)
                        })
                        print(f"\n🎉 ¡Exportación completada! {len(generated_files)} archivos generados")
                    else:
                        logger.shopify_logger.error("Error en exportación interactiva")
                        print("\n❌ Error en la exportación")
                else:
                    logger.shopify_logger.info("Usuario eligió no exportar")
                    print("📋 Conversión completada sin exportar")
            else:
                logger.shopify_logger.warning("No se encontraron pedidos válidos en conversión interactiva", extra={
                    "short_numbers": short_numbers
                })
                print("\n⚠️ No se encontraron pedidos válidos")
                
        except Exception as e:
            logger.shopify_logger.error("Error procesando entrada del usuario", extra={
                "user_input": user_input,
                "error": str(e)
            })
            logger.error_logger.error("Interactive converter error", extra={
                "source_module": "orders_order_converter",
                "function": "interactive_converter",
                "user_input": user_input,
                "error": str(e)
            })
            print(f"❌ Error procesando entrada: {e}")

if __name__ == "__main__":
    logger.shopify_logger.info("=== INICIANDO HERRAMIENTA DE CONVERSIÓN DE PEDIDOS ===")
    
    print("🛠️ HERRAMIENTA DE CONVERSIÓN DE PEDIDOS SHOPIFY")
    print("=" * 60)
    
    # Mostrar demo
    demo_conversion()
    
    # Ejemplo de exportación
    export_by_short_numbers_example()
    
    # Modo interactivo
    interactive_converter()
    
    logger.shopify_logger.info("=== HERRAMIENTA DE CONVERSIÓN FINALIZADA ===") 