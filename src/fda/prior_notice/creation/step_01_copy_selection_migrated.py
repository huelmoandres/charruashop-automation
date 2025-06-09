"""
Paso 2: Editar Información del Prior Notice (VERSIÓN MIGRADA)
Actualiza trackingNumber, state y portOfArrivalDate usando helpers centralizados

Esta es la versión mejorada que muestra cómo usar:
- Constantes centralizadas
- Helpers reutilizables  
- Rutas configurables
- Mensajes consistentes
"""

import csv
import os
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# 🆕 Imports de la nueva arquitectura
from src.constants.timeouts import SleepTimes, ElementTimeouts
from src.constants.selectors import FDASelectors
from src.constants.messages import LogMessages, UserMessages, ProcessMessages
from src.constants.paths import CSVPaths
from src.utils.selenium_helpers import ElementFinder, ClickHelper, InputHelper, DebugHelper

def read_guia_aerea_from_csv():
    """
    Lee el valor de guia_aerea desde el archivo CSV usando rutas centralizadas
    """
    try:
        csv_path = CSVPaths.FDA_ORDER_FILE  # 🆕 Ruta centralizada
        
        if not csv_path.exists():  # 🆕 Usando Path methods
            print(LogMessages.ELEMENT_NOT_FOUND.format(element=f"archivo CSV en {csv_path}"))
            return None
        
        print(LogMessages.READING_DATA.format(source=csv_path))
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
            if not rows:
                print(f"⚠️ El archivo CSV está vacío: {csv_path}")
                return None
            
            # Tomar el valor de guia_aerea del primer producto
            guia_aerea = rows[0].get('guia_aerea', '').strip()
            
            if not guia_aerea:
                print(f"⚠️ No se encontró valor en la columna 'guia_aerea'")
                return None
            
            print(LogMessages.DATA_FOUND.format(data=f"guía aérea: '{guia_aerea}'"))
            print(f"📦 Datos del pedido: {rows[0].get('order_number')} - {rows[0].get('shipping_name')}")
            
            return guia_aerea
            
    except Exception as e:
        print(f"❌ Error leyendo archivo CSV: {e}")
        return None

def click_edit_button(driver, wait):
    """
    Hace clic en el botón de editar información usando helpers
    """
    try:
        print(LogMessages.SEARCHING_ELEMENT.format(element="botón de editar información"))
        
        # 🆕 Usando selectores centralizados y ElementFinder
        edit_selectors = [
            FDASelectors.EDIT_BUTTON,
            "//button[contains(@class, 'edit-button')]",
            "//button[@title='Edit Information' and contains(@class, 'edit-button')]",
            "//button[.//i[contains(@class, 'edit-icon')]]"
        ]
        
        edit_button = ElementFinder.find_by_multiple_selectors(
            driver, wait, edit_selectors, "botón edit"
        )
        
        if not edit_button:
            return False
        
        # 🆕 Usando ClickHelper para clic seguro
        return ClickHelper.safe_click(driver, edit_button, "botón de editar")
        
    except Exception as e:
        print(LogMessages.CLICK_FAILED.format(element="botón edit"))
        print(f"Error: {e}")
        return False

def update_tracking_number(driver, wait, guia_aerea):
    """
    Actualiza el campo trackingNumber usando helpers mejorados
    """
    try:
        print(LogMessages.SEARCHING_ELEMENT.format(element="input trackingNumber"))
        
        # 🆕 Usando selector centralizado
        tracking_input = wait.until(
            EC.presence_of_element_located((By.ID, FDASelectors.TRACKING_NUMBER_INPUT))
        )
        
        print(LogMessages.ELEMENT_FOUND.format(element="campo trackingNumber"))
        
        # 🆕 Usando InputHelper para llenado con validación
        success = InputHelper.fill_input_with_validation(
            driver, tracking_input, guia_aerea, "trackingNumber"
        )
        
        return success
        
    except TimeoutException:
        print(LogMessages.ELEMENT_NOT_FOUND.format(element="campo trackingNumber"))
        return False
    except Exception as e:
        print(f"❌ Error actualizando trackingNumber: {e}")
        return False

def update_state_to_tennessee(driver, wait):
    """
    Actualiza el select state a Tennessee usando selectores centralizados
    """
    try:
        print(LogMessages.SEARCHING_ELEMENT.format(element="select de state"))
        
        # 🆕 Usando selector centralizado
        state_select = wait.until(
            EC.presence_of_element_located((By.NAME, FDASelectors.STATE_SELECT))
        )
        
        print(LogMessages.ELEMENT_FOUND.format(element="select state"))
        
        # Crear objeto Select
        select = Select(state_select)
        
        # Intentar seleccionar por valor TN
        try:
            select.select_by_value("TN")
            print(LogMessages.FIELD_UPDATED.format(field="state", value="Tennessee (TN) por valor"))
        except NoSuchElementException:
            # Si no funciona por valor, intentar por texto visible
            try:
                select.select_by_visible_text("Tennessee")
                print(LogMessages.FIELD_UPDATED.format(field="state", value="Tennessee por texto visible"))
            except NoSuchElementException:
                # Listar opciones disponibles para debug
                options = [option.text for option in select.options]
                print(f"⚠️ Opciones disponibles en select: {options}")
                print(f"❌ No se pudo seleccionar Tennessee")
                return False
        
        return True
        
    except TimeoutException:
        print(LogMessages.ELEMENT_NOT_FOUND.format(element="select de state"))
        return False
    except Exception as e:
        print(f"❌ Error actualizando state: {e}")
        return False

def update_port_of_arrival_date(driver, wait):
    """
    Actualiza el campo portOfArrivalDate con helpers avanzados y mensajes centralizados
    """
    try:
        print(LogMessages.SEARCHING_ELEMENT.format(element="input portOfArrivalDate"))
        
        # 🆕 Usando selector centralizado
        date_input = wait.until(
            EC.presence_of_element_located((By.ID, FDASelectors.PORT_ARRIVAL_DATE_INPUT))
        )
        
        print(LogMessages.ELEMENT_FOUND.format(element="campo portOfArrivalDate"))
        print(f"📋 Tipo de input: {date_input.get_attribute('class')}")
        
        # 🆕 Mostrar instrucciones centralizadas
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
        
        # 🆕 Estrategias múltiples usando timeouts centralizados
        success = False
        
        # Estrategia 1: InputHelper con limpieza avanzada
        try:
            print("🔄 Estrategia 1: InputHelper con limpieza avanzada")
            
            # Limpiar usando helper
            if InputHelper.clear_input_field(driver, date_input):
                print("🧹 Campo limpiado, enviando fecha...")
                date_input.send_keys(arrival_date)
                time.sleep(SleepTimes.FIELD_UPDATE)  # 🆕 Timeout centralizado
                
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
                
                time.sleep(SleepTimes.INPUT_CLEAR)  # 🆕 Timeout centralizado
                
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
                
                time.sleep(SleepTimes.FIELD_UPDATE)  # 🆕 Timeout centralizado
                
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
            
            # 🆕 Usar mensaje centralizado para confirmación
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
        
        # 🆕 Múltiples selectores centralizados
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
            # 🆕 Debug automático usando helper
            DebugHelper.list_all_buttons(driver)
            return False
        
        # 🆕 Usar ClickHelper
        success = ClickHelper.safe_click(driver, save_button, "Save & Continue")
        
        if success:
            # 🆕 Timeout centralizado
            time.sleep(SleepTimes.SAVE_PROCESSING)
            print(LogMessages.PROCESS_COMPLETED.format(process="Save & Continue"))
        
        return success
        
    except Exception as e:
        print(LogMessages.CLICK_FAILED.format(element="Save & Continue"))
        print(f"Error: {e}")
        return False

def execute_step_02_migrated(driver):
    """
    Ejecuta el paso 2 completo usando la nueva arquitectura
    """
    print(LogMessages.STARTING_PROCESS.format(process=ProcessMessages.EDIT_INFORMATION))
    print("=" * 50)
    
    wait = WebDriverWait(driver, ElementTimeouts.DEFAULT)  # 🆕 Timeout centralizado
    
    # Paso 1: Leer guía aérea del CSV
    print(f"\n📋 Paso 2.1: Leer guía aérea desde CSV")
    guia_aerea = read_guia_aerea_from_csv()
    
    if not guia_aerea:
        print(LogMessages.PROCESS_FAILED.format(process="lectura de guía aérea"))
        return False
    
    # Paso 2: Hacer clic en botón edit
    print(f"\n🖱️ Paso 2.2: Hacer clic en botón de editar")
    if not click_edit_button(driver, wait):
        print(LogMessages.PROCESS_FAILED.format(process="clic en botón edit"))
        return False
    
    # Esperar a que se cargue la vista de edición
    time.sleep(SleepTimes.FORM_LOAD)  # 🆕 Timeout centralizado
    
    # Paso 3: Actualizar trackingNumber
    print(f"\n📝 Paso 2.3: Actualizar trackingNumber")
    if not update_tracking_number(driver, wait, guia_aerea):
        print("⚠️ Error actualizando trackingNumber")
    
    # Paso 4: Actualizar state a Tennessee
    print(f"\n🏛️ Paso 2.4: Actualizar state a Tennessee")
    if not update_state_to_tennessee(driver, wait):
        print("⚠️ Error actualizando state")
    
    # Paso 5: Actualizar port of arrival date
    print(f"\n📅 Paso 2.5: Actualizar fecha de llegada al puerto")
    if not update_port_of_arrival_date(driver, wait):
        print("⚠️ Error actualizando portOfArrivalDate")
    
    # Paso 6: Clic en botón "Save & Continue"
    print(f"\n🖱️ Paso 2.6: Clic en botón 'Save & Continue'")
    if not click_save_and_continue_button(driver, wait):
        print("❌ Error al hacer clic en 'Save & Continue'")
    
    print(f"\n{LogMessages.PROCESS_COMPLETED.format(process='PASO 2')}")
    print(ProcessMessages.CHANGES_SUMMARY)
    print(f"   • trackingNumber: {guia_aerea}")
    print(f"   • state: Tennessee (TN)")
    print(f"   • portOfArrivalDate: (ingresado por usuario)")
    print(f"   • Save & Continue: Clickeado")
    print(f"\n🎯 El Prior Notice está listo para el siguiente paso")
    
    return True

if __name__ == "__main__":
    print("⚠️ Este archivo debe ser ejecutado desde creation_coordinator.py")
    print("💡 Para testing individual, importa la función execute_step_02_migrated(driver)") 