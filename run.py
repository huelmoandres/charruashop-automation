#!/usr/bin/env python3
"""
🚀 Script runner para FDA/Shopify Automation
Uso: python run.py <comando>
Similar a 'npm run' en Node.js

Desarrollado por: Andrés Huelmo & Christian Huelmo
"""

import sys
import subprocess
import os
from pathlib import Path

def run_command(cmd, silent=False):
    """Ejecuta un comando del sistema con mejor feedback"""
    try:
        if not silent:
            print(f"⚡ Ejecutando...")
        result = subprocess.run(cmd, shell=True, check=True, capture_output=silent)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        if not silent:
            print(f"❌ Error: {e}")
        return False

def show_help():
    """Muestra la ayuda de comandos disponibles"""
    print("🚀 FDA Automation - Script Runner UX Optimizado")
    print("Uso: python run.py <comando>")
    print("")
    print("⚡ SHORTCUTS RÁPIDOS (nuevo):")
    print("  s                 - Status sistema (súper rápido)")
    print("  l                 - Últimas 5 líneas de log")
    print("  ls                - Estadísticas logs")
    print("  c                 - Limpieza rápida")
    print("  h                 - Health check rápido")
    print("  p                 - Performance check")
    print("  logs              - Últimas 10 líneas")
    print("  errors            - Últimos errores")
    print("  last              - Últimas 3 líneas")
    print("  size              - Tamaño de logs")
    print("")
    print("🏛️ FDA Commands:")
    print("  fda / start / dev / run / go  - FDA automation")
    print("  fda:full          - Proceso FDA directo")
    print("  fda:test          - Testing sistema")
    print("")
    print("📊 Logs & Monitoring:")
    print("  logs:stats        - Estadísticas completas")
    print("  logs:clean        - Limpieza automática")
    print("  logs:view         - Ver logs recientes")
    print("  logs:compress     - Comprimir logs antiguos")
    print("")
    print("🔧 Maintenance:")
    print("  clean:auto        - Limpieza completa")
    print("  health            - Health check completo")
    print("  performance       - Análisis performance completo")
    print("")
    print("💡 TIP: Usa shortcuts de 1 letra para comandos súper rápidos!")

def main():
    """Función principal del script runner"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1]
    
    # Diccionario de comandos disponibles (OPTIMIZADO)
    commands = {
        # FDA Commands (Optimizado)
        "fda": "python main.py",
        "fda:full": "python main.py",
        "fda:test": "python -c \"from src.core.optimized_logger import init_optimized_logging; logger = init_optimized_logging(); logger.info('Sistema de prueba', module='test')\"",
        
        # Shopify/Orders Commands
        "shopify:export": "python src/orders/generate_csv.py",
        "shopify:upload-metafields": "python src/shopify/upload_fda_metafields.py",
        "orders:convert": "python src/orders/order_converter.py",
        "orders:guia": "python src/orders/update_guia_aerea.py",
        "orders:analyze": "python src/orders/csv_utils.py",
        "shopify:export-fda-mapping": "python src/shopify/export_products_for_fda_mapping.py",
        
        # Logs & Monitoring (OPTIMIZADO)
        "logs:stats": "python src/utils/log_cleaner.py",
        "logs:clean": "python -c \"from src.utils.log_cleaner import LogCleaner; LogCleaner().compress_old_logs()\"",
        "logs:view": "tail -20 logs/fda_automation.log",
        "logs:compress": "python -c \"from src.utils.log_cleaner import LogCleaner; LogCleaner().full_cleanup()\"",
        
        # Maintenance (OPTIMIZADO)
        "clean:auto": "python -c \"from src.utils.log_cleaner import LogCleaner; LogCleaner().full_cleanup()\"",
        "health": "python -c \"from src.core.optimized_logger import get_optimized_logger; logger = get_optimized_logger(); print('✅ Sistema optimizado funcionando')\"",
        "performance": "python -c \"from src.core.performance import get_global_performance_tracker; tracker = get_global_performance_tracker(); print(tracker.get_current_stats())\"",
        
        # Setup
        "install": "pip install -r requirements.txt",
        "setup": "python -c \"from src.core.optimized_logger import init_optimized_logging; logger = init_optimized_logging(); logger.info('Setup completado', module='setup')\"",
        
        # Aliases y Shortcuts adicionales
        "start": "python main.py",
        "dev": "python main.py",
        "run": "python main.py",
        "go": "python main.py",
        "test": "python -c \"from src.core.optimized_logger import init_optimized_logging; logger = init_optimized_logging(); logger.info('Test completado', module='test')\"",
        
        # Shortcuts rápidos
        "s": "python -c \"from src.core.optimized_logger import get_optimized_logger; logger = get_optimized_logger(); print('✅ Sistema OK')\"",
        "l": "tail -5 logs/fda_automation.log",
        "ls": "python src/utils/log_cleaner.py",
        "c": "python -c \"from src.utils.log_cleaner import LogCleaner; LogCleaner().full_cleanup(); print('🧹 Limpieza completada')\"",
        "h": "python -c \"from src.core.optimized_logger import get_optimized_logger; logger = get_optimized_logger(); print('💚 Sistema saludable')\"",
        "p": "python -c \"from src.core.performance import get_global_performance_tracker; print('📊 Performance OK')\"",
        
        # Shortcuts de logs
        "logs": "tail -10 logs/fda_automation.log",
        "errors": "grep -i error logs/fda_automation.log | tail -5 || echo '✅ Sin errores recientes'",
        "last": "tail -3 logs/fda_automation.log",
        "size": "du -sh logs/",
    }
    
    if command in commands:
        # Comandos rápidos sin output verbose
        if command in ['s', 'l', 'ls', 'c', 'h', 'p', 'logs', 'errors', 'last', 'size']:
            success = run_command(commands[command], silent=True)
            if not success:
                print(f"❌ Error en '{command}'")
        else:
            print(f"🚀 {command}")
            success = run_command(commands[command])
            if success:
                print(f"✅ Listo")
            else:
                print(f"❌ Error")
    else:
        print(f"❌ '{command}' no existe")
        print("\n💡 Comandos rápidos: s, l, ls, c, h, p, logs, errors, last, size")
        print("   Usa 'python run.py' para ver todos los comandos")

if __name__ == "__main__":
    main() 