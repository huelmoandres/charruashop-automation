#!/usr/bin/env python3
"""
Utilidades de mantenimiento para el sistema de automatización
"""

import os
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

def clean_old_logs():
    """Limpia logs antiguos (más de 30 días)"""
    logs_dir = Path("logs")
    if not logs_dir.exists():
        print("❌ Directorio de logs no encontrado")
        return
    
    cutoff_date = datetime.now() - timedelta(days=30)
    cutoff_str = cutoff_date.strftime('%Y-%m-%d')
    
    cleaned_count = 0
    
    for category in logs_dir.iterdir():
        if category.is_dir():
            for date_dir in category.iterdir():
                if date_dir.is_dir() and date_dir.name < cutoff_str:
                    print(f"🗑️ Eliminando logs antiguos: {category.name}/{date_dir.name}")
                    shutil.rmtree(date_dir)
                    cleaned_count += 1
    
    if cleaned_count > 0:
        print(f"✅ Se eliminaron {cleaned_count} directorios de logs antiguos")
    else:
        print("✅ No hay logs antiguos para limpiar")

def backup_data():
    """Crea backup de la carpeta data/"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"backup_data_{timestamp}"
    
    try:
        shutil.copytree("data", f"backups/{backup_name}")
        print(f"✅ Backup creado: backups/{backup_name}")
    except Exception as e:
        print(f"❌ Error creando backup: {e}")

def health_check():
    """Verifica el estado del sistema"""
    print("🔍 Verificando estado del sistema...")
    
    # Verificar estructura de directorios
    required_dirs = ["data", "src", "logs", "config"]
    missing_dirs = []
    
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"❌ Directorios faltantes: {', '.join(missing_dirs)}")
    else:
        print("✅ Estructura de directorios OK")
    
    # Verificar archivos críticos
    critical_files = [
        "data/orders_export.csv",
        "config/config.py",
        "main.py"
    ]
    
    missing_files = []
    for file_path in critical_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Archivos críticos faltantes: {', '.join(missing_files)}")
    else:
        print("✅ Archivos críticos OK")
    
    # Verificar logs recientes
    today = datetime.now().strftime('%Y-%m-%d')
    fda_log_path = f"logs/fda/{today}"
    
    if os.path.exists(fda_log_path):
        print("✅ Logs de FDA actuales encontrados")
    else:
        print("⚠️ No hay logs de FDA para hoy")
    
    # Verificar espacio en disco
    try:
        total, used, free = shutil.disk_usage(".")
        free_gb = free // (1024**3)
        print(f"💽 Espacio libre: {free_gb} GB")
        
        if free_gb < 1:
            print("⚠️ Poco espacio en disco disponible")
    except:
        print("❌ No se pudo verificar espacio en disco")
    
    print("🎯 Health check completado")

def create_backup_dir():
    """Crea directorio de backups si no existe"""
    backup_dir = Path("backups")
    if not backup_dir.exists():
        backup_dir.mkdir()
        print("📁 Directorio de backups creado")

def clean_screenshots():
    """Limpia screenshots antiguos (más de 7 días)"""
    screenshots_dir = Path("logs/screenshots")
    if not screenshots_dir.exists():
        print("❌ Directorio de screenshots no encontrado")
        return
    
    cutoff_date = datetime.now() - timedelta(days=7)
    cutoff_str = cutoff_date.strftime('%Y-%m-%d')
    
    cleaned_count = 0
    
    for date_dir in screenshots_dir.iterdir():
        if date_dir.is_dir() and date_dir.name < cutoff_str:
            print(f"🖼️ Eliminando screenshots antiguos: {date_dir.name}")
            shutil.rmtree(date_dir)
            cleaned_count += 1
    
    if cleaned_count > 0:
        print(f"✅ Se eliminaron {cleaned_count} directorios de screenshots antiguos")
    else:
        print("✅ No hay screenshots antiguos para limpiar")

if __name__ == "__main__":
    import sys
    
    commands = {
        "clean-logs": clean_old_logs,
        "backup": backup_data,
        "health": health_check,
        "clean-screenshots": clean_screenshots,
        "init": create_backup_dir
    }
    
    if len(sys.argv) > 1 and sys.argv[1] in commands:
        commands[sys.argv[1]]()
    else:
        print("🔧 Comandos de mantenimiento disponibles:")
        print("  python scripts/maintenance.py clean-logs       - Limpiar logs antiguos (>30 días)")
        print("  python scripts/maintenance.py backup           - Backup de carpeta data/")
        print("  python scripts/maintenance.py health           - Health check del sistema")
        print("  python scripts/maintenance.py clean-screenshots - Limpiar screenshots antiguos (>7 días)")
        print("  python scripts/maintenance.py init             - Crear directorios necesarios") 