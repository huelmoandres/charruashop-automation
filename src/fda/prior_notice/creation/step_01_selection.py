"""
Paso 1: Copy Selection (MIGRADO)
Selecciona la opción "COPY WITH NO FOOD ARTICLES" usando arquitectura moderna

Mejoras implementadas:
- Selectores centralizados
- Helpers reutilizables para búsqueda y clics
- Timeouts optimizados
- Mensajes consistentes
- Debug automático mejorado
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

# Imports de la nueva arquitectura
from src.constants.timeouts import SleepTimes, ElementTimeouts
from src.constants.selectors import FDASelectors
from src.constants.messages import LogMessages, UserMessages, ProcessMessages
from src.utils.selenium_helpers import ElementFinder, ClickHelper, DebugHelper, WaitHelper
from src.core.logger import AutomationLogger

# Inicializar logger
logger = AutomationLogger.get_instance()

def select_no_food_articles(driver, wait):
    """
    Selecciona la opción "NO FOOD ARTICLES" 
    usando helpers y selectores centralizados
    """
    logger.fda_logger.info("=== INICIANDO SELECCIÓN NO FOOD ARTICLES ===")
    
    try:
        logger.fda_logger.debug("Buscando botón 'NO FOOD ARTICLES'")
        
        # Esperar a que la página de opciones se cargue (optimizado)
        time.sleep(SleepTimes.FORM_LOAD)
        
        # Múltiples selectores para mayor robustez
        no_food_selectors = [
            FDASelectors.COPY_NO_FOOD_BUTTON,  # Selector principal centralizado
            "//button[@class='button button-stepper' and contains(text(), 'COPY WITH NO FOOD ARTICLES')]",
            "//button[contains(text(), 'COPY WITH NO FOOD') or contains(text(), 'NO FOOD ARTICLES')]",
            "//button[contains(@class, 'button-stepper') and contains(text(), 'NO FOOD')]"
        ]
        
        logger.fda_logger.debug("Ejecutando búsqueda con múltiples selectores", extra={
            "selectors_count": len(no_food_selectors),
            "primary_selector": FDASelectors.COPY_NO_FOOD_BUTTON
        })
        
        # Usar ElementFinder para búsqueda robusta
        no_food_button = ElementFinder.find_by_multiple_selectors(
            driver, wait, no_food_selectors, "botón NO FOOD ARTICLES"
        )
        
        if not no_food_button:
            logger.fda_logger.warning("Botón NO FOOD ARTICLES no encontrado")
            # Debug automático usando helper
            logger.fda_logger.debug("Analizando botones disponibles...")
            DebugHelper.list_all_buttons(driver)
            return False
        
        logger.fda_logger.info("Botón 'NO FOOD ARTICLES' encontrado exitosamente")
        
        # Usar ClickHelper para clic seguro con scroll automático
        success = ClickHelper.safe_click_with_scroll(
            driver, no_food_button, "NO FOOD ARTICLES"
        )
        
        if success:
            # Esperar procesamiento con timeout optimizado
            time.sleep(SleepTimes.SAVE_PROCESSING)
            logger.fda_logger.info("=== SELECCIÓN NO FOOD ARTICLES COMPLETADA EXITOSAMENTE ===")
            return True
        else:
            logger.fda_logger.error("Fallo en clic del botón NO FOOD ARTICLES")
            return False
        
    except Exception as e:
        logger.fda_logger.error("Error buscando botón 'NO FOOD ARTICLES'", extra={"error": str(e)})
        logger.error_logger.error("Step 01 selection failed", extra={
            "source_module": "fda_prior_notice_step_01",
            "function": "select_no_food_articles", 
            "error": str(e),
            "error_type": type(e).__name__
        })
        
        # Método de fallback mejorado
        return fallback_selection(driver, wait)

def fallback_selection(driver, wait):
    """
    Método de fallback usando análisis inteligente de botones
    """
    logger.fda_logger.info("Ejecutando método de fallback para selección")
    
    try:
        # Usar DebugHelper para análisis completo
        buttons_info = DebugHelper.analyze_buttons_with_text(driver, "food")
        
        if not buttons_info:
            logger.fda_logger.error("No se encontraron botones relacionados con 'food'")
            return False
        
        logger.fda_logger.debug("Botones encontrados para análisis", extra={
            "buttons_count": len(buttons_info),
            "search_term": "food"
        })
        
        # Buscar el botón más adecuado
        target_button = None
        for button_info in buttons_info:
            text = button_info['text'].upper()
            if "NO FOOD" in text:
                target_button = button_info['element']
                logger.fda_logger.info("Botón objetivo encontrado en fallback", extra={
                    "button_text": button_info['text']
                })
                break
        
        if target_button:
            success = ClickHelper.safe_click_with_scroll(
                driver, target_button, "botón no food (fallback)"
            )
            
            if success:
                time.sleep(SleepTimes.SAVE_PROCESSING)
                logger.fda_logger.info("Selección completada usando fallback")
                return True
        
        logger.fda_logger.error("No se pudo encontrar botón adecuado en fallback")
        return False
        
    except Exception as e:
        logger.fda_logger.error("Error en método de fallback", extra={"error": str(e)})
        logger.error_logger.error("Step 01 fallback failed", extra={
            "source_module": "fda_prior_notice_step_01",
            "function": "fallback_selection",
            "error": str(e)
        })
        return False

def execute_step_01(driver, wait=None):
    """
    Ejecuta el paso 1 completo: Selección del tipo de opción
    Función pública para mantener compatibilidad
    """
    logger.fda_logger.info("🔄 EJECUTANDO PASO 1: SELECTION")
    
    try:
        # Crear wait si no se proporciona
        if wait is None:
            wait = WebDriverWait(driver, ElementTimeouts.DEFAULT)
        
        logger.fda_logger.debug("WebDriverWait configurado", extra={
            "timeout": ElementTimeouts.DEFAULT
        })
        
        if select_no_food_articles(driver, wait):
            logger.fda_logger.info("✅ PASO 1 - Selection COMPLETADO")
            return True
        else:
            logger.fda_logger.error("❌ PASO 1 - Selection FALLÓ")
            return False
            
    except Exception as e:
        logger.fda_logger.error("Error durante el Paso 1", extra={"error": str(e)})
        logger.error_logger.error("Step 01 execution failed", extra={
            "source_module": "fda_prior_notice_step_01",
            "function": "execute_step_01",
            "error": str(e)
        })
        return False

# Alias para mantener compatibilidad con código legacy
def complete_step_01_selection(driver, wait):
    """
    Alias para compatibilidad con versiones anteriores
    """
    logger.fda_logger.debug("Ejecutando step 01 via función legacy")
    return execute_step_01(driver, wait)

 