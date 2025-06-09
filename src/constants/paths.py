"""
Rutas y configuraciones de archivos centralizadas
Permite personalizar dónde se almacenan los diferentes tipos de archivos
"""

import os
from pathlib import Path

class ProjectPaths:
    """Rutas base del proyecto"""
    
    # Directorio raíz del proyecto
    ROOT_DIR = Path(__file__).parent.parent.parent
    
    # Directorios principales
    SRC_DIR = ROOT_DIR / "src"
    CONFIG_DIR = ROOT_DIR / "config"
    DOCS_DIR = ROOT_DIR / "docs"
    TESTS_DIR = ROOT_DIR / "tests"
    
    # Directorio de datos temporales
    TEMP_DIR = ROOT_DIR / "temp"

class CSVPaths:
    """Rutas para archivos CSV - CONFIGURABLES POR USUARIO"""
    
    # 📁 CARPETA BASE PARA CSV - CAMBIAR SEGÚN PREFERENCIA
    CSV_BASE_DIR = ProjectPaths.ROOT_DIR / "csv_files"  # 👈 PERSONALIZABLE
    
    # Subcarpetas organizadas
    SHOPIFY_DIR = CSV_BASE_DIR / "shopify"
    FDA_DIR = CSV_BASE_DIR / "fda" 
    ORDERS_DIR = CSV_BASE_DIR / "orders"
    EXPORTS_DIR = CSV_BASE_DIR / "exports"
    BACKUPS_DIR = CSV_BASE_DIR / "backups"
    
    # Archivos específicos
    ORDER_EXPORT_FILE = SHOPIFY_DIR / "orders_export.csv"
    FDA_ORDER_FILE = FDA_DIR / "order.csv"
    
    @classmethod
    def create_directories(cls):
        """Crea todas las carpetas necesarias si no existen"""
        directories = [
            cls.CSV_BASE_DIR,
            cls.SHOPIFY_DIR, 
            cls.FDA_DIR,
            cls.ORDERS_DIR,
            cls.EXPORTS_DIR,
            cls.BACKUPS_DIR
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"📁 Directorio asegurado: {directory}")

class OutputPaths:
    """Rutas para archivos de salida"""
    
    # 📁 CARPETA BASE PARA OUTPUTS - PERSONALIZABLE
    OUTPUT_BASE_DIR = ProjectPaths.ROOT_DIR / "output"  # 👈 PERSONALIZABLE
    
    # Subcarpetas por tipo
    CSV_OUTPUT_DIR = OUTPUT_BASE_DIR / "csv"
    PDF_OUTPUT_DIR = OUTPUT_BASE_DIR / "pdf"
    SCREENSHOTS_DIR = OUTPUT_BASE_DIR / "screenshots"
    LOGS_DIR = OUTPUT_BASE_DIR / "logs"
    REPORTS_DIR = OUTPUT_BASE_DIR / "reports"
    
    @classmethod
    def create_directories(cls):
        """Crea todas las carpetas de salida"""
        directories = [
            cls.OUTPUT_BASE_DIR,
            cls.CSV_OUTPUT_DIR,
            cls.PDF_OUTPUT_DIR, 
            cls.SCREENSHOTS_DIR,
            cls.LOGS_DIR,
            cls.REPORTS_DIR
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"📁 Directorio de salida asegurado: {directory}")

class SeleniumPaths:
    """Rutas para archivos de Selenium"""
    
    # ChromeDriver
    CHROMEDRIVER_PATH = ProjectPaths.ROOT_DIR / "drivers" / "chromedriver"
    
    # Perfil de Chrome - PERSONALIZABLE
    CHROME_PROFILE_DIR = Path.home() / "Library" / "Application Support" / "Google" / "Chrome" / "selenium-profile"  # 👈 PERSONALIZABLE
    
    # Screenshots automáticos
    SCREENSHOTS_DIR = OutputPaths.SCREENSHOTS_DIR

class ConfigPaths:
    """Rutas para archivos de configuración"""
    
    # Archivo de configuración principal
    MAIN_CONFIG = ProjectPaths.CONFIG_DIR / "config.py"
    
    # Configuraciones específicas
    FDA_CONFIG = ProjectPaths.CONFIG_DIR / "fda_config.json"
    SHOPIFY_CONFIG = ProjectPaths.CONFIG_DIR / "shopify_config.json"
    SELENIUM_CONFIG = ProjectPaths.CONFIG_DIR / "selenium_config.json"

# 🎯 CONFIGURACIÓN RÁPIDA PARA USUARIOS
class UserPreferences:
    """
    Configuración rápida para usuarios - PERSONALIZAR AQUÍ
    """
    
    # 📍 ¿Dónde quieres guardar los CSV?
    CSV_FOLDER = "csv_data"  # Cambia por el nombre que prefieras
    
    # 📍 ¿Dónde quieres los archivos de salida? 
    OUTPUT_FOLDER = "results"  # Cambia por el nombre que prefieras
    
    # 📍 ¿Usar carpeta específica para screenshots?
    SCREENSHOTS_FOLDER = "capturas"  # Cambia por el nombre que prefieras
    
    @classmethod
    def apply_preferences(cls):
        """Aplica las preferencias del usuario a las rutas"""
        
        # Actualizar rutas base según preferencias
        if cls.CSV_FOLDER:
            CSVPaths.CSV_BASE_DIR = ProjectPaths.ROOT_DIR / cls.CSV_FOLDER
            # Actualizar subcarpetas
            CSVPaths.SHOPIFY_DIR = CSVPaths.CSV_BASE_DIR / "shopify"
            CSVPaths.FDA_DIR = CSVPaths.CSV_BASE_DIR / "fda"
            CSVPaths.ORDERS_DIR = CSVPaths.CSV_BASE_DIR / "orders"
            CSVPaths.EXPORTS_DIR = CSVPaths.CSV_BASE_DIR / "exports"
            CSVPaths.BACKUPS_DIR = CSVPaths.CSV_BASE_DIR / "backups"
            # Actualizar archivos específicos
            CSVPaths.ORDER_EXPORT_FILE = CSVPaths.SHOPIFY_DIR / "orders_export.csv"
            CSVPaths.FDA_ORDER_FILE = CSVPaths.FDA_DIR / "order.csv"
        
        if cls.OUTPUT_FOLDER:
            OutputPaths.OUTPUT_BASE_DIR = ProjectPaths.ROOT_DIR / cls.OUTPUT_FOLDER
            # Actualizar subcarpetas
            OutputPaths.CSV_OUTPUT_DIR = OutputPaths.OUTPUT_BASE_DIR / "csv"
            OutputPaths.PDF_OUTPUT_DIR = OutputPaths.OUTPUT_BASE_DIR / "pdf"
            OutputPaths.SCREENSHOTS_DIR = OutputPaths.OUTPUT_BASE_DIR / "screenshots"
            OutputPaths.LOGS_DIR = OutputPaths.OUTPUT_BASE_DIR / "logs"
            OutputPaths.REPORTS_DIR = OutputPaths.OUTPUT_BASE_DIR / "reports"
        
        if cls.SCREENSHOTS_FOLDER:
            SeleniumPaths.SCREENSHOTS_DIR = ProjectPaths.ROOT_DIR / cls.SCREENSHOTS_FOLDER

def setup_all_directories():
    """
    Función de conveniencia para crear todas las carpetas necesarias
    """
    print("🚀 Configurando directorios del sistema...")
    
    # Aplicar preferencias del usuario primero
    UserPreferences.apply_preferences()
    
    # Crear directorios
    CSVPaths.create_directories()
    OutputPaths.create_directories()
    
    # Crear directorio de configuración
    ProjectPaths.CONFIG_DIR.mkdir(exist_ok=True)
    
    print("✅ Todos los directorios configurados correctamente")

# Función para mostrar la configuración actual
def show_current_configuration():
    """Muestra la configuración actual de rutas"""
    
    print("\n📋 CONFIGURACIÓN ACTUAL DE RUTAS:")
    print("=" * 50)
    
    print(f"📁 CSV Base: {CSVPaths.CSV_BASE_DIR}")
    print(f"📁 Shopify: {CSVPaths.SHOPIFY_DIR}")
    print(f"📁 FDA: {CSVPaths.FDA_DIR}")
    print(f"📁 Orders: {CSVPaths.ORDERS_DIR}")
    print(f"📁 Exports: {CSVPaths.EXPORTS_DIR}")
    
    print(f"\n📤 Output Base: {OutputPaths.OUTPUT_BASE_DIR}")
    print(f"📤 CSV Output: {OutputPaths.CSV_OUTPUT_DIR}")
    print(f"📤 Screenshots: {OutputPaths.SCREENSHOTS_DIR}")
    print(f"📤 Logs: {OutputPaths.LOGS_DIR}")
    
    print(f"\n🔧 ChromeDriver: {SeleniumPaths.CHROMEDRIVER_PATH}")
    print(f"🔧 Chrome Profile: {SeleniumPaths.CHROME_PROFILE_DIR}")

if __name__ == "__main__":
    # Mostrar configuración actual
    UserPreferences.apply_preferences()
    show_current_configuration()
    
    # Crear directorios
    setup_all_directories() 