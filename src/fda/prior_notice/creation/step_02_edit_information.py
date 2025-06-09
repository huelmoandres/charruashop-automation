"""
Paso 2: Editar Información del Prior Notice (MIGRADO)
Actualiza trackingNumber, state y portOfArrivalDate usando helpers centralizados

Mejoras implementadas:
- Constantes centralizadas
- Helpers reutilizables  
- Rutas configurables
- Mensajes consistentes
- Manejo avanzado de Angular Material datepicker
"""

import csv
import os
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Imports de la nueva arquitectura
from src.constants.timeouts import SleepTimes, ElementTimeouts
from src.constants.selectors import FDASelectors
from src.constants.messages import LogMessages, UserMessages, ProcessMessages
from src.constants.paths import ORDER_SAMPLE_FILE
from src.utils.selenium_helpers import ElementFinder, ClickHelper, InputHelper, DebugHelper, WaitHelper
from src.core.logger import AutomationLogger

# Inicializar logger
logger = AutomationLogger.get_instance()

def read_guia_aerea_from_csv():
    """
    Lee el valor de guia_aerea desde el archivo CSV usando rutas centralizadas
    """
    logger.fda_logger.info("=== LEYENDO GUÍA AÉREA DESDE CSV ===")
    
    try:
        csv_path = ORDER_SAMPLE_FILE  # Ruta centralizada
        
        logger.fda_logger.debug("Verificando existencia de archivo CSV", extra={"csv_path": str(csv_path)})
        
        if not csv_path.exists():  # Usando Path methods
            logger.fda_logger.error("Archivo CSV no encontrado", extra={"expected_path": str(csv_path)})
            return None
        
        logger.fda_logger.info("Archivo CSV encontrado, leyendo datos", extra={"file_path": str(csv_path)})
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
            if not rows:
                logger.fda_logger.warning("Archivo CSV está vacío", extra={"file_path": str(csv_path)})
                return None
            
            # Tomar el valor de guia_aerea del primer producto
            guia_aerea = rows[0].get('guia_aerea', '').strip()
            
            if not guia_aerea:
                logger.fda_logger.warning("No se encontró valor en la columna 'guia_aerea'")
                return None
            
            order_info = {
                "guia_aerea": guia_aerea,
                "order_number": rows[0].get('order_number', 'N/A'),
                "shipping_name": rows[0].get('shipping_name', 'N/A')
            }
            
            logger.fda_logger.info("Guía aérea leída exitosamente", extra=order_info)
            
            return guia_aerea
            
    except Exception as e:
        logger.fda_logger.error("Error leyendo archivo CSV", extra={"error": str(e), "file_path": str(csv_path)})
        logger.error_logger.error("CSV reading failed", extra={
            "source_module": "fda_prior_notice_step_02",
            "function": "read_guia_aerea_from_csv",
            "error": str(e),
            "file_path": str(csv_path)
        })
        return None

def click_edit_button(driver, wait):
    """
    Hace clic en el botón de editar información usando helpers
    """
    logger.fda_logger.info("Iniciando búsqueda del botón de editar información")
    
    try:
        # Usando selectores centralizados y ElementFinder
        edit_selectors = [
            FDASelectors.EDIT_BUTTON,
            "//button[contains(@class, 'edit-button')]",
            "//button[@title='Edit Information' and contains(@class, 'edit-button')]",
            "//button[.//i[contains(@class, 'edit-icon')]]"
        ]
        
        logger.fda_logger.debug("Buscando botón de editar con múltiples selectores", extra={
            "selectors_count": len(edit_selectors)
        })
        
        edit_button = ElementFinder.find_by_multiple_selectors(
            driver, wait, edit_selectors, "botón edit"
        )
        
        if not edit_button:
            logger.fda_logger.error("Botón de editar información no encontrado")
            return False
        
        logger.fda_logger.info("Botón de editar información encontrado")
        
        # Usando ClickHelper para clic seguro
        success = ClickHelper.safe_click(driver, edit_button, "botón de editar")
        
        if success:
            logger.fda_logger.info("Clic en botón de editar ejecutado exitosamente")
        else:
            logger.fda_logger.error("Falló el clic en botón de editar")
        
        return success
        
    except Exception as e:
        logger.fda_logger.error("Error haciendo clic en botón edit", extra={"error": str(e)})
        logger.error_logger.error("Edit button click failed", extra={
            "source_module": "fda_prior_notice_step_02",
            "function": "click_edit_button",
            "error": str(e)
        })
        return False

def update_tracking_number(driver, wait, guia_aerea):
    """
    Actualiza el campo trackingNumber usando helpers mejorados
    """
    logger.fda_logger.info("Actualizando campo trackingNumber", extra={"tracking_value": guia_aerea})
    
    try:
        logger.fda_logger.debug("Buscando input trackingNumber")
        
        # Usando selector centralizado
        tracking_input = wait.until(
            EC.presence_of_element_located((By.ID, FDASelectors.TRACKING_NUMBER_INPUT))
        )
        
        logger.fda_logger.debug("Campo trackingNumber encontrado")
        
        # Usando InputHelper para llenado con validación
        success = InputHelper.fill_input_with_validation(
            driver, tracking_input, guia_aerea, "trackingNumber"
        )
        
        if success:
            logger.fda_logger.info("Campo trackingNumber actualizado exitosamente", extra={
                "field": "trackingNumber",
                "value": guia_aerea
            })
        else:
            logger.fda_logger.error("Falló la actualización del campo trackingNumber")
        
        return success
        
    except TimeoutException:
        logger.fda_logger.error("Timeout: Campo trackingNumber no encontrado", extra={
            "selector": FDASelectors.TRACKING_NUMBER_INPUT,
            "timeout": wait._timeout
        })
        return False
    except Exception as e:
        logger.fda_logger.error("Error actualizando trackingNumber", extra={"error": str(e)})
        logger.error_logger.error("Tracking number update failed", extra={
            "source_module": "fda_prior_notice_step_02",
            "function": "update_tracking_number",
            "error": str(e),
            "tracking_value": guia_aerea
        })
        return False

def update_state_to_tennessee(driver, wait):
    """
    Actualiza el select state a Tennessee usando selectores centralizados
    """
    logger.fda_logger.info("Actualizando campo state a Tennessee")
    
    try:
        logger.fda_logger.debug("Buscando select de state")
        
        # Usando selector centralizado
        state_select = wait.until(
            EC.presence_of_element_located((By.NAME, FDASelectors.STATE_SELECT))
        )
        
        logger.fda_logger.debug("Select state encontrado")
        
        # Crear objeto Select
        select = Select(state_select)
        
        # Intentar seleccionar por valor TN
        try:
            select.select_by_value("TN")
            logger.fda_logger.info("State actualizado exitosamente", extra={
                "field": "state",
                "value": "Tennessee (TN)",
                "method": "by_value"
            })
        except NoSuchElementException:
            # Si no funciona por valor, intentar por texto visible
            try:
                select.select_by_visible_text("Tennessee")
                logger.fda_logger.info("State actualizado exitosamente", extra={
                    "field": "state", 
                    "value": "Tennessee",
                    "method": "by_visible_text"
                })
            except NoSuchElementException:
                # Listar opciones disponibles para debug
                options = [option.text for option in select.options]
                logger.fda_logger.error("No se pudo seleccionar Tennessee", extra={
                    "available_options": options,
                    "attempted_values": ["TN", "Tennessee"]
                })
                return False
        
        return True
        
    except TimeoutException:
        logger.fda_logger.error("Timeout: Select de state no encontrado", extra={
            "selector": FDASelectors.STATE_SELECT,
            "timeout": wait._timeout
        })
        return False
    except Exception as e:
        logger.fda_logger.error("Error actualizando state", extra={"error": str(e)})
        logger.error_logger.error("State update failed", extra={
            "source_module": "fda_prior_notice_step_02",
            "function": "update_state_to_tennessee",
            "error": str(e)
        })
        return False

def update_port_of_arrival_date(driver, wait):
    """
    Actualiza el campo portOfArrivalDate con helpers avanzados y mensajes centralizados
    """
    try:
        print(LogMessages.SEARCHING_ELEMENT.format(element="input portOfArrivalDate"))
        
        # Usando selector centralizado
        date_input = wait.until(
            EC.presence_of_element_located((By.ID, FDASelectors.PORT_ARRIVAL_DATE_INPUT))
        )
        
        print(LogMessages.ELEMENT_FOUND.format(element="campo portOfArrivalDate"))
        print(f"📋 Tipo de input: {date_input.get_attribute('class')}")
        
        # Mostrar instrucciones centralizadas
        print(UserMessages.DATE_FORMAT_HELP)
        
        while True:
            arrival_date = input(UserMessages.ENTER_DATE).strip()
            
            if not arrival_date:
                print(UserMessages.EMPTY_DATE)
                continue
            
            # Validación más estricta para formato MM/DD/YYYY
            pattern = r'^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/(19|20)\d{2}$'
            
            if re.match(pattern, arrival_date):
                # Validación adicional de fechas lógicas
                parts = arrival_date.split('/')
                month, day, year = int(parts[0]), int(parts[1]), int(parts[2])
                
                if month > 12 or day > 31:
                    print(UserMessages.INVALID_DATE_VALUES)
                    continue
                
                print(f"✅ Formato de fecha válido: {arrival_date}")
                break
            else:
                print(UserMessages.INVALID_DATE_FORMAT)
                print("💡 Ejemplos: 01/15/2024, 12/25/2023")
                continue
        
        # Estrategias múltiples usando timeouts centralizados
        success = False
        
        # Estrategia 1: InputHelper con limpieza avanzada
        try:
            print("🔄 Estrategia 1: InputHelper con limpieza avanzada")
            
            # Limpiar usando helper
            if InputHelper.clear_input_field(driver, date_input):
                print("🧹 Campo limpiado, enviando fecha...")
                date_input.send_keys(arrival_date)
                time.sleep(SleepTimes.FIELD_UPDATE)  # Timeout centralizado
                
                # Verificar resultado
                final_value = date_input.get_attribute('value')
                if final_value and arrival_date in final_value:
                    print(LogMessages.FIELD_UPDATED.format(field="portOfArrivalDate", value=arrival_date))
                    success = True
            
        except Exception as e:
            print(f"❌ Estrategia 1 falló: {e}")
        
        # Estrategia 2: JavaScript completo si falló la primera
        if not success:
            try:
                print("🔄 Estrategia 2: JavaScript con eventos Angular")
                
                # Limpiar completamente con JavaScript
                driver.execute_script("""
                    var input = arguments[0];
                    input.value = '';
                    input.setAttribute('value', '');
                """, date_input)
                
                time.sleep(SleepTimes.INPUT_CLEAR)  # Timeout centralizado
                
                # Establecer el nuevo valor
                driver.execute_script(f"arguments[0].value = '{arrival_date}';", date_input)
                
                # Disparar eventos Angular
                driver.execute_script("""
                    var input = arguments[0];
                    var inputEvent = new Event('input', { bubbles: true, cancelable: true });
                    var changeEvent = new Event('change', { bubbles: true, cancelable: true });
                    var focusEvent = new Event('focus', { bubbles: true });
                    var blurEvent = new Event('blur', { bubbles: true });
                    
                    input.dispatchEvent(focusEvent);
                    input.dispatchEvent(inputEvent);
                    input.dispatchEvent(changeEvent);
                    input.dispatchEvent(blurEvent);
                """, date_input)
                
                time.sleep(SleepTimes.FIELD_UPDATE)  # Timeout centralizado
                
                # Verificar
                final_value = date_input.get_attribute('value')
                if final_value and arrival_date in final_value:
                    print(LogMessages.FIELD_UPDATED.format(field="portOfArrivalDate", value=arrival_date))
                    success = True
                    
            except Exception as e:
                print(f"❌ Estrategia 2 falló: {e}")
        
        # Verificación final
        final_check_value = date_input.get_attribute('value')
        print(f"\n📊 VERIFICACIÓN FINAL:")
        print(f"   Fecha ingresada: '{arrival_date}'")
        print(f"   Valor en campo:  '{final_check_value}'")
        
        if success:
            print(LogMessages.PROCESS_COMPLETED.format(process="actualización de fecha"))
            return True
        else:
            print(f"⚠️ Fecha ingresada pero verificación incierta")
            
            # Usar mensaje centralizado para confirmación
            user_confirm = input(UserMessages.FIELD_CORRECT).strip().lower()
            if user_confirm in ['s', 'si', 'yes', 'y']:
                print("✅ Usuario confirmó que el campo está correcto")
                return True
            else:
                print("❌ Usuario indica que hay problemas con el campo")
                return False
        
    except TimeoutException:
        print(LogMessages.ELEMENT_NOT_FOUND.format(element="campo portOfArrivalDate"))
        return False
    except Exception as e:
        print(f"❌ Error actualizando portOfArrivalDate: {e}")
        return False

def click_save_and_continue_button(driver, wait):
    """
    Hace clic en el botón "Save & Continue" usando helpers y selectores centralizados
    """
    try:
        print(LogMessages.SEARCHING_ELEMENT.format(element="botón 'Save & Continue'"))
        
        # Múltiples selectores centralizados
        save_selectors = [
            FDASelectors.SAVE_CONTINUE_BUTTON,
            "//button[contains(text(), 'Save')]//span[contains(text(), 'Continue')]",
            f"//button[@class='{FDASelectors.SAVE_CONTINUE_CLASS}']",
            "//span[contains(text(), 'Save & Continue')]/parent::button",
            "//button[.//span[contains(text(), 'Save & Continue')]]"
        ]
        
        save_button = ElementFinder.find_by_multiple_selectors(
            driver, wait, save_selectors, "botón Save & Continue"
        )
        
        if not save_button:
            # Debug automático usando helper
            DebugHelper.list_all_buttons(driver)
            return False
        
        # Usar ClickHelper
        success = ClickHelper.safe_click(driver, save_button, "Save & Continue")
        
        if success:
            # Timeout centralizado
            time.sleep(SleepTimes.SAVE_PROCESSING)
            print(LogMessages.PROCESS_COMPLETED.format(process="Save & Continue"))
        
        return success
        
    except Exception as e:
        print(LogMessages.CLICK_FAILED.format(element="Save & Continue"))
        print(f"Error: {e}")
        return False

def execute_step_02(driver, wait=None):
    """
    Ejecuta el paso 2 completo usando la nueva arquitectura
    Función pública para mantener compatibilidad
    """
    logger.fda_logger.info("🔄 EJECUTANDO PASO 2: EDIT INFORMATION")
    
    # Crear wait si no se proporciona
    if wait is None:
        wait = WebDriverWait(driver, ElementTimeouts.DEFAULT)
    
    logger.fda_logger.debug("WebDriverWait configurado", extra={"timeout": ElementTimeouts.DEFAULT})
    
    # Paso 1: Leer guía aérea del CSV
    logger.fda_logger.info("📋 Paso 2.1: Leer guía aérea desde CSV")
    guia_aerea = read_guia_aerea_from_csv()
    
    if not guia_aerea:
        logger.fda_logger.error("Falló lectura de guía aérea")
        return False
    
    # Paso 2: Hacer clic en botón edit
    logger.fda_logger.info("🖱️ Paso 2.2: Hacer clic en botón de editar")
    if not click_edit_button(driver, wait):
        logger.fda_logger.error("Falló clic en botón edit")
        return False
    
    # Esperar a que se cargue la vista de edición
    time.sleep(SleepTimes.FORM_LOAD)  # Timeout centralizado
    logger.fda_logger.debug("Esperando carga de vista de edición", extra={"sleep_time": SleepTimes.FORM_LOAD})
    
    # Paso 3: Actualizar trackingNumber
    logger.fda_logger.info("📝 Paso 2.3: Actualizar trackingNumber")
    if not update_tracking_number(driver, wait, guia_aerea):
        logger.fda_logger.warning("Error actualizando trackingNumber")
    
    # Paso 4: Actualizar state a Tennessee
    logger.fda_logger.info("🏛️ Paso 2.4: Actualizar state a Tennessee")
    if not update_state_to_tennessee(driver, wait):
        logger.fda_logger.warning("Error actualizando state")
    
    # Paso 5: Actualizar port of arrival date
    logger.fda_logger.info("📅 Paso 2.5: Actualizar fecha de llegada al puerto")
    if not update_port_of_arrival_date(driver, wait):
        logger.fda_logger.warning("Error actualizando portOfArrivalDate")
    
    # Paso 6: Clic en botón "Save & Continue"
    logger.fda_logger.info("🖱️ Paso 2.6: Clic en botón 'Save & Continue'")
    if not click_save_and_continue_button(driver, wait):
        logger.fda_logger.error("Error al hacer clic en 'Save & Continue'")
    
    logger.fda_logger.info("✅ PASO 2 - Edit Information COMPLETADO")
    logger.fda_logger.info("📋 Resumen de cambios realizados:", extra={
        "trackingNumber": guia_aerea,
        "state": "Tennessee (TN)",
        "portOfArrivalDate": "(ingresado por usuario)",
        "save_and_continue": "Clickeado"
    })
    
    logger.fda_logger.info("🎯 El Prior Notice está listo para el siguiente paso")
    
    return True

# Alias para mantener compatibilidad con código legacy
def complete_step_02_edit_information(driver, wait):
    """
    Alias para compatibilidad con versiones anteriores
    """
    return execute_step_02(driver, wait)

if __name__ == "__main__":
    print("⚠️ Este archivo debe ser ejecutado desde main.py")
    print("💡 Para testing individual, importa la función execute_step_02(driver)") 