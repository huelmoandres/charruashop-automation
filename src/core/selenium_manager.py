"""
Manager central para Selenium WebDriver
Centraliza la configuración y gestión del driver de Selenium
Ahora integra logging avanzado y screenshots automáticos
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException
import os
import time
from typing import Optional

from ..constants.timeouts import DEFAULT_WAIT
from .logger import get_logger
from ..utils.screenshot_utils import create_screenshot_manager

class SeleniumManager:
    """
    Clase central para gestionar el driver de Selenium
    Proporciona configuración estándar, métodos de utilidad y logging integrado
    """
    
    def __init__(self, headless: bool = False, user_data_dir: Optional[str] = None):
        """
        Inicializa el manager de Selenium con logging integrado
        
        Args:
            headless: Si ejecutar Chrome en modo headless
            user_data_dir: Directorio de datos de usuario de Chrome
        """
        self.headless = headless
        self.user_data_dir = user_data_dir or self._get_default_user_data_dir()
        self.driver = None
        self.wait = None
        
        # Inicializar logger y screenshot manager
        self.logger = get_logger()
        self.screenshot_manager = None
        
        self.logger.info("🚀 SeleniumManager inicializado", module='selenium')
    
    def _get_default_user_data_dir(self) -> str:
        """Obtiene el directorio de datos de usuario por defecto"""
        home_dir = os.path.expanduser("~")
        return os.path.join(home_dir, "Library", "Application Support", "Google", "Chrome", "selenium-profile")
    
    def _setup_chrome_options(self) -> Options:
        """
        Configura las opciones de Chrome con logging detallado
        
        Returns:
            Options configuradas para Chrome
        """
        self.logger.debug("🔧 Configurando opciones de Chrome", module='selenium')
        
        options = Options()
        
        # Configuraciones básicas
        basic_args = [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-web-security",
            "--allow-running-insecure-content"
        ]
        
        for arg in basic_args:
            options.add_argument(arg)
            self.logger.debug(f"   + Argumento: {arg}", module='selenium')
        
        # User data directory para mantener sesión
        if self.user_data_dir:
            options.add_argument(f"--user-data-dir={self.user_data_dir}")
            self.logger.debug(f"   + User data dir: {self.user_data_dir}", module='selenium')
        
        # Modo headless si se especifica
        if self.headless:
            options.add_argument("--headless")
            self.logger.info("   🕶️ Modo headless habilitado", module='selenium')
        
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
        
        self.logger.info("✅ Opciones de Chrome configuradas", module='selenium')
        return options
    
    def start_driver(self, driver_path: str = "./drivers/chromedriver") -> webdriver.Chrome:
        """
        Inicia el driver de Chrome con logging completo y screenshots automáticos
        
        Args:
            driver_path: Ruta al ejecutable de ChromeDriver
            
        Returns:
            Driver de Chrome configurado
            
        Raises:
            Exception: Si no se puede iniciar el driver
        """
        try:
            self.logger.info("🔄 Iniciando driver de Chrome...", module='selenium')
            
            # Verificar que el driver existe
            if not os.path.exists(driver_path):
                error_msg = f"ChromeDriver no encontrado en: {driver_path}"
                self.logger.error(error_msg, module='selenium')
                raise FileNotFoundError(error_msg)
            
            self.logger.debug(f"✅ ChromeDriver encontrado en: {driver_path}", module='selenium')
            
            # Configurar el servicio
            service = Service(driver_path)
            self.logger.debug("🔧 Servicio de Chrome configurado", module='selenium')
            
            # Configurar opciones
            options = self._setup_chrome_options()
            
            # Crear el driver
            start_time = time.time()
            self.driver = webdriver.Chrome(service=service, options=options)
            startup_time = time.time() - start_time
            
            # Configurar timeouts implícitos
            self.driver.implicitly_wait(DEFAULT_WAIT)
            
            # Crear WebDriverWait
            self.wait = WebDriverWait(self.driver, DEFAULT_WAIT)
            
            # Inicializar screenshot manager
            self.screenshot_manager = create_screenshot_manager(self.logger)
            
            # Logs de éxito
            self.logger.info(f"✅ Driver de Chrome iniciado exitosamente ({startup_time:.2f}s)", module='selenium')
            self.logger.info(f"   📁 User data dir: {self.user_data_dir}", module='selenium')
            self.logger.info(f"   🖥️ Headless: {self.headless}", module='selenium')
            self.logger.info(f"   ⏱️ Timeout implícito: {DEFAULT_WAIT}s", module='selenium')
            
            print(f"✅ Driver de Chrome iniciado exitosamente")
            print(f"   📁 User data dir: {self.user_data_dir}")
            print(f"   🖥️ Headless: {self.headless}")
            
            # Screenshot inicial opcional
            if self.screenshot_manager:
                try:
                    # Navegar a about:blank para screenshot inicial
                    self.driver.get("about:blank")
                    self.screenshot_manager.capture_screenshot(self.driver, "driver_startup", "INFO")
                except:
                    pass  # No fallar por screenshot inicial
            
            return self.driver
            
        except Exception as e:
            error_msg = f"Error iniciando driver de Chrome: {e}"
            self.logger.error(error_msg, module='selenium', exception=e)
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
        """Cierra el driver de forma segura con logging y resúmenes"""
        if self.driver:
            try:
                # Screenshot final
                if self.screenshot_manager:
                    try:
                        self.screenshot_manager.capture_screenshot(self.driver, "session_end", "INFO")
                    except:
                        pass
                
                # Cerrar driver
                self.driver.quit()
                self.logger.info("🔧 Driver cerrado exitosamente", module='selenium')
                print("🔧 Driver cerrado exitosamente")
                
                # Log de summary de screenshots
                if self.screenshot_manager:
                    summary = self.screenshot_manager.get_screenshot_summary()
                    self.logger.info(f"📸 Screenshots capturados: {summary.get('total_screenshots', 0)}", module='selenium')
                
            except Exception as e:
                self.logger.error(f"⚠️ Error cerrando driver: {e}", module='selenium', exception=e)
                print(f"⚠️ Error cerrando driver: {e}")
            finally:
                self.driver = None
                self.wait = None
                self.screenshot_manager = None
    
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
    
    def navigate_to(self, url: str, take_screenshot: bool = True):
        """
        Navega a una URL con logging y screenshots automáticos
        
        Args:
            url: URL de destino
            take_screenshot: Si tomar screenshot después de navegar
        """
        if not self.driver:
            raise RuntimeError("Driver no iniciado")
        
        try:
            self.logger.info(f"🌐 Navegando a: {url}", module='selenium')
            start_time = time.time()
            
            self.driver.get(url)
            
            navigation_time = time.time() - start_time
            self.logger.info(f"✅ Navegación completada ({navigation_time:.2f}s)", module='selenium')
            
            # Información adicional de la página
            try:
                page_title = self.driver.title
                current_url = self.driver.current_url
                self.logger.debug(f"   📄 Título: {page_title}", module='selenium')
                self.logger.debug(f"   🔗 URL final: {current_url}", module='selenium')
            except:
                pass
            
            # Screenshot automático
            if take_screenshot and self.screenshot_manager:
                try:
                    clean_url = url.replace('https://', '').replace('http://', '').replace('/', '_')
                    self.screenshot_manager.capture_screenshot(self.driver, f"navigation_{clean_url}", "INFO")
                except:
                    self.logger.warning("⚠️ No se pudo capturar screenshot de navegación", module='selenium')
            
            print(f"🔍 Navegando a: {url}")
            
        except Exception as e:
            self.logger.error(f"❌ Error navegando a {url}: {e}", module='selenium', exception=e)
            
            # Screenshot de error
            if self.screenshot_manager:
                try:
                    self.screenshot_manager.capture_error_screenshot(self.driver, f"navigation_error_{url}", e)
                except:
                    pass
            
            raise
    
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