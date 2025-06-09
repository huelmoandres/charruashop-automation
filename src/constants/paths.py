"""
Rutas fijas del proyecto - Configuración simple y directa
"""

import os
from pathlib import Path

# Directorio raíz del proyecto
ROOT_DIR = Path(__file__).parent.parent.parent

# Directorios principales
SRC_DIR = ROOT_DIR / "src"
CONFIG_DIR = ROOT_DIR / "config"
DOCS_DIR = ROOT_DIR / "docs"
DATA_DIR = ROOT_DIR / "data"
LOGS_DIR = ROOT_DIR / "logs"
DRIVERS_DIR = ROOT_DIR / "drivers"

# Directorios de datos
SAMPLES_DIR = DATA_DIR / "samples"

# Directorios de outputs específicos
ORDERS_OUTPUT_DIR = SRC_DIR / "orders" / "output"

# ChromeDriver
CHROMEDRIVER_PATH = DRIVERS_DIR / "chromedriver"

# Archivos específicos
ORDER_SAMPLE_FILE = SAMPLES_DIR / "order_sample.csv"
ORDERS_EXPORT_FILE = DATA_DIR / "orders_export.csv"

def ensure_directories():
    """Crea las carpetas necesarias si no existen"""
    directories = [
        DATA_DIR,
        SAMPLES_DIR,
        ORDERS_OUTPUT_DIR,
        DRIVERS_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def show_paths():
    """Muestra las rutas configuradas"""
    print("\n📋 RUTAS DEL PROYECTO:")
    print("=" * 40)
    print(f"📁 Root: {ROOT_DIR}")
    print(f"📁 Source: {SRC_DIR}")
    print(f"📁 Config: {CONFIG_DIR}")
    print(f"📁 Data: {DATA_DIR}")
    print(f"📁 Logs: {LOGS_DIR}")
    print(f"📁 Samples: {SAMPLES_DIR}")
    print(f"📁 Orders Output: {ORDERS_OUTPUT_DIR}")
    print(f"🔧 ChromeDriver: {CHROMEDRIVER_PATH}")

if __name__ == "__main__":
    ensure_directories()
    show_paths() 