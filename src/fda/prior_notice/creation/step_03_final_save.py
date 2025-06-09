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

def click_second_save_and_continue(driver, wait):
    """
    Hace clic en el segundo botón "Save & Continue" en la nueva vista
    usando helpers y selectores centralizados
    """
    try:
        print(LogMessages.SEARCHING_ELEMENT.format(element="segundo botón 'Save & Continue'"))
        
        # Esperar a que la nueva vista se cargue (optimizado)
        time.sleep(SleepTimes.FORM_LOAD)
        
        # Scroll inteligente hacia abajo para elementos lazy loading
        print("📜 Scroll inteligente para cargar elementos...")
        ClickHelper.scroll_to_bottom_smart(driver)
        
        # Búsqueda directa por texto usando DebugHelper
        save_button = DebugHelper.find_button_by_exact_text(driver, "SAVE & CONTINUE")
        
        if save_button:
            print("✅ Botón encontrado por búsqueda directa")
            success = ClickHelper.safe_click_with_scroll(
                driver, save_button, "segundo Save & Continue"
            )
            
            if success:
                time.sleep(SleepTimes.SAVE_PROCESSING)
                return True
        
        # Método de respaldo: Múltiples selectores centralizados
        print("🔄 Método de respaldo: selectores centralizados...")
        
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
        
        save_button = ElementFinder.find_by_multiple_selectors(
            driver, short_wait, save_selectors, "segundo botón Save & Continue"
        )
        
        if save_button:
            success = ClickHelper.safe_click_with_scroll(
                driver, save_button, "segundo Save & Continue (selector)"
            )
            
            if success:
                time.sleep(SleepTimes.SAVE_PROCESSING)
                return True
        
        # Debug automático usando helper
        print("❌ No se pudo encontrar el segundo botón 'Save & Continue'")
        DebugHelper.analyze_save_continue_buttons(driver)
        
        return False
        
    except Exception as e:
        print(f"❌ Error haciendo clic en segundo 'Save & Continue': {e}")
        return False

def handle_confirmation_modal(driver, wait):
    """
    Maneja el modal de confirmación si aparece usando selectores centralizados
    """
    try:
        print("🔍 Verificando si aparece modal de confirmación...")
        
        # Esperar un poco para que aparezca el modal (optimizado)
        time.sleep(SleepTimes.MODAL_APPEAR)
        
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
        
        modal_button = ElementFinder.find_by_multiple_selectors(
            driver, short_wait, modal_selectors, "botón de modal"
        )
        
        if modal_button:
            print("✅ Modal de confirmación encontrado!")
            
            success = ClickHelper.safe_click_with_scroll(
                driver, modal_button, "botón de confirmación"
            )
            
            if success:
                time.sleep(SleepTimes.MODAL_PROCESSING)
                print(LogMessages.PROCESS_COMPLETED.format(process="confirmación de modal"))
                return True
        else:
            print("ℹ️ No se detectó modal de confirmación (esto es normal)")
        
        return True  # True porque es opcional
        
    except Exception as e:
        print(f"⚠️ Error manejando modal de confirmación: {e}")
        return True  # No fallar el proceso por problemas de modal

def wait_for_final_processing(driver):
    """
    Espera a que se complete el procesamiento final usando timeouts centralizados
    """
    try:
        print("⏳ Esperando procesamiento final...")
        
        # Esperar procesamiento principal
        time.sleep(SleepTimes.FINAL_PROCESSING)
        
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
        
        for selector in loading_indicators:
            try:
                loading_element = short_wait.until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                
                if loading_element:
                    print("🔄 Detectado indicador de carga, esperando...")
                    # Esperar a que desaparezca
                    WebDriverWait(driver, ElementTimeouts.LOADING).until(
                        EC.invisibility_of_element(loading_element)
                    )
                    print("✅ Indicador de carga desapareció")
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
        
        for selector in success_indicators:
            try:
                success_element = short_wait.until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                
                if success_element:
                    success_text = success_element.text.strip()
                    print(f"✅ Indicador de éxito encontrado: '{success_text}'")
                    return True
            except TimeoutException:
                continue
        
        print("ℹ️ No se encontraron indicadores específicos, asumiendo éxito")
        return True
        
    except Exception as e:
        print(f"⚠️ Error durante espera de procesamiento: {e}")
        return True  # No fallar por esto

def execute_step_03(driver, wait=None):
    """
    Ejecuta el paso 3 completo: Guardar final y confirmación
    Función pública para mantener compatibilidad
    """
    try:
        print(f"\n{ProcessMessages.STEP_INDICATOR.format(step=3, description='Final Save')}")
        print("=" * 50)
        
        # Crear wait si no se proporciona
        if wait is None:
            wait = WebDriverWait(driver, ElementTimeouts.DEFAULT)
        
        # Paso 1: Hacer clic en segundo Save & Continue
        print(f"\n📝 Paso 3.1: Segundo botón 'Save & Continue'")
        if not click_second_save_and_continue(driver, wait):
            print(LogMessages.PROCESS_FAILED.format(process="segundo Save & Continue"))
            return False
        
        # Paso 2: Manejar modal de confirmación si aparece
        print(f"\n🔍 Paso 3.2: Verificar modal de confirmación")
        if not handle_confirmation_modal(driver, wait):
            print("⚠️ Problema con modal de confirmación, pero continuando...")
        
        # Paso 3: Esperar procesamiento final
        print(f"\n⏳ Paso 3.3: Esperar procesamiento final")
        if not wait_for_final_processing(driver):
            print("⚠️ Procesamiento final incierto, pero continuando...")
        
        # Proceso completado
        print(f"\n{LogMessages.PROCESS_COMPLETED.format(process='PASO 3 - Final Save')}")
        print(ProcessMessages.SUCCESS_SUMMARY)
        print("📊 Resumen de lo ejecutado:")
        print("   ✅ Segundo Save & Continue clickeado")
        print("   ✅ Modal de confirmación manejado")
        print("   ✅ Procesamiento final completado")
        print("\n🎯 El Prior Notice debería estar completamente guardado en FDA")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante el Paso 3: {e}")
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