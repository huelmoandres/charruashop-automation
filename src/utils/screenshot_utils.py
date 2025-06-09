"""
Utilidades para captura automática de screenshots
Integrado con el sistema de logging para debugging de Selenium
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Union
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from src.core.logger import AutomationLogger

class ScreenshotManager:
    """
    Manejador de screenshots automáticos para debugging de Selenium
    """
    
    def __init__(self, logger=None):
        """
        Inicializa el manejador de screenshots
        
        Args:
            logger: Instancia del AutomationLogger (deprecated, se usa AutomationLogger directamente)
        """
        self.logger = AutomationLogger.get_instance()
        self.screenshots_dir = Path("logs/screenshots")
        self._ensure_screenshot_directory()
        
        self.logger.selenium_logger.info("=== SCREENSHOT MANAGER INICIALIZADO ===", extra={
            "screenshots_dir": str(self.screenshots_dir)
        })
    
    def _ensure_screenshot_directory(self):
        """Crea el directorio de screenshots si no existe"""
        today = datetime.now().strftime('%Y-%m-%d')
        self.daily_dir = self.screenshots_dir / today
        self.daily_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.selenium_logger.debug("Directorio de screenshots configurado", extra={
            "daily_dir": str(self.daily_dir),
            "date": today
        })
    
    def capture_screenshot(self, 
                          driver: webdriver.Chrome, 
                          context: str = "screenshot",
                          level: str = "INFO") -> Optional[str]:
        """
        Captura un screenshot del estado actual del navegador
        
        Args:
            driver: Instancia del WebDriver
            context: Contexto/descripción del screenshot
            level: Nivel de log (INFO, ERROR, DEBUG)
            
        Returns:
            Ruta del archivo de screenshot o None si falló
        """
        self.logger.selenium_logger.debug("Capturando screenshot", extra={
            "context": context,
            "level": level
        })
        
        try:
            # Generar nombre único del archivo
            timestamp = datetime.now().strftime('%H%M%S')
            clean_context = "".join(c for c in context if c.isalnum() or c in (' ', '-', '_')).strip()
            clean_context = clean_context.replace(' ', '_')
            
            filename = f"{level.lower()}_{clean_context}_{timestamp}.png"
            filepath = self.daily_dir / filename
            
            # Capturar screenshot
            driver.save_screenshot(str(filepath))
            
            screenshot_info = {
                "screenshot_filename": filename,
                "screenshot_filepath": str(filepath),
                "screenshot_context": context,
                "screenshot_level": level,
                "screenshot_timestamp": timestamp
            }
            
            # Log del screenshot
            self.logger.selenium_logger.info("Screenshot capturado exitosamente", extra=screenshot_info)
            
            if level == "ERROR":
                self.logger.selenium_logger.error("Screenshot de error guardado", extra=screenshot_info)
                
            return str(filepath)
            
        except WebDriverException as e:
            self.logger.selenium_logger.error("Error WebDriver capturando screenshot", extra={
                "context": context,
                "error": str(e)
            })
            self.logger.error_logger.error("WebDriver screenshot error", extra={
                "source_module": "utils_screenshot",
                "function": "capture_screenshot",
                "context": context,
                "error": str(e)
            })
            return None
        except Exception as e:
            self.logger.selenium_logger.error("Error inesperado capturando screenshot", extra={
                "context": context,
                "error": str(e)
            })
            self.logger.error_logger.error("Unexpected screenshot error", extra={
                "source_module": "utils_screenshot",
                "function": "capture_screenshot",
                "context": context,
                "error": str(e)
            })
            return None
    
    def capture_error_screenshot(self, 
                                driver: webdriver.Chrome, 
                                error_context: str,
                                exception: Optional[Exception] = None) -> Optional[str]:
        """
        Captura un screenshot específicamente para errores
        
        Args:
            driver: Instancia del WebDriver
            error_context: Descripción del error
            exception: Excepción que causó el error
            
        Returns:
            Ruta del archivo de screenshot o None si falló
        """
        self.logger.selenium_logger.error("=== CAPTURANDO SCREENSHOT DE ERROR ===", extra={
            "error_context": error_context,
            "exception": str(exception) if exception else None
        })
        
        try:
            # Información adicional del estado del navegador
            current_url = "unknown"
            page_title = "unknown"
            
            try:
                current_url = driver.current_url
                page_title = driver.title[:50] if driver.title else "no_title"
            except:
                pass
            
            browser_state = {
                "current_url": current_url,
                "page_title": page_title
            }
            
            self.logger.selenium_logger.debug("Estado del navegador en error", extra=browser_state)
            
            # Contexto detallado
            detailed_context = f"error_{error_context}_url_{current_url.split('/')[-1]}"
            screenshot_path = self.capture_screenshot(driver, detailed_context, "ERROR")
            
            # Log detallado del error
            if screenshot_path:
                error_details = {
                    "screenshot": screenshot_path,
                    "current_url": current_url,
                    "page_title": page_title,
                    "error_context": error_context,
                    "exception": str(exception) if exception else None
                }
                
                self.logger.selenium_logger.error("Screenshot de error con detalles", extra=error_details)
            
            return screenshot_path
            
        except Exception as e:
            self.logger.selenium_logger.critical("Fallo crítico capturando screenshot de error", extra={
                "error_context": error_context,
                "error": str(e)
            })
            self.logger.error_logger.critical("Critical screenshot failure", extra={
                "source_module": "utils_screenshot",
                "function": "capture_error_screenshot",
                "error_context": error_context,
                "error": str(e)
            })
            return None
    
    def capture_step_screenshot(self, 
                               driver: webdriver.Chrome, 
                               step_name: str,
                               step_number: Optional[int] = None) -> Optional[str]:
        """
        Captura un screenshot para documentar un paso del proceso
        
        Args:
            driver: Instancia del WebDriver
            step_name: Nombre del paso
            step_number: Número del paso (opcional)
            
        Returns:
            Ruta del archivo de screenshot o None si falló
        """
        step_context = f"step_{step_number}_{step_name}" if step_number else f"step_{step_name}"
        
        self.logger.selenium_logger.info("Capturando screenshot de paso", extra={
            "step_name": step_name,
            "step_number": step_number,
            "step_context": step_context
        })
        
        return self.capture_screenshot(driver, step_context, "INFO")
    
    def capture_success_screenshot(self, 
                                  driver: webdriver.Chrome, 
                                  success_context: str) -> Optional[str]:
        """
        Captura un screenshot para documentar un éxito/completación
        
        Args:
            driver: Instancia del WebDriver
            success_context: Descripción del éxito
            
        Returns:
            Ruta del archivo de screenshot o None si falló
        """
        self.logger.selenium_logger.info("Capturando screenshot de éxito", extra={
            "success_context": success_context
        })
        
        return self.capture_screenshot(driver, f"success_{success_context}", "INFO")
    
    def get_screenshot_summary(self) -> dict:
        """
        Obtiene un resumen de los screenshots capturados en la sesión actual
        
        Returns:
            Diccionario con estadísticas de screenshots
        """
        self.logger.selenium_logger.debug("Generando resumen de screenshots")
        
        try:
            screenshots = list(self.daily_dir.glob("*.png"))
            
            # Categorizar por tipo
            by_type = {
                'error': len([s for s in screenshots if 'error_' in s.name]),
                'step': len([s for s in screenshots if 'step_' in s.name]),
                'success': len([s for s in screenshots if 'success_' in s.name]),
                'info': len([s for s in screenshots if 'info_' in s.name]),
                'other': 0
            }
            
            by_type['other'] = len(screenshots) - sum(by_type.values())
            
            summary = {
                'total_screenshots': len(screenshots),
                'by_type': by_type,
                'screenshots_directory': str(self.daily_dir),
                'latest_screenshots': [s.name for s in sorted(screenshots, key=lambda x: x.stat().st_mtime)[-5:]]
            }
            
            self.logger.selenium_logger.info("Resumen de screenshots generado", extra=summary)
            return summary
            
        except Exception as e:
            self.logger.selenium_logger.error("Error generando resumen de screenshots", extra={
                "error": str(e)
            })
            self.logger.error_logger.error("Screenshot summary failed", extra={
                "source_module": "utils_screenshot",
                "function": "get_screenshot_summary",
                "error": str(e)
            })
            return {'error': str(e)}

# Función de conveniencia para inicializar
def create_screenshot_manager(logger=None) -> ScreenshotManager:
    """
    Crea una instancia del ScreenshotManager
    
    Args:
        logger: Instancia del logger (deprecated, se ignora)
        
    Returns:
        Instancia de ScreenshotManager
    """
    logger_instance = AutomationLogger.get_instance()
    logger_instance.selenium_logger.info("Creando nuevo ScreenshotManager")
    return ScreenshotManager(logger)

# Decorador para captura automática de screenshots en errores
def auto_screenshot_on_error(screenshot_manager: ScreenshotManager, context: str = "function_error"):
    """
    Decorador que captura automáticamente un screenshot si la función falla
    
    Args:
        screenshot_manager: Instancia del ScreenshotManager
        context: Contexto para el screenshot
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Buscar el driver en los argumentos
                driver = None
                for arg in args:
                    if isinstance(arg, webdriver.Chrome):
                        driver = arg
                        break
                
                if driver:
                    screenshot_manager.capture_error_screenshot(
                        driver, 
                        f"{func.__name__}_{context}",
                        e
                    )
                
                raise  # Re-raise la excepción original
        
        return wrapper
    return decorator 