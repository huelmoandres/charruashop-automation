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

def run_command(cmd):
    """Ejecuta un comando del sistema"""
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando comando: {e}")
        return False

def show_help():
    """Muestra la ayuda de comandos disponibles"""
    print("🚀 FDA/Shopify Automation - Script Runner")
    print("Uso: python run.py <comando>")
    print("")
    print("🏛️ FDA Commands:")
    print("  fda               - Proceso FDA completo")
    print("  fda:full          - Proceso FDA directo")
    print("  fda:test          - Testing de pasos individuales")
    print("  fda:coordinator   - Ejecutar coordinador FDA")
    print("")
    print("🛒 Shopify/Orders Commands:")
    print("  shopify:export    - Exportar pedidos de Shopify")
    print("  orders:convert    - Convertir números de orden")
    print("  orders:guia       - Actualizar guías aéreas")
    print("  orders:analyze    - Analizar CSVs generados")
    print("")
    print("📊 Logs & Monitoring:")
    print("  logs:fda          - Ver logs de FDA del día")
    print("  logs:errors       - Ver logs de errores")
    print("  logs:performance  - Ver logs de performance")
    print("  logs:tail         - Seguir logs en tiempo real")
    print("  logs:list         - Listar logs disponibles")
    print("")
    print("🔧 Maintenance:")
    print("  clean:logs        - Limpiar logs antiguos")
    print("  backup            - Backup de datos")
    print("  health            - Health check del sistema")
    print("  clean:screenshots - Limpiar screenshots antiguos")
    print("")
    print("📦 Setup:")
    print("  install           - Instalar dependencias")
    print("  setup             - Setup inicial")

def main():
    """Función principal del script runner"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1]
    
    # Diccionario de comandos disponibles
    commands = {
        # FDA Commands
        "fda": "python main.py",
        "fda:full": "python -c \"from main import main_fda_process; main_fda_process()\"",
        "fda:test": "python -c \"from src.fda.prior_notice.management.creation_coordinator import test_individual_steps; test_individual_steps()\"",
        "fda:coordinator": "python -c \"from src.fda.prior_notice.management.creation_coordinator import coordinate_prior_notice_creation; coordinate_prior_notice_creation()\"",
        
        # Shopify/Orders Commands
        "shopify:export": "python src/orders/generate_csv.py",
        "orders:convert": "python src/orders/order_converter.py",
        "orders:guia": "python src/orders/update_guia_aerea.py",
        "orders:analyze": "python src/orders/csv_utils.py",
        
        # Logs & Monitoring
        "logs:fda": "python scripts/log_viewer.py fda",
        "logs:errors": "python scripts/log_viewer.py errors",
        "logs:performance": "python scripts/log_viewer.py performance",
        "logs:tail": "python scripts/log_viewer.py tail",
        "logs:list": "python scripts/log_viewer.py list",
        
        # Maintenance
        "clean:logs": "python scripts/maintenance.py clean-logs",
        "backup": "python scripts/maintenance.py backup",
        "health": "python scripts/maintenance.py health",
        "clean:screenshots": "python scripts/maintenance.py clean-screenshots",
        
        # Setup
        "install": "pip install -r requirements.txt",
        "setup": "python scripts/maintenance.py init",
        
        # Aliases comunes
        "start": "python main.py",
        "dev": "python main.py",
        "test": "python -c \"from src.fda.prior_notice.management.creation_coordinator import test_individual_steps; test_individual_steps()\"",
    }
    
    if command in commands:
        print(f"🚀 Ejecutando: {command}")
        success = run_command(commands[command])
        if success:
            print(f"✅ Comando '{command}' completado exitosamente")
        else:
            print(f"❌ Error ejecutando comando '{command}'")
    else:
        print(f"❌ Comando '{command}' no reconocido")
        print("")
        show_help()

if __name__ == "__main__":
    main() 