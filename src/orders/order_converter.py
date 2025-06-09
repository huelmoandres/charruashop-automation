"""
Herramienta para convertir números de orden cortos de Shopify a IDs largos
y exportar pedidos usando números cortos
"""

from generate_csv import (
    get_order_id_from_number, 
    get_multiple_order_ids, 
    export_orders_by_short_numbers
)

def demo_conversion():
    """Ejemplo de conversión de números cortos a largos"""
    print("🎯 DEMO: Conversión de números de orden")
    print("=" * 50)
    
    # Ejemplo: convertir un solo número
    print("1️⃣ Conversión individual:")
    order_id = get_order_id_from_number("1001")
    if order_id:
        print(f"   Número corto #1001 = ID largo: {order_id}")
    
    print("\n2️⃣ Conversión múltiple:")
    # Ejemplo: convertir varios números
    short_numbers = ["1001", "1002", "1003"]
    long_ids = get_multiple_order_ids(short_numbers)
    
    print(f"\n📋 Resultados:")
    for i, short_num in enumerate(short_numbers):
        if i < len(long_ids):
            print(f"   #{short_num} -> {long_ids[i]}")
        else:
            print(f"   #{short_num} -> No encontrado")

def export_by_short_numbers_example():
    """Ejemplo de exportación usando números cortos"""
    print("\n🚀 DEMO: Exportación por números cortos")
    print("=" * 50)
    
    # Lista de números de orden cortos que quieres exportar
    orders_to_export = ["1001", "1002", "1003"]
    
    # Exportar directamente usando números cortos
    generated_files = export_orders_by_short_numbers(orders_to_export)
    
    if generated_files:
        print(f"\n✅ Se generaron {len(generated_files)} archivos CSV")
    else:
        print("\n❌ No se pudieron generar archivos")

def interactive_converter():
    """Conversor interactivo para que el usuario ingrese números"""
    print("\n🎯 CONVERSOR INTERACTIVO")
    print("=" * 50)
    print("Ingresa números de orden cortos separados por comas")
    print("Ejemplo: 1001, 1002, 1003")
    print("(Presiona Enter sin texto para salir)")
    
    while True:
        user_input = input("\n📝 Números de orden: ").strip()
        
        if not user_input:
            print("👋 ¡Hasta luego!")
            break
        
        try:
            # Procesar entrada del usuario
            short_numbers = [num.strip().replace("#", "") for num in user_input.split(",")]
            short_numbers = [num for num in short_numbers if num]  # Filtrar vacíos
            
            if not short_numbers:
                print("⚠️ No se ingresaron números válidos")
                continue
            
            print(f"\n🔍 Buscando {len(short_numbers)} pedidos...")
            
            # Convertir números
            long_ids = get_multiple_order_ids(short_numbers)
            
            if long_ids:
                print(f"\n✅ ¿Quieres exportar estos {len(long_ids)} pedidos a CSV? (s/n)")
                export_choice = input("Respuesta: ").strip().lower()
                
                if export_choice in ['s', 'si', 'sí', 'y', 'yes']:
                    print("\n📦 Exportando pedidos...")
                    generated_files = export_orders_by_short_numbers(short_numbers)
                    
                    if generated_files:
                        print(f"\n🎉 ¡Exportación completada! {len(generated_files)} archivos generados")
                    else:
                        print("\n❌ Error en la exportación")
                else:
                    print("📋 Conversión completada sin exportar")
            else:
                print("\n⚠️ No se encontraron pedidos válidos")
                
        except Exception as e:
            print(f"❌ Error procesando entrada: {e}")

if __name__ == "__main__":
    print("🛠️ HERRAMIENTA DE CONVERSIÓN DE PEDIDOS SHOPIFY")
    print("=" * 60)
    
    # Mostrar demo
    demo_conversion()
    
    # Ejemplo de exportación
    export_by_short_numbers_example()
    
    # Modo interactivo
    interactive_converter() 