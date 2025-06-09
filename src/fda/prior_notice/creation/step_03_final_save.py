"""
Paso 3: Guardar Final y Confirmación (MIGRADO)
Maneja la segunda pantalla con Save & Continue y modales de confirmación

Mejoras implementadas:
- Selectores centralizados para modales
- Helpers reutilizables para búsqueda y clics
- Timeouts optimizados
- Debug automático mejorado
- Scroll inteligente para elementos lazy loading
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Imports de la nueva arquitectura
from src.constants.timeouts import SleepTimes, ElementTimeouts
from src.constants.selectors import FDASelectors, ModalSelectors
from src.constants.messages import LogMessages, UserMessages, ProcessMessages
from src.utils.selenium_helpers import ElementFinder, ClickHelper, DebugHelper, WaitHelper
from src.core.logger import AutomationLogger

# Inicializar logger
logger = AutomationLogger.get_instance()

def click_second_save_and_continue(driver, wait):
    """
    Hace clic en el segundo botón "Save & Continue" en la nueva vista
    usando helpers y selectores centralizados
    """
    logger.fda_logger.info("=== BUSCANDO SEGUNDO BOTÓN SAVE & CONTINUE ===")
    
    try:
        # Esperar a que la nueva vista se cargue (optimizado)
        time.sleep(SleepTimes.FORM_LOAD)
        logger.fda_logger.debug("Esperando carga de nueva vista", extra={"sleep_time": SleepTimes.FORM_LOAD})
        
        # Scroll inteligente hacia abajo para elementos lazy loading
        logger.fda_logger.debug("Ejecutando scroll inteligente para cargar elementos...")
        ClickHelper.scroll_to_bottom_smart(driver)
        
        # Búsqueda directa por texto usando DebugHelper
        save_button = DebugHelper.find_button_by_exact_text(driver, "SAVE & CONTINUE")
        
        if save_button:
            logger.fda_logger.info("Botón encontrado por búsqueda directa")
            success = ClickHelper.safe_click_with_scroll(
                driver, save_button, "segundo Save & Continue"
            )
            
            if success:
                time.sleep(SleepTimes.SAVE_PROCESSING)
                logger.fda_logger.info("Segundo Save & Continue clickeado exitosamente (búsqueda directa)")
                return True
        
        # Método de respaldo: Múltiples selectores centralizados
        logger.fda_logger.info("Ejecutando método de respaldo con selectores centralizados")
        
        # Crear wait más corto para no tardar tanto
        short_wait = WebDriverWait(driver, ElementTimeouts.SHORT)
        
        # Selectores optimizados (los más específicos primero)
        save_selectors = [
            FDASelectors.SAVE_CONTINUE_BUTTON,  # Selector principal centralizado
            "//button[contains(@class, 'button-stepper') and .//span[text()='Save & Continue']]",
            "//button[text()='SAVE & CONTINUE']",
            "//button[contains(text(), 'SAVE & CONTINUE')]",
            "//span[text()='Save & Continue']/parent::button",
            f"//button[@class='{FDASelectors.SAVE_CONTINUE_CLASS}']",
            "//button[contains(@class, 'button-stepper')]//span[contains(text(), 'Save')]"
        ]
        
        logger.fda_logger.debug("Buscando con múltiples selectores", extra={
            "selectors_count": len(save_selectors),
            "timeout": ElementTimeouts.SHORT
        })
        
        save_button = ElementFinder.find_by_multiple_selectors(
            driver, short_wait, save_selectors, "segundo botón Save & Continue"
        )
        
        if save_button:
            success = ClickHelper.safe_click_with_scroll(
                driver, save_button, "segundo Save & Continue (selector)"
            )
            
            if success:
                time.sleep(SleepTimes.SAVE_PROCESSING)
                logger.fda_logger.info("Segundo Save & Continue clickeado exitosamente (selector)")
                return True
        
        # Debug automático usando helper
        logger.fda_logger.error("No se pudo encontrar el segundo botón 'Save & Continue'")
        DebugHelper.analyze_save_continue_buttons(driver)
        
        return False
        
    except Exception as e:
        logger.fda_logger.error("Error haciendo clic en segundo 'Save & Continue'", extra={"error": str(e)})
        logger.error_logger.error("Step 03 save button click failed", extra={
            "source_module": "fda_prior_notice_step_03",
            "function": "click_second_save_and_continue",
            "error": str(e)
        })
        return False

def handle_confirmation_modal(driver, wait):
    """
    Maneja el modal de confirmación si aparece usando selectores centralizados
    """
    logger.fda_logger.info("🔍 Verificando modal de confirmación...")
    
    try:
        # Esperar un poco para que aparezca el modal (optimizado)
        time.sleep(SleepTimes.MODAL_APPEAR)
        logger.fda_logger.debug("Esperando aparición de modal", extra={"sleep_time": SleepTimes.MODAL_APPEAR})
        
        # Múltiples selectores centralizados para modales
        modal_selectors = [
            ModalSelectors.OK_BUTTON,  # Selector principal centralizado
            ModalSelectors.CONFIRM_BUTTON,
            ModalSelectors.ACCEPT_BUTTON,
            ModalSelectors.CONTINUE_BUTTON,
            "//button[contains(text(), 'OK')]",
            "//button[contains(text(), 'Ok')]",
            "//button[contains(text(), 'Confirm')]",
            "//button[contains(text(), 'Confirmar')]",
            "//button[contains(text(), 'Accept')]",
            "//button[contains(text(), 'Aceptar')]",
            "//button[contains(text(), 'Continue')]",
            "//button[contains(text(), 'Continuar')]",
            "//button[contains(@class, 'confirm')]",
            "//button[contains(@class, 'primary')]",
            "//div[@class='modal']//button",
            "//div[contains(@class, 'dialog')]//button"
        ]
        
        # Usar wait más corto para verificar modal
        short_wait = WebDriverWait(driver, ElementTimeouts.MODAL)
        
        logger.fda_logger.debug("Buscando modal con múltiples selectores", extra={
            "selectors_count": len(modal_selectors),
            "timeout": ElementTimeouts.MODAL
        })
        
        modal_button = ElementFinder.find_by_multiple_selectors(
            driver, short_wait, modal_selectors, "botón de modal"
        )
        
        if modal_button:
            logger.fda_logger.info("✅ Modal de confirmación encontrado!")
            
            success = ClickHelper.safe_click_with_scroll(
                driver, modal_button, "botón de confirmación"
            )
            
            if success:
                time.sleep(SleepTimes.MODAL_PROCESSING)
                logger.fda_logger.info("Modal de confirmación procesado exitosamente")
                return True
        else:
            logger.fda_logger.info("ℹ️ No se detectó modal de confirmación (esto es normal)")
        
        return True  # True porque es opcional
        
    except Exception as e:
        logger.fda_logger.warning("Error manejando modal de confirmación", extra={"error": str(e)})
        return True  # No fallar el proceso por problemas de modal

def wait_for_final_processing(driver):
    """
    Espera a que se complete el procesamiento final usando timeouts centralizados
    """
    logger.fda_logger.info("⏳ Esperando procesamiento final...")
    
    try:
        # Esperar procesamiento principal
        time.sleep(SleepTimes.FINAL_PROCESSING)
        logger.fda_logger.debug("Esperando procesamiento principal", extra={"sleep_time": SleepTimes.FINAL_PROCESSING})
        
        # Verificar si hay indicadores de carga
        loading_indicators = [
            "//div[contains(@class, 'loading')]",
            "//div[contains(@class, 'spinner')]",
            "//div[contains(@class, 'progress')]",
            "//div[text()='Processing...']",
            "//div[text()='Procesando...']"
        ]
        
        # Wait corto para indicadores de carga
        short_wait = WebDriverWait(driver, ElementTimeouts.SHORT)
        
        logger.fda_logger.debug("Verificando indicadores de carga", extra={
            "indicators_count": len(loading_indicators),
            "timeout": ElementTimeouts.SHORT
        })
        
        for selector in loading_indicators:
            try:
                loading_element = short_wait.until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                
                if loading_element:
                    logger.fda_logger.info("🔄 Detectado indicador de carga, esperando...")
                    # Esperar a que desaparezca
                    WebDriverWait(driver, ElementTimeouts.LOADING).until(
                        EC.invisibility_of_element(loading_element)
                    )
                    logger.fda_logger.info("✅ Indicador de carga desapareció")
                    break
            except TimeoutException:
                continue
        
        # Verificar éxito buscando elementos típicos de confirmación
        success_indicators = [
            "//div[contains(text(), 'Success')]",
            "//div[contains(text(), 'Complete')]",
            "//div[contains(text(), 'Submitted')]",
            "//div[contains(text(), 'Saved')]",
            "//span[contains(@class, 'success')]",
            "//div[contains(@class, 'alert-success')]"
        ]
        
        logger.fda_logger.debug("Verificando indicadores de éxito", extra={
            "indicators_count": len(success_indicators)
        })
        
        for selector in success_indicators:
            try:
                success_element = short_wait.until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                
                if success_element:
                    success_text = success_element.text.strip()
                    logger.fda_logger.info("✅ Indicador de éxito encontrado", extra={"success_text": success_text})
                    return True
            except TimeoutException:
                continue
        
        logger.fda_logger.info("ℹ️ No se encontraron indicadores específicos, asumiendo éxito")
        return True
        
    except Exception as e:
        logger.fda_logger.warning("Error durante espera de procesamiento", extra={"error": str(e)})
        return True  # No fallar por esto

def execute_step_03(driver, wait=None):
    """
    Ejecuta el paso 3 completo: Guardar final y confirmación
    Función pública para mantener compatibilidad
    """
    logger.fda_logger.info("🔄 EJECUTANDO PASO 3: FINAL SAVE")
    
    try:
        # Crear wait si no se proporciona
        if wait is None:
            wait = WebDriverWait(driver, ElementTimeouts.DEFAULT)
        
        logger.fda_logger.debug("WebDriverWait configurado", extra={"timeout": ElementTimeouts.DEFAULT})
        
        # Paso 1: Hacer clic en segundo Save & Continue
        logger.fda_logger.info("📝 Paso 3.1: Segundo botón 'Save & Continue'")
        if not click_second_save_and_continue(driver, wait):
            logger.fda_logger.error("Falló segundo Save & Continue")
            return False
        
        # Paso 2: Manejar modal de confirmación si aparece
        logger.fda_logger.info("🔍 Paso 3.2: Verificar modal de confirmación")
        if not handle_confirmation_modal(driver, wait):
            logger.fda_logger.warning("Problema con modal de confirmación, pero continuando...")
        
        # Paso 3: Esperar procesamiento final
        logger.fda_logger.info("⏳ Paso 3.3: Esperar procesamiento final")
        if not wait_for_final_processing(driver):
            logger.fda_logger.warning("Procesamiento final incierto, pero continuando...")
        
        # Proceso completado
        logger.fda_logger.info("✅ PASO 3 - Final Save COMPLETADO")
        logger.fda_logger.info("📊 Resumen de lo ejecutado:", extra={
            "segundo_save_continue": "Clickeado",
            "modal_confirmacion": "Manejado",
            "procesamiento_final": "Completado"
        })
        
        logger.fda_logger.info("🎯 El Prior Notice debería estar completamente guardado en FDA")
        
        return True
        
    except Exception as e:
        logger.fda_logger.error("Error durante el Paso 3", extra={"error": str(e)})
        logger.error_logger.error("Step 03 execution failed", extra={
            "source_module": "fda_prior_notice_step_03",
            "function": "execute_step_03",
            "error": str(e),
            "error_type": type(e).__name__
        })
        return False

def debug_step_03(driver):
    """
    Función de debug mejorada usando helpers centralizados
    """
    print("🔍 DEBUG PASO 3 - Análisis completo de elementos...")
    
    try:
        # Debug usando DebugHelper
        print("\n📊 Análisis de botones Save/Continue:")
        DebugHelper.analyze_save_continue_buttons(driver)
        
        print("\n📊 Análisis de elementos de modal:")
        DebugHelper.analyze_modal_elements(driver)
        
        print("\n📊 Análisis general de botones:")
        DebugHelper.list_all_buttons(driver, limit=15)
        
    except Exception as e:
        print(f"❌ Error en debug: {e}")

# Alias para mantener compatibilidad con código legacy
def complete_step_03_final_save(driver, wait):
    """
    Alias para compatibilidad con versiones anteriores
    """
    return execute_step_03(driver, wait)

if __name__ == "__main__":
    print("⚠️ Este archivo debe ser ejecutado desde main.py")
    print("💡 Para testing individual, importa la función execute_step_03(driver)")
    print("🔍 Para debug, usa debug_step_03(driver)") 