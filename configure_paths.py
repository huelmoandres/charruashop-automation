#!/usr/bin/env python3
"""
Script de Configuración Rápida de Rutas
Permite a los usuarios personalizar fácilmente dónde se guardan los CSV y archivos de salida
"""

import os
from pathlib import Path

def show_welcome():
    """Muestra bienvenida y explicación"""
    print("🛠️ CONFIGURADOR DE RUTAS FDA AUTOMATION")
    print("=" * 50)
    print("Este script te ayuda a personalizar las carpetas donde")
    print("se guardan los archivos CSV y de salida del sistema.")
    print()
    print("🎯 Configuraciones disponibles:")
    print("  📁 Carpeta para archivos CSV (shopify, fda, orders)")
    print("  📤 Carpeta para archivos de salida (reports, logs)")
    print("  📸 Carpeta para screenshots")
    print()

def get_user_preferences():
    """Solicita las preferencias del usuario"""
    print("📋 CONFIGURACIÓN DE CARPETAS")
    print("-" * 30)
    
    # CSV Folder
    print("\n1️⃣ Carpeta para archivos CSV:")
    print("   Aquí se guardarán: orders.csv, fda_data.csv, exports, etc.")
    print("   💡 Sugerencias: 'csv_data', 'data', 'shopify_files'")
    csv_folder = input("   📁 Nombre de carpeta CSV (Enter = 'csv_data'): ").strip()
    if not csv_folder:
        csv_folder = "csv_data"
    
    # Output Folder
    print("\n2️⃣ Carpeta para archivos de salida:")
    print("   Aquí se guardarán: reports, logs, resultados procesados")
    print("   💡 Sugerencias: 'results', 'output', 'generated_files'")
    output_folder = input("   📤 Nombre de carpeta de salida (Enter = 'results'): ").strip()
    if not output_folder:
        output_folder = "results"
    
    # Screenshots Folder
    print("\n3️⃣ Carpeta para screenshots:")
    print("   Aquí se guardarán las capturas de pantalla automáticas")
    print("   💡 Sugerencias: 'capturas', 'screenshots', 'imagenes'")
    screenshots_folder = input("   📸 Nombre de carpeta screenshots (Enter = 'capturas'): ").strip()
    if not screenshots_folder:
        screenshots_folder = "capturas"
    
    return csv_folder, output_folder, screenshots_folder

def show_configuration_preview(csv_folder, output_folder, screenshots_folder):
    """Muestra preview de la configuración"""
    print("\n📋 PREVIEW DE CONFIGURACIÓN")
    print("-" * 30)
    
    current_dir = Path.cwd()
    
    print(f"📁 Directorio del proyecto: {current_dir}")
    print(f"📁 Carpeta CSV: {current_dir / csv_folder}")
    print(f"   └── shopify/")
    print(f"   └── fda/")
    print(f"   └── orders/")
    print(f"   └── exports/")
    print(f"   └── backups/")
    print(f"📤 Carpeta salida: {current_dir / output_folder}")
    print(f"   └── csv/")
    print(f"   └── reports/")
    print(f"   └── logs/")
    print(f"📸 Screenshots: {current_dir / screenshots_folder}")
    
    return True

def update_paths_file(csv_folder, output_folder, screenshots_folder):
    """Actualiza el archivo paths.py con las nuevas configuraciones"""
    
    paths_file = Path("src/constants/paths.py")
    
    if not paths_file.exists():
        print(f"❌ Error: No se encontró {paths_file}")
        print("💡 Asegúrate de ejecutar este script desde el directorio raíz del proyecto")
        return False
    
    try:
        # Leer el archivo actual
        with open(paths_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar las configuraciones en UserPreferences
        lines = content.split('\n')
        updated_lines = []
        
        for line in lines:
            if 'CSV_FOLDER =' in line and 'UserPreferences' in content[content.find('class UserPreferences'):content.find('CSV_FOLDER =')]:
                updated_lines.append(f'    CSV_FOLDER = "{csv_folder}"  # Cambia por el nombre que prefieras')
            elif 'OUTPUT_FOLDER =' in line and 'UserPreferences' in content[content.find('class UserPreferences'):content.find('OUTPUT_FOLDER =')]:
                updated_lines.append(f'    OUTPUT_FOLDER = "{output_folder}"  # Cambia por el nombre que prefieras')
            elif 'SCREENSHOTS_FOLDER =' in line and 'UserPreferences' in content[content.find('class UserPreferences'):content.find('SCREENSHOTS_FOLDER =')]:
                updated_lines.append(f'    SCREENSHOTS_FOLDER = "{screenshots_folder}"  # Cambia por el nombre que prefieras')
            else:
                updated_lines.append(line)
        
        # Escribir el archivo actualizado
        with open(paths_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(updated_lines))
        
        print(f"✅ Archivo {paths_file} actualizado correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando archivo: {e}")
        return False

def create_directories(csv_folder, output_folder, screenshots_folder):
    """Crea las carpetas configuradas"""
    print(f"\n📁 CREANDO CARPETAS...")
    
    current_dir = Path.cwd()
    
    folders_to_create = [
        # CSV folders
        current_dir / csv_folder,
        current_dir / csv_folder / "shopify",
        current_dir / csv_folder / "fda", 
        current_dir / csv_folder / "orders",
        current_dir / csv_folder / "exports",
        current_dir / csv_folder / "backups",
        
        # Output folders
        current_dir / output_folder,
        current_dir / output_folder / "csv",
        current_dir / output_folder / "reports",
        current_dir / output_folder / "logs",
        current_dir / output_folder / "pdf",
        
        # Screenshots
        current_dir / screenshots_folder,
        
        # Config
        current_dir / "config"
    ]
    
    created_count = 0
    for folder in folders_to_create:
        try:
            folder.mkdir(parents=True, exist_ok=True)
            print(f"   ✅ {folder}")
            created_count += 1
        except Exception as e:
            print(f"   ❌ Error creando {folder}: {e}")
    
    print(f"\n📊 Resultado: {created_count}/{len(folders_to_create)} carpetas creadas/verificadas")
    return created_count == len(folders_to_create)

def main():
    """Función principal"""
    
    show_welcome()
    
    # Solicitar preferencias
    csv_folder, output_folder, screenshots_folder = get_user_preferences()
    
    # Mostrar preview
    show_configuration_preview(csv_folder, output_folder, screenshots_folder)
    
    # Confirmar
    print(f"\n❓ ¿Confirmas esta configuración?")
    confirm = input("   ✅ (s/n): ").strip().lower()
    
    if confirm not in ['s', 'si', 'yes', 'y']:
        print("❌ Configuración cancelada")
        return
    
    # Aplicar cambios
    print(f"\n🔧 APLICANDO CONFIGURACIÓN...")
    
    # Actualizar archivo paths.py
    if not update_paths_file(csv_folder, output_folder, screenshots_folder):
        print("❌ Error al actualizar configuración")
        return
    
    # Crear carpetas
    if not create_directories(csv_folder, output_folder, screenshots_folder):
        print("⚠️ Algunas carpetas no se pudieron crear")
    
    # Verificar resultado
    print(f"\n🎉 CONFIGURACIÓN COMPLETADA")
    print("=" * 30)
    print("✅ Archivo paths.py actualizado")
    print("✅ Carpetas creadas")
    print()
    print("🎯 Próximos pasos:")
    print("1. Coloca tu archivo orders.csv en:")
    print(f"   📁 {Path.cwd() / csv_folder / 'fda' / 'order.csv'}")
    print("2. Ejecuta el sistema FDA normalmente")
    print("3. Todos los archivos se guardarán en las carpetas configuradas")
    print()
    print("💡 Para cambiar la configuración, ejecuta este script de nuevo")

if __name__ == "__main__":
    main() 