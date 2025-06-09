"""
Funciones utilitarias reutilizables para operaciones con Selenium
Centraliza operaciones comunes para evitar duplicación de código
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from typing import List, Optional, Union

from ..constants.timeouts import SleepTimes, ElementTimeouts
from ..constants.messages import LogMessages
from src.core.logger import AutomationLogger

# Inicializar logger
logger = AutomationLogger.get_instance()

class ElementFinder:
    """Clase para encontrar elementos con múltiples estrategias"""
    
    @staticmethod
    def find_by_multiple_selectors(driver, wait: WebDriverWait, selectors: List[str], 
                                 element_name: str = "elemento") -> Optional[object]:
        """
        Busca un elemento usando múltiples selectores como respaldo
        
        Args:
            driver: WebDriver instance
            wait: WebDriverWait instance
            selectors: Lista de selectores XPath a probar
            element_name: Nombre del elemento para logging
            
        Returns:
            Elemento encontrado o None si no se encuentra
        """
        logger.selenium_logger.info("=== BUSCANDO ELEMENTO CON MÚLTIPLES SELECTORES ===", extra={
            "element_name": element_name,
            "selectors_count": len(selectors)
        })
        
        print(LogMessages.SEARCHING_ELEMENT.format(element=element_name))
        
        for i, selector in enumerate(selectors):
            try:
                logger.selenium_logger.debug("Probando selector", extra={
                    "attempt": i + 1,
                    "selector": selector,
                    "element_name": element_name
                })
                
                element = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                
                logger.selenium_logger.info("Elemento encontrado exitosamente", extra={
                    "element_name": element_name,
                    "selector_used": selector,
                    "attempt": i + 1
                })
                
                print(LogMessages.ELEMENT_FOUND.format(element=element_name))
                print(f"   📍 Selector usado: {selector}")
                return element
            except TimeoutException:
                logger.selenium_logger.warning("Selector falló", extra={
                    "attempt": i + 1,
                    "selector": selector,
                    "element_name": element_name
                })
                
                if i < len(selectors) - 1:
                    print(f"   ⚠️ Selector {i+1} falló, probando siguiente...")
                continue
        
        logger.selenium_logger.error("Elemento no encontrado con ningún selector", extra={
            "element_name": element_name,
            "total_selectors": len(selectors)
        })
        
        print(LogMessages.ELEMENT_NOT_FOUND.format(element=element_name))
        return None

    @staticmethod
    def find_button_by_text(driver, text: str, partial_match: bool = True) -> Optional[object]:
        """
        Encuentra un botón por su texto
        
        Args:
            driver: WebDriver instance
            text: Texto a buscar en el botón
            partial_match: Si usar coincidencia parcial o exacta
            
        Returns:
            Botón encontrado o None
        """
        logger.selenium_logger.debug("Buscando botón por texto", extra={
            "text": text,
            "partial_match": partial_match
        })
        
        try:
            selector = f"//button[contains(text(), '{text}')]" if partial_match else f"//button[text()='{text}']"
            button = driver.find_element(By.XPATH, selector)
            
            logger.selenium_logger.info("Botón encontrado por texto", extra={
                "text": text,
                "selector": selector
            })
            
            return button
        except NoSuchElementException:
            logger.selenium_logger.warning("Botón no encontrado por texto", extra={
                "text": text,
                "partial_match": partial_match
            })
            return None

class ClickHelper:
    """Clase para manejar clics con múltiples estrategias"""
    
    @staticmethod
    def safe_click(driver, element, element_name: str = "elemento") -> bool:
        """
        Hace clic en un elemento con múltiples estrategias de respaldo
        
        Args:
            driver: WebDriver instance
            element: Elemento en el que hacer clic
            element_name: Nombre del elemento para logging
            
        Returns:
            True si el clic fue exitoso, False si falló
        """
        logger.selenium_logger.info("=== EJECUTANDO CLIC SEGURO ===", extra={
            "element_name": element_name
        })
        
        print(LogMessages.CLICKING_ELEMENT.format(element=element_name))
        
        # Estrategia 1: Scroll y clic normal
        try:
            logger.selenium_logger.debug("Intentando clic normal con scroll", extra={
                "element_name": element_name
            })
            
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(SleepTimes.SCROLL)
            element.click()
            
            logger.selenium_logger.info("Clic normal exitoso", extra={
                "element_name": element_name,
                "method": "normal_click"
            })
            
            print(LogMessages.CLICK_SUCCESS.format(element=element_name))
            return True
        except Exception as e:
            logger.selenium_logger.warning("Clic normal falló", extra={
                "element_name": element_name,
                "error": str(e)
            })
            print(f"   ⚠️ Clic normal falló: {e}")
        
        # Estrategia 2: JavaScript click
        try:
            logger.selenium_logger.debug("Intentando clic con JavaScript", extra={
                "element_name": element_name
            })
            
            driver.execute_script("arguments[0].click();", element)
            
            logger.selenium_logger.info("Clic JavaScript exitoso", extra={
                "element_name": element_name,
                "method": "javascript_click"
            })
            
            print(LogMessages.CLICK_SUCCESS.format(element=element_name) + " (JavaScript)")
            return True
        except Exception as e:
            logger.selenium_logger.error("Todas las estrategias de clic fallaron", extra={
                "element_name": element_name,
                "error": str(e)
            })
            print(LogMessages.CLICK_FAILED.format(element=element_name))
            return False

    @staticmethod
    def scroll_to_bottom_smart(driver):
        """
        Scroll inteligente hacia abajo para cargar elementos lazy loading
        """
        logger.selenium_logger.debug("Ejecutando scroll inteligente")
        
        try:
            # Scroll gradual para cargar elementos lazy
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
            time.sleep(0.3)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            
            logger.selenium_logger.info("Scroll inteligente completado exitosamente")
            print("📜 Scroll inteligente completado")
            return True
        except Exception as e:
            logger.selenium_logger.error("Error en scroll inteligente", extra={"error": str(e)})
            print(f"⚠️ Error en scroll inteligente: {e}")
            return False
    
    @staticmethod
    def safe_click_with_scroll(driver, element, element_name="elemento"):
        """
        Hace clic seguro con scroll automático al elemento
        """
        logger.selenium_logger.info("Ejecutando clic seguro con scroll", extra={
            "element_name": element_name
        })
        
        try:
            # Scroll al elemento
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            
            # Intentar clic normal
            try:
                element.click()
                logger.selenium_logger.info("Clic seguro exitoso", extra={
                    "element_name": element_name,
                    "method": "normal_click"
                })
                print(f"✅ {element_name} clickeado exitosamente")
                return True
            except:
                # Fallback con JavaScript
                driver.execute_script("arguments[0].click();", element)
                logger.selenium_logger.info("Clic seguro exitoso con JavaScript", extra={
                    "element_name": element_name,
                    "method": "javascript_click"
                })
                print(f"✅ {element_name} clickeado con JavaScript")
                return True
                
        except Exception as e:
            logger.selenium_logger.error("Error en clic seguro con scroll", extra={
                "element_name": element_name,
                "error": str(e)
            })
            print(f"❌ Error haciendo clic en {element_name}: {e}")
            return False

class InputHelper:
    """Clase para manejar inputs y formularios"""
    
    @staticmethod
    def clear_input_field(driver, input_element, max_attempts: int = 3) -> bool:
        """
        Limpia un campo de input de forma agresiva (útil para Angular Material)
        
        Args:
            driver: WebDriver instance
            input_element: Elemento input a limpiar
            max_attempts: Número máximo de intentos
            
        Returns:
            True si se limpió exitosamente, False si falló
        """
        logger.selenium_logger.info("=== LIMPIANDO CAMPO INPUT ===", extra={
            "max_attempts": max_attempts
        })
        
        for attempt in range(max_attempts):
            try:
                logger.selenium_logger.debug("Intento de limpieza", extra={
                    "attempt": attempt + 1,
                    "max_attempts": max_attempts
                })
                
                print(f"🧹 Intento {attempt + 1} de limpieza del campo...")
                
                # Método 1: Clear básico
                input_element.clear()
                
                # Método 2: Seleccionar todo y borrar
                input_element.send_keys(Keys.CONTROL + "a")
                input_element.send_keys(Keys.BACKSPACE)
                
                # Método 3: JavaScript múltiple
                driver.execute_script("""
                    var element = arguments[0];
                    element.value = '';
                    element.setAttribute('value', '');
                    element.textContent = '';
                    if (element.setAttribute) element.setAttribute('data-value', '');
                """, input_element)
                
                # Método 4: Múltiples backspaces
                for _ in range(20):
                    input_element.send_keys(Keys.BACKSPACE)
                
                time.sleep(SleepTimes.INPUT_CLEAR)
                
                # Verificar si está limpio
                current_value = input_element.get_attribute('value') or ''
                if not current_value or len(current_value.strip()) == 0:
                    logger.selenium_logger.info("Campo limpiado exitosamente", extra={
                        "attempt": attempt + 1
                    })
                    print(f"✅ Campo limpiado exitosamente en intento {attempt + 1}")
                    return True
                else:
                    logger.selenium_logger.warning("Limpieza parcial", extra={
                        "attempt": attempt + 1,
                        "remaining_value": current_value
                    })
                    print(f"⚠️ Intento {attempt + 1} parcial. Valor restante: '{current_value}'")
                    
            except Exception as e:
                logger.selenium_logger.error("Error en intento de limpieza", extra={
                    "attempt": attempt + 1,
                    "error": str(e)
                })
        
        logger.selenium_logger.error("No se pudo limpiar el campo después de todos los intentos", extra={
            "max_attempts": max_attempts
        })
        return False

    @staticmethod
    def fill_input_with_validation(driver, input_element, value: str, 
                                 element_name: str = "campo") -> bool:
        """
        Llena un input y valida que el valor se haya establecido correctamente
        
        Args:
            driver: WebDriver instance
            input_element: Elemento input a llenar
            value: Valor a escribir
            element_name: Nombre del campo para logging
            
        Returns:
            True si se llenó correctamente, False si falló
        """
        logger.selenium_logger.info("=== LLENANDO CAMPO CON VALIDACIÓN ===", extra={
            "element_name": element_name,
            "value_length": len(value)
        })
        
        print(LogMessages.UPDATING_FIELD.format(field=element_name))
        
        # Limpiar primero
        if not InputHelper.clear_input_field(driver, input_element):
            logger.selenium_logger.warning("No se pudo limpiar campo completamente", extra={
                "element_name": element_name
            })
            print(f"⚠️ No se pudo limpiar {element_name} completamente")
        
        # Escribir valor
        input_element.send_keys(value)
        time.sleep(SleepTimes.FIELD_UPDATE)
        
        # Validar
        current_value = input_element.get_attribute('value')
        if value in current_value:
            logger.selenium_logger.info("Campo llenado y validado exitosamente", extra={
                "element_name": element_name,
                "expected_value": value,
                "current_value": current_value
            })
            print(LogMessages.FIELD_UPDATED.format(field=element_name, value=value))
            return True
        else:
            logger.selenium_logger.error("Validación de campo falló", extra={
                "element_name": element_name,
                "expected_value": value,
                "current_value": current_value
            })
            print(f"⚠️ Valor esperado: '{value}', valor actual: '{current_value}'")
            return False

class WaitHelper:
    """Clase para manejar esperas inteligentes"""
    
    @staticmethod
    def wait_for_page_load(driver, timeout: int = ElementTimeouts.NAVIGATION):
        """
        Espera a que la página se cargue completamente
        
        Args:
            driver: WebDriver instance
            timeout: Timeout en segundos
        """
        logger.selenium_logger.debug("Esperando carga completa de página", extra={
            "timeout": timeout
        })
        
        wait = WebDriverWait(driver, timeout)
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        
        logger.selenium_logger.info("Página cargada completamente")

    @staticmethod
    def wait_for_element_to_disappear(driver, selector: str, timeout: int = ElementTimeouts.DEFAULT):
        """
        Espera a que un elemento desaparezca de la página
        
        Args:
            driver: WebDriver instance
            selector: Selector del elemento
            timeout: Timeout en segundos
        """
        logger.selenium_logger.debug("Esperando que elemento desaparezca", extra={
            "selector": selector,
            "timeout": timeout
        })
        
        try:
            wait = WebDriverWait(driver, timeout)
            wait.until_not(EC.presence_of_element_located((By.XPATH, selector)))
            
            logger.selenium_logger.info("Elemento desapareció exitosamente", extra={
                "selector": selector
            })
            return True
        except TimeoutException:
            logger.selenium_logger.warning("Timeout esperando que elemento desaparezca", extra={
                "selector": selector,
                "timeout": timeout
            })
            return False

class DebugHelper:
    """Clase para funciones de debug y diagnóstico"""
    
    @staticmethod
    def list_all_buttons(driver, max_buttons: int = 20):
        """
        Lista todos los botones disponibles en la página para debug
        
        Args:
            driver: WebDriver instance
            max_buttons: Número máximo de botones a mostrar
        """
        logger.selenium_logger.debug("=== LISTANDO BOTONES PARA DEBUG ===", extra={
            "max_buttons": max_buttons
        })
        
        try:
            buttons = driver.find_elements(By.TAG_NAME, "button")
            
            logger.selenium_logger.info("Botones encontrados en página", extra={
                "total_buttons": len(buttons),
                "showing_max": max_buttons
            })
            
            print(f"🔍 Botones disponibles en la página ({len(buttons)}):")
            
            for i, btn in enumerate(buttons[:max_buttons]):
                try:
                    btn_text = btn.text.strip() or "Sin texto"
                    btn_class = btn.get_attribute("class") or "Sin clase"
                    btn_title = btn.get_attribute("title") or "Sin title"
                    
                    button_info = {
                        "index": i + 1,
                        "text": btn_text,
                        "class": btn_class[:50],
                        "title": btn_title
                    }
                    
                    logger.selenium_logger.debug("Botón encontrado", extra=button_info)
                    print(f"   {i+1}. Texto: '{btn_text}' | Clase: '{btn_class[:50]}...' | Title: '{btn_title}'")
                except:
                    continue
                    
            if len(buttons) > max_buttons:
                logger.selenium_logger.debug("Botones adicionales no mostrados", extra={
                    "hidden_buttons": len(buttons) - max_buttons
                })
                print(f"   ... y {len(buttons) - max_buttons} botones más")
                
        except Exception as e:
            logger.selenium_logger.error("Error listando botones", extra={
                "error": str(e)
            })
            print(f"❌ Error listando botones: {e}")

    @staticmethod
    def capture_page_info(driver):
        """
        Captura información general de la página actual
        
        Args:
            driver: WebDriver instance
        """
        try:
            print("📊 INFORMACIÓN DE LA PÁGINA:")
            print(f"   URL: {driver.current_url}")
            print(f"   Título: {driver.title}")
            
            # Contar elementos
            buttons = len(driver.find_elements(By.TAG_NAME, "button"))
            inputs = len(driver.find_elements(By.TAG_NAME, "input"))
            selects = len(driver.find_elements(By.TAG_NAME, "select"))
            
            print(f"   Elementos: {buttons} botones, {inputs} inputs, {selects} selects")
            
        except Exception as e:
            print(f"❌ Error capturando info de página: {e}")

    @staticmethod
    def find_button_by_exact_text(driver, text):
        """
        Busca un botón por texto exacto
        """
        try:
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            
            for btn in all_buttons:
                try:
                    btn_text = btn.text.strip()
                    if btn_text == text:
                        return btn
                except:
                    continue
            
            return None
        except Exception as e:
            print(f"❌ Error buscando botón por texto exacto: {e}")
            return None
    
    @staticmethod
    def analyze_buttons_with_text(driver, search_text):
        """
        Analiza botones que contengan cierto texto
        """
        try:
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            matching_buttons = []
            
            for btn in all_buttons:
                try:
                    btn_text = btn.text.strip()
                    if search_text.lower() in btn_text.lower():
                        matching_buttons.append({
                            'element': btn,
                            'text': btn_text,
                            'class': btn.get_attribute("class") or ""
                        })
                except:
                    continue
            
            return matching_buttons
        except Exception as e:
            print(f"❌ Error analizando botones: {e}")
            return []
    
    @staticmethod
    def analyze_save_continue_buttons(driver):
        """
        Analiza específicamente botones relacionados con Save/Continue
        """
        try:
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            print(f"📊 Total de botones encontrados: {len(all_buttons)}")
            
            # Buscar específicamente botones con "SAVE" o "Continue"
            save_buttons = []
            for i, btn in enumerate(all_buttons):
                try:
                    btn_text = btn.text.strip().upper()
                    btn_class = btn.get_attribute("class") or ""
                    
                    if "SAVE" in btn_text or "CONTINUE" in btn_text or "button-stepper" in btn_class:
                        save_buttons.append({
                            'index': i+1,
                            'text': btn.text.strip(),
                            'class': btn_class[:80] + "..." if len(btn_class) > 80 else btn_class
                        })
                except:
                    continue
            
            print(f"🎯 Botones relacionados con Save/Continue ({len(save_buttons)}):")
            for btn_info in save_buttons:
                print(f"   {btn_info['index']}. Texto: '{btn_info['text']}' | Clase: '{btn_info['class']}'")
                
        except Exception as e:
            print(f"❌ Error analizando botones Save/Continue: {e}")
    
    @staticmethod
    def analyze_modal_elements(driver):
        """
        Analiza elementos de modal en la página
        """
        try:
            # Buscar posibles modales
            modals = driver.find_elements(By.XPATH, "//div[contains(@class, 'modal') or contains(@class, 'dialog')]")
            print(f"📊 Se encontraron {len(modals)} posibles modales")
            
            for i, modal in enumerate(modals):
                try:
                    modal_text = modal.text.strip()[:100]
                    modal_class = modal.get_attribute("class") or ""
                    print(f"   {i+1}. Clase: '{modal_class}' | Texto: '{modal_text}...'")
                except:
                    continue
                    
        except Exception as e:
            print(f"❌ Error analizando modales: {e}") 