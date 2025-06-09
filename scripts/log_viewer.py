#!/usr/bin/env python3
"""
Utilidades para visualizar logs del sistema de automatización
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path

def get_today_date():
    """Obtiene la fecha de hoy en formato YYYY-MM-DD"""
    return datetime.now().strftime('%Y-%m-%d')

def view_fda_logs():
    """Ver logs de FDA del día actual"""
    today = get_today_date()
    log_path = f"logs/fda/{today}/{today}_fda_automation.log"
    
    if os.path.exists(log_path):
        print(f"📊 Mostrando logs de FDA del {today}")
        subprocess.run(["cat", log_path])
    else:
        print(f"❌ No se encontraron logs de FDA para {today}")

def view_error_logs():
    """Ver logs de errores del día actual"""
    today = get_today_date()
    log_path = f"logs/errors/{today}/{today}_errors.log"
    
    if os.path.exists(log_path):
        print(f"🚨 Mostrando logs de errores del {today}")
        subprocess.run(["cat", log_path])
    else:
        print(f"✅ No hay logs de errores para {today}")

def view_performance_logs():
    """Ver logs de performance del día actual"""
    today = get_today_date()
    log_path = f"logs/performance/{today}/{today}_performance.log"
    
    if os.path.exists(log_path):
        print(f"⚡ Mostrando logs de performance del {today}")
        subprocess.run(["cat", log_path])
    else:
        print(f"❌ No se encontraron logs de performance para {today}")

def tail_logs():
    """Seguir logs de FDA en tiempo real"""
    today = get_today_date()
    log_path = f"logs/fda/{today}/{today}_fda_automation.log"
    
    if os.path.exists(log_path):
        print(f"👁️ Siguiendo logs de FDA en tiempo real (Ctrl+C para salir)")
        subprocess.run(["tail", "-f", log_path])
    else:
        print(f"❌ No se encontraron logs de FDA para {today}")

def list_available_logs():
    """Lista todos los logs disponibles"""
    logs_dir = Path("logs")
    if not logs_dir.exists():
        print("❌ Directorio de logs no encontrado")
        return
    
    print("📁 Logs disponibles:")
    for category in ["sessions", "fda", "shopify", "selenium", "performance", "errors"]:
        category_path = logs_dir / category
        if category_path.exists():
            dates = [d.name for d in category_path.iterdir() if d.is_dir()]
            if dates:
                print(f"  📊 {category}: {', '.join(sorted(dates))}")

if __name__ == "__main__":
    import sys
    
    commands = {
        "fda": view_fda_logs,
        "errors": view_error_logs,
        "performance": view_performance_logs,
        "tail": tail_logs,
        "list": list_available_logs
    }
    
    if len(sys.argv) > 1 and sys.argv[1] in commands:
        commands[sys.argv[1]]()
    else:
        print("📊 Comandos disponibles:")
        print("  python scripts/log_viewer.py fda         - Ver logs de FDA")
        print("  python scripts/log_viewer.py errors      - Ver logs de errores")
        print("  python scripts/log_viewer.py performance - Ver logs de performance")
        print("  python scripts/log_viewer.py tail        - Seguir logs en tiempo real")
        print("  python scripts/log_viewer.py list        - Listar logs disponibles") 