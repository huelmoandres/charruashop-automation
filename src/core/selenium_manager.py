"""
Manager central para Selenium WebDriver
Centraliza la configuración y gestión del driver de Selenium
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import os
from typing import Optional

from ..constants.timeouts import DEFAULT_WAIT

class SeleniumManager:
    """
    Clase central para gestionar el driver de Selenium
    Proporciona configuración estándar y métodos de utilidad
    """
    
    def __init__(self, headless: bool = False, user_data_dir: Optional[str] = None):
        """
        Inicializa el manager de Selenium
        
        Args:
            headless: Si ejecutar Chrome en modo headless
            user_data_dir: Directorio de datos de usuario de Chrome
        """
        self.headless = headless
        self.user_data_dir = user_data_dir or self._get_default_user_data_dir()
        self.driver = None
        self.wait = None
    
    def _get_default_user_data_dir(self) -> str:
        """Obtiene el directorio de datos de usuario por defecto"""
        home_dir = os.path.expanduser("~")
        return os.path.join(home_dir, "Library", "Application Support", "Google", "Chrome", "selenium-profile")
    
    def _setup_chrome_options(self) -> Options:
        """
        Configura las opciones de Chrome
        
        Returns:
            Options configuradas para Chrome
        """
        options = Options()
        
        # Configuraciones básicas
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        
        # User data directory para mantener sesión
        if self.user_data_dir:
            options.add_argument(f"--user-data-dir={self.user_data_dir}")
        
        # Modo headless si se especifica
        if self.headless:
            options.add_argument("--headless")
        
        # Configuraciones de ventana
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        
        # Configuraciones adicionales para estabilidad
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Deshabilitar notificaciones
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.images": 2  # Opcional: deshabilitar imágenes para velocidad
        }
        options.add_experimental_option("prefs", prefs)
        
        return options
    
    def start_driver(self, driver_path: str = "./drivers/chromedriver") -> webdriver.Chrome:
        """
        Inicia el driver de Chrome con la configuración establecida
        
        Args:
            driver_path: Ruta al ejecutable de ChromeDriver
            
        Returns:
            Driver de Chrome configurado
            
        Raises:
            Exception: Si no se puede iniciar el driver
        """
        try:
            # Verificar que el driver existe
            if not os.path.exists(driver_path):
                raise FileNotFoundError(f"ChromeDriver no encontrado en: {driver_path}")
            
            # Configurar el servicio
            service = Service(driver_path)
            
            # Configurar opciones
            options = self._setup_chrome_options()
            
            # Crear el driver
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Configurar timeouts implícitos
            self.driver.implicitly_wait(DEFAULT_WAIT)
            
            # Crear WebDriverWait
            self.wait = WebDriverWait(self.driver, DEFAULT_WAIT)
            
            print(f"✅ Driver de Chrome iniciado exitosamente")
            print(f"   📁 User data dir: {self.user_data_dir}")
            print(f"   🖥️ Headless: {self.headless}")
            
            return self.driver
            
        except Exception as e:
            print(f"❌ Error iniciando driver de Chrome: {e}")
            raise
    
    def get_wait(self, timeout: Optional[int] = None) -> WebDriverWait:
        """
        Obtiene una instancia de WebDriverWait
        
        Args:
            timeout: Timeout personalizado (usa el default si no se especifica)
            
        Returns:
            WebDriverWait instance
        """
        if not self.driver:
            raise RuntimeError("Driver no iniciado. Llama a start_driver() primero")
        
        if timeout:
            return WebDriverWait(self.driver, timeout)
        
        return self.wait
    
    def close_driver(self):
        """Cierra el driver de forma segura"""
        if self.driver:
            try:
                self.driver.quit()
                print("🔧 Driver cerrado exitosamente")
            except Exception as e:
                print(f"⚠️ Error cerrando driver: {e}")
            finally:
                self.driver = None
                self.wait = None
    
    def take_screenshot(self, filename: str = None) -> str:
        """
        Toma una captura de pantalla
        
        Args:
            filename: Nombre del archivo (opcional)
            
        Returns:
            Ruta del archivo guardado
        """
        if not self.driver:
            raise RuntimeError("Driver no iniciado")
        
        if not filename:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        # Crear directorio si no existe
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        
        filepath = os.path.join(screenshots_dir, filename)
        self.driver.save_screenshot(filepath)
        
        print(f"📸 Captura guardada: {filepath}")
        return filepath
    
    def navigate_to(self, url: str):
        """
        Navega a una URL
        
        Args:
            url: URL de destino
        """
        if not self.driver:
            raise RuntimeError("Driver no iniciado")
        
        print(f"🔍 Navegando a: {url}")
        self.driver.get(url)
    
    def get_current_url(self) -> str:
        """Obtiene la URL actual"""
        if not self.driver:
            raise RuntimeError("Driver no iniciado")
        
        return self.driver.current_url
    
    def get_page_title(self) -> str:
        """Obtiene el título de la página actual"""
        if not self.driver:
            raise RuntimeError("Driver no iniciado")
        
        return self.driver.title
    
    def __enter__(self):
        """Soporte para context manager"""
        self.start_driver()
        return self.driver
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra el driver automáticamente al salir del context"""
        self.close_driver()

# Función de conveniencia para compatibilidad con código existente
def setup_chrome_driver(headless: bool = False, user_data_dir: Optional[str] = None) -> webdriver.Chrome:
    """
    Función de conveniencia para crear un driver de Chrome
    
    Args:
        headless: Si ejecutar en modo headless
        user_data_dir: Directorio de datos de usuario
        
    Returns:
        Driver de Chrome configurado
    """
    manager = SeleniumManager(headless=headless, user_data_dir=user_data_dir)
    return manager.start_driver()

def setup_wait(driver: webdriver.Chrome, timeout: int = DEFAULT_WAIT) -> WebDriverWait:
    """
    Función de conveniencia para crear WebDriverWait
    
    Args:
        driver: Driver de Chrome
        timeout: Timeout en segundos
        
    Returns:
        WebDriverWait instance
    """
    return WebDriverWait(driver, timeout) 