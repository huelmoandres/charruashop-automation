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

def select_copy_with_no_food_articles(driver, wait):
    """
    Después de copiar un prior notice, selecciona la opción COPY WITH NO FOOD ARTICLES
    usando helpers y selectores centralizados
    """
    try:
        print(LogMessages.SEARCHING_ELEMENT.format(element="botón 'COPY WITH NO FOOD ARTICLES'"))
        
        # Esperar a que la página de opciones de copia se cargue (optimizado)
        time.sleep(SleepTimes.FORM_LOAD)
        
        # Múltiples selectores para mayor robustez
        copy_selectors = [
            FDASelectors.COPY_NO_FOOD_BUTTON,  # Selector principal centralizado
            "//button[@class='button button-stepper' and contains(text(), 'COPY WITH NO FOOD ARTICLES')]",
            "//button[contains(text(), 'COPY WITH NO FOOD') or contains(text(), 'NO FOOD ARTICLES')]",
            "//button[contains(@class, 'button-stepper') and contains(text(), 'NO FOOD')]"
        ]
        
        # Usar ElementFinder para búsqueda robusta
        copy_button = ElementFinder.find_by_multiple_selectors(
            driver, wait, copy_selectors, "botón COPY WITH NO FOOD ARTICLES"
        )
        
        if not copy_button:
            # Debug automático usando helper
            print("🔍 Analizando botones disponibles...")
            DebugHelper.list_all_buttons(driver)
            return False
        
        print(LogMessages.ELEMENT_FOUND.format(element="botón 'COPY WITH NO FOOD ARTICLES'"))
        
        # Usar ClickHelper para clic seguro con scroll automático
        success = ClickHelper.safe_click_with_scroll(
            driver, copy_button, "COPY WITH NO FOOD ARTICLES"
        )
        
        if success:
            # Esperar procesamiento con timeout optimizado
            time.sleep(SleepTimes.SAVE_PROCESSING)
            print(LogMessages.PROCESS_COMPLETED.format(process="selección de copia"))
            return True
        else:
            return False
        
    except Exception as e:
        print(f"❌ Error buscando botón 'COPY WITH NO FOOD ARTICLES': {e}")
        
        # Método de fallback mejorado
        return fallback_copy_selection(driver, wait)

def fallback_copy_selection(driver, wait):
    """
    Método de fallback usando análisis inteligente de botones
    """
    try:
        print("🔄 Ejecutando método de fallback...")
        
        # Usar DebugHelper para análisis completo
        buttons_info = DebugHelper.analyze_buttons_with_text(driver, "food")
        
        if not buttons_info:
            print("❌ No se encontraron botones relacionados con 'food'")
            return False
        
        # Buscar el botón más adecuado
        target_button = None
        for button_info in buttons_info:
            text = button_info['text'].upper()
            if "NO FOOD" in text and "COPY" in text:
                target_button = button_info['element']
                print(f"✅ Botón objetivo encontrado: '{button_info['text']}'")
                break
        
        if target_button:
            success = ClickHelper.safe_click_with_scroll(
                driver, target_button, "botón de copia (fallback)"
            )
            
            if success:
                time.sleep(SleepTimes.SAVE_PROCESSING)
                print(LogMessages.PROCESS_COMPLETED.format(process="selección de copia (fallback)"))
                return True
        
        print("❌ No se pudo encontrar botón adecuado en fallback")
        return False
        
    except Exception as e:
        print(f"❌ Error en método de fallback: {e}")
        return False

def execute_step_01(driver, wait=None):
    """
    Ejecuta el paso 1 completo: Selección del tipo de copia
    Función pública para mantener compatibilidad
    """
    try:
        print(f"\n{ProcessMessages.STEP_INDICATOR.format(step=1, description='Copy Selection')}")
        print("=" * 50)
        
        # Crear wait si no se proporciona
        if wait is None:
            wait = WebDriverWait(driver, ElementTimeouts.DEFAULT)
        
        if select_copy_with_no_food_articles(driver, wait):
            print(LogMessages.PROCESS_COMPLETED.format(process="PASO 1 - Copy Selection"))
            return True
        else:
            print(LogMessages.PROCESS_FAILED.format(process="PASO 1 - Copy Selection"))
            return False
            
    except Exception as e:
        print(f"❌ Error durante el Paso 1: {e}")
        return False

# Alias para mantener compatibilidad con código legacy
def complete_step_01_copy_selection(driver, wait):
    """
    Alias para compatibilidad con versiones anteriores
    """
    return execute_step_01(driver, wait) 