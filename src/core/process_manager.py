"""
Process Manager - Gestión centralizada de procesos de automatización
Refactoriza funciones largas en componentes pequeños y reutilizables
"""

import time
from datetime import datetime
from typing import Optional, Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from ..constants.enums import (
    ProcessStep, ProcessResult, SystemConfiguration, 
    UserResponse, ProcessError, SystemModule
)
from ..constants.timeouts import SleepTimes, ElementTimeouts
from ..constants.messages import ProcessMessages, LogMessages, UserMessages
from ..fda.prior_notice.creation.step_01_selection import execute_step_01
from ..fda.prior_notice.creation.step_02_edit_information import execute_step_02
from ..fda.prior_notice.creation.step_03_final_save import execute_step_03
from ..fda.authentication.fda_login import complete_fda_login
from ..utils.selenium_helpers import WaitHelper


class ProcessManager:
    """Gestor centralizado de procesos de automatización"""
    
    def __init__(self, logger, performance_tracker=None, screenshot_manager=None):
        self.logger = logger
        self.performance_tracker = performance_tracker
        self.screenshot_manager = screenshot_manager
        
    def initialize_session(self, operation_type: str) -> SystemConfiguration:
        """Inicializa una nueva sesión del sistema"""
        session_id = f"{operation_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        config = SystemConfiguration(
            session_id=session_id,
            operation_type=operation_type,
            debug_mode=False,
            screenshot_enabled=self.screenshot_manager is not None,
            performance_tracking=self.performance_tracker is not None
        )
        
        self.logger.info(f"🏗️ Nueva sesión iniciada: {session_id}", module=SystemModule.MAIN.value)
        return config
        
    def get_user_confirmation(self, message: str) -> bool:
        """Obtiene confirmación del usuario con validación mejorada"""
        user_input = input(f"\n{message}").strip()
        response = UserResponse.from_string(user_input)
        
        if response == UserResponse.YES:
            self.logger.info("✅ Usuario confirmó la acción", module=SystemModule.MAIN.value)
            return True
        elif response == UserResponse.NO:
            self.logger.info("❌ Usuario canceló la acción", module=SystemModule.MAIN.value)
            return False
        else:
            print("⚠️ Respuesta no válida. Por favor responde 's' o 'n'")
            return self.get_user_confirmation(message)
    
    def execute_navigation(self, driver: WebDriver, url: str) -> ProcessResult:
        """Ejecuta navegación con tracking y manejo de errores"""
        try:
            self.logger.info(f"🔗 Navegando a: {url}", module=SystemModule.SELENIUM.value)
            
            if self.performance_tracker:
                with self.performance_tracker.track("navigation"):
                    driver.get(url)
            else:
                driver.get(url)
            
            # Screenshot de navegación
            if self.screenshot_manager:
                self.screenshot_manager.capture_step_screenshot(driver, "navigation")
            
            # Esperar carga
            if self.performance_tracker:
                with self.performance_tracker.track("page_load_wait"):
                    WaitHelper.wait_for_page_load(driver, ElementTimeouts.PAGE_LOAD)
            else:
                WaitHelper.wait_for_page_load(driver, ElementTimeouts.PAGE_LOAD)
            
            return ProcessResult(
                success=True,
                step=ProcessStep.LOGIN,
                message=f"Navegación exitosa a {url}"
            )
            
        except Exception as e:
            error_msg = f"Error en navegación a {url}: {e}"
            self.logger.error(error_msg, module=SystemModule.SELENIUM.value, exception=e)
            
            if self.screenshot_manager:
                self.screenshot_manager.capture_error_screenshot(driver, "navigation_error", e)
            
            return ProcessResult(
                success=False,
                step=ProcessStep.LOGIN,
                message="Error en navegación",
                error=error_msg
            )
    
    def execute_login_process(self, driver: WebDriver) -> ProcessResult:
        """Ejecuta proceso de login con manejo mejorado"""
        try:
            self.logger.info("🔐 Iniciando proceso de login", module=SystemModule.FDA.value)
            print(f"\n{ProcessMessages.STEP_INDICATOR.format(step='LOGIN', description='Autenticación FDA')}")
            
            if self.performance_tracker:
                with self.performance_tracker.track("fda_login_process"):
                    login_success = complete_fda_login(driver, WebDriverWait(driver, ElementTimeouts.DEFAULT))
            else:
                login_success = complete_fda_login(driver, WebDriverWait(driver, ElementTimeouts.DEFAULT))
            
            if login_success:
                self.logger.info("✅ Login completado exitosamente", module=SystemModule.FDA.value)
                if self.screenshot_manager:
                    self.screenshot_manager.capture_success_screenshot(driver, "fda_login_success")
                
                return ProcessResult(
                    success=True,
                    step=ProcessStep.LOGIN,
                    message="Login exitoso"
                )
            else:
                error_msg = "Error en el proceso de login"
                self.logger.error(error_msg, module=SystemModule.FDA.value)
                if self.screenshot_manager:
                    self.screenshot_manager.capture_error_screenshot(driver, "fda_login_failed")
                
                return ProcessResult(
                    success=False,
                    step=ProcessStep.LOGIN,
                    message="Login fallido",
                    error=error_msg
                )
                
        except Exception as e:
            error_msg = f"Error inesperado en login: {e}"
            self.logger.error(error_msg, module=SystemModule.FDA.value, exception=e)
            
            if self.screenshot_manager:
                self.screenshot_manager.capture_error_screenshot(driver, "login_exception", e)
            
            return ProcessResult(
                success=False,
                step=ProcessStep.LOGIN,
                message="Error inesperado en login",
                error=error_msg
            )
    
    def execute_step_with_tracking(self, driver: WebDriver, step: ProcessStep, 
                                  step_function, *args, **kwargs) -> ProcessResult:
        """Ejecuta un paso con tracking, logging y manejo de errores unificado"""
        step_name = step.value
        step_descriptions = {
            ProcessStep.STEP_01_SELECTION: "Copy Selection",
            ProcessStep.STEP_02_EDIT_INFO: "Edit Information", 
            ProcessStep.STEP_03_FINAL_SAVE: "Final Save"
        }
        
        description = step_descriptions.get(step, step_name)
        
        try:
            self.logger.info(f"🚀 Ejecutando {description}", module=SystemModule.FDA.value)
            print(f"\n{ProcessMessages.STEP_INDICATOR.format(step=step_name, description=description)}")
            
            # Ejecutar con tracking
            if self.performance_tracker:
                track_name = f"fda_{step_name.lower()}"
                with self.performance_tracker.track(track_name):
                    success = step_function(driver, *args, **kwargs)
            else:
                success = step_function(driver, *args, **kwargs)
            
            if success:
                self.logger.info(f"✅ {description} completado exitosamente", module=SystemModule.FDA.value)
                if self.screenshot_manager:
                    screenshot_name = f"{step_name.lower()}_completed"
                    self.screenshot_manager.capture_success_screenshot(driver, screenshot_name)
                
                # Pausa entre pasos
                self._pause_between_steps()
                
                return ProcessResult(
                    success=True,
                    step=step,
                    message=f"{description} completado"
                )
            else:
                error_msg = f"Fallo en {description}"
                self.logger.error(error_msg, module=SystemModule.FDA.value)
                if self.screenshot_manager:
                    screenshot_name = f"{step_name.lower()}_failed"
                    self.screenshot_manager.capture_error_screenshot(driver, screenshot_name)
                
                return ProcessResult(
                    success=False,
                    step=step,
                    message=f"{description} falló",
                    error=error_msg
                )
                
        except Exception as e:
            error_msg = f"Error inesperado en {description}: {e}"
            self.logger.error(error_msg, module=SystemModule.FDA.value, exception=e)
            
            if self.screenshot_manager:
                screenshot_name = f"{step_name.lower()}_error"
                self.screenshot_manager.capture_error_screenshot(driver, screenshot_name, e)
            
            return ProcessResult(
                success=False,
                step=step,
                message=f"Error en {description}",
                error=error_msg
            )
    
    def _pause_between_steps(self):
        """Pausa configurada entre pasos"""
        self.logger.debug(f"⏸️ Pausa entre pasos ({SleepTimes.BETWEEN_STEPS}s)", module=SystemModule.FDA.value)
        print(f"⏸️ Pausa entre pasos...")
        time.sleep(SleepTimes.BETWEEN_STEPS)
    
    def execute_navigation_to_prior_notice_system(self, driver: WebDriver) -> ProcessResult:
        """
        Ejecuta navegación específica al Prior Notice System Interface
        Este paso es OBLIGATORIO después del login y antes de los steps
        """
        try:
            self.logger.info("🏛️ Navegando al Prior Notice System Interface", module=SystemModule.FDA.value)
            print(f"\n{ProcessMessages.STEP_INDICATOR.format(step='NAVIGATION', description='Prior Notice System Interface')}")
            
            # Importar aquí para evitar import circular
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support import expected_conditions as EC
            
            # Crear wait para esta navegación
            wait = WebDriverWait(driver, ElementTimeouts.DEFAULT)
            
            if self.performance_tracker:
                with self.performance_tracker.track("navigate_to_prior_notice_system"):
                    # Paso 1: Buscar enlace "Prior Notice System Interface"
                    self.logger.info("🔍 Buscando enlace 'Prior Notice System Interface'", module=SystemModule.FDA.value)
                    print("🔍 Buscando enlace 'Prior Notice System Interface'...")
                    
                    prior_notice_link = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//a[@title='Prior Notice System Interface']"))
                    )
                    
                    prior_notice_link.click()
                    self.logger.info("✅ Navegando a Prior Notice System Interface", module=SystemModule.FDA.value)
                    print("✅ Accediendo a Prior Notice System Interface")
                    
                    # Pausa para carga
                    time.sleep(SleepTimes.FORM_LOAD)
                    
                    # Paso 2: Navegar a submissions
                    self.logger.info("🔍 Buscando botón 'submissions'", module=SystemModule.FDA.value)
                    print("🔍 Buscando botón 'submissions'...")
                    
                    submissions_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@routerlink='/submissions']"))
                    )
                    
                    submissions_button.click()
                    self.logger.info("✅ Navegando a Previous Submissions & Drafts", module=SystemModule.FDA.value)
                    print("✅ Accediendo a Previous Submissions & Drafts")
                    
                    # Pausa para carga de tabla
                    time.sleep(SleepTimes.FORM_LOAD)
                    
                    # Paso 3: Buscar y seleccionar prior notice en la tabla
                    self.logger.info("🔍 Buscando tabla de prior notices", module=SystemModule.FDA.value)
                    print("🔍 Buscando tabla de prior notices...")
                    
                    # Esperar a que aparezca la tabla
                    from src.constants.selectors import FDASelectors
                    table = wait.until(
                        EC.presence_of_element_located((By.XPATH, FDASelectors.PRIOR_NOTICE_TABLE))
                    )
                    self.logger.info("✅ Tabla de prior notices encontrada", module=SystemModule.FDA.value)
                    print("✅ Tabla encontrada")
                    
                    # Buscar filas de la tabla
                    self.logger.info("🔍 Buscando filas en la tabla", module=SystemModule.FDA.value)
                    print("🔍 Buscando prior notices disponibles...")
                    
                    table_rows = wait.until(
                        EC.presence_of_all_elements_located((By.XPATH, FDASelectors.TABLE_ROWS))
                    )
                    
                    if not table_rows:
                        raise Exception("No se encontraron prior notices en la tabla")
                    
                    self.logger.info(f"✅ Encontradas {len(table_rows)} filas en la tabla", module=SystemModule.FDA.value)
                    print(f"✅ Encontrados {len(table_rows)} prior notices")
                    
                    # Seleccionar el primer prior notice (el más reciente)
                    first_row = table_rows[0]
                    self.logger.info("🎯 Seleccionando el primer prior notice", module=SystemModule.FDA.value)
                    print("🎯 Seleccionando el primer prior notice...")
                    
                    # Buscar botón "Copy" en la primera fila
                    copy_button = first_row.find_element(By.XPATH, FDASelectors.COPY_BUTTON)
                    
                    if not copy_button:
                        raise Exception("No se encontró el botón 'Copy' en el prior notice seleccionado")
                    
                    copy_button.click()
                    self.logger.info("✅ Botón 'Copy' clickeado exitosamente", module=SystemModule.FDA.value)
                    print("✅ Prior notice seleccionado para copiar")
                    
                    # Pausa para procesamiento
                    time.sleep(SleepTimes.SAVE_PROCESSING)
            else:
                # Mismo proceso sin tracking
                self.logger.info("🔍 Buscando enlace 'Prior Notice System Interface'", module=SystemModule.FDA.value)
                print("🔍 Buscando enlace 'Prior Notice System Interface'...")
                
                prior_notice_link = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@title='Prior Notice System Interface']"))
                )
                
                prior_notice_link.click()
                self.logger.info("✅ Navegando a Prior Notice System Interface", module=SystemModule.FDA.value)
                print("✅ Accediendo a Prior Notice System Interface")
                
                time.sleep(SleepTimes.FORM_LOAD)
                
                self.logger.info("🔍 Buscando botón 'submissions'", module=SystemModule.FDA.value)
                print("🔍 Buscando botón 'submissions'...")
                
                submissions_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@routerlink='/submissions']"))
                )
                
                submissions_button.click()
                self.logger.info("✅ Navegando a Previous Submissions & Drafts", module=SystemModule.FDA.value)
                print("✅ Accediendo a Previous Submissions & Drafts")
                
                time.sleep(SleepTimes.FORM_LOAD)
                
                # Paso 3: Buscar y seleccionar prior notice en la tabla
                self.logger.info("🔍 Buscando tabla de prior notices", module=SystemModule.FDA.value)
                print("🔍 Buscando tabla de prior notices...")
                
                # Esperar a que aparezca la tabla
                from src.constants.selectors import FDASelectors
                table = wait.until(
                    EC.presence_of_element_located((By.XPATH, FDASelectors.PRIOR_NOTICE_TABLE))
                )
                self.logger.info("✅ Tabla de prior notices encontrada", module=SystemModule.FDA.value)
                print("✅ Tabla encontrada")
                
                # Buscar filas de la tabla
                self.logger.info("🔍 Buscando filas en la tabla", module=SystemModule.FDA.value)
                print("🔍 Buscando prior notices disponibles...")
                
                table_rows = wait.until(
                    EC.presence_of_all_elements_located((By.XPATH, FDASelectors.TABLE_ROWS))
                )
                
                if not table_rows:
                    raise Exception("No se encontraron prior notices en la tabla")
                
                self.logger.info(f"✅ Encontradas {len(table_rows)} filas en la tabla", module=SystemModule.FDA.value)
                print(f"✅ Encontrados {len(table_rows)} prior notices")
                
                # Seleccionar el primer prior notice (el más reciente)
                first_row = table_rows[0]
                self.logger.info("🎯 Seleccionando el primer prior notice", module=SystemModule.FDA.value)
                print("🎯 Seleccionando el primer prior notice...")
                
                # Buscar botón "Copy" en la primera fila
                copy_button = first_row.find_element(By.XPATH, FDASelectors.COPY_BUTTON)
                
                if not copy_button:
                    raise Exception("No se encontró el botón 'Copy' en el prior notice seleccionado")
                
                copy_button.click()
                self.logger.info("✅ Botón 'Copy' clickeado exitosamente", module=SystemModule.FDA.value)
                print("✅ Prior notice seleccionado para copiar")
                
                # Pausa para procesamiento
                time.sleep(SleepTimes.SAVE_PROCESSING)
            
            # Screenshot de confirmación
            if self.screenshot_manager:
                self.screenshot_manager.capture_step_screenshot(driver, "prior_notice_system_navigation")
            
            self.logger.info("🎯 Navegación y selección de prior notice completada", module=SystemModule.FDA.value)
            print("🎯 Prior notice seleccionado - Listo para crear copia")
            
            return ProcessResult(
                success=True,
                step=ProcessStep.NAVIGATION,
                message="Navegación y selección de prior notice exitosa"
            )
            
        except Exception as e:
            error_msg = f"Error navegando al Prior Notice System: {e}"
            self.logger.error(error_msg, module=SystemModule.FDA.value, exception=e)
            
            if self.screenshot_manager:
                self.screenshot_manager.capture_error_screenshot(driver, "prior_notice_navigation_error", e)
            
            return ProcessResult(
                success=False,
                step=ProcessStep.NAVIGATION,
                message="Error en navegación al Prior Notice System",
                error=error_msg
            )
    
    def execute_complete_prior_notice_process(self, driver: WebDriver) -> ProcessResult:
        """Ejecuta el proceso completo de Prior Notice con manejo estructurado"""
        try:
            self.logger.info("📋 Iniciando automatización de Prior Notice", module=SystemModule.FDA.value)
            print(f"\n{ProcessMessages.STEP_INDICATOR.format(step='PRIOR_NOTICE', description='Automatización Prior Notice')}")
            print(f"💡 El proceso es mayormente automático")
            print(f"👤 Solo necesitarás ingresar la fecha cuando se solicite")
            
            # PASO 0: Navegación y selección de prior notice (NUEVO - OBLIGATORIO)
            print("\n🏛️ Navegando al Prior Notice System y seleccionando prior notice...")
            navigation_result = self.execute_navigation_to_prior_notice_system(driver)
            
            if not navigation_result.success:
                return navigation_result
            
            print("✅ Prior notice seleccionado para copiar")
            
            # PASO 1: Copy Selection
            result_step1 = self.execute_step_with_tracking(
                driver, ProcessStep.STEP_01_SELECTION,
                execute_step_01, SleepTimes.SHORT_WAIT
            )
            
            if not result_step1.success:
                return result_step1
            
            # PASO 2: Edit Information
            result_step2 = self.execute_step_with_tracking(
                driver, ProcessStep.STEP_02_EDIT_INFO,
                execute_step_02, wait=SleepTimes.SHORT_WAIT
            )
            
            if not result_step2.success:
                return result_step2
            
            # PASO 3: Final Save
            result_step3 = self.execute_step_with_tracking(
                driver, ProcessStep.STEP_03_FINAL_SAVE,
                execute_step_03, wait=SleepTimes.SHORT_WAIT
            )
            
            if not result_step3.success:
                return result_step3
            
            # Proceso completado exitosamente
            self.logger.info("🎉 PROCESO DE PRIOR NOTICE COMPLETADO EXITOSAMENTE", module=SystemModule.FDA.value)
            self._show_success_summary()
            
            # Screenshot final
            if self.screenshot_manager:
                self.screenshot_manager.capture_success_screenshot(driver, "prior_notice_creation_completed")
            
            return ProcessResult(
                success=True,
                step=ProcessStep.COMPLETED,
                message="Prior Notice creado exitosamente"
            )
            
        except KeyboardInterrupt:
            self.logger.warning("⏹️ Proceso interrumpido por el usuario", module=SystemModule.FDA.value)
            return ProcessResult(
                success=False,
                step=ProcessStep.COMPLETED,
                message="Proceso interrumpido por usuario",
                error="KeyboardInterrupt"
            )
        except Exception as e:
            error_msg = f"Error inesperado durante la creación: {e}"
            self.logger.error(error_msg, module=SystemModule.FDA.value, exception=e)
            
            if self.screenshot_manager:
                self.screenshot_manager.capture_error_screenshot(driver, "prior_notice_creation_error", e)
            
            return ProcessResult(
                success=False,
                step=ProcessStep.COMPLETED,
                message="Error en proceso de Prior Notice",
                error=error_msg
            )
    
    def _show_success_summary(self):
        """Muestra resumen de éxito estandarizado"""
        print(f"\n🎉 {LogMessages.PROCESS_COMPLETED.format(process='CREACIÓN DE PRIOR NOTICE')}")
        print(ProcessMessages.SUCCESS_SUMMARY)
        print("📊 Resumen de lo ejecutado:")
        print("   ✅ Navegación: Prior notice seleccionado de la tabla")
        print("   ✅ Paso 1: Copy Selection completado")
        print("   ✅ Paso 2: Edit Information completado")
        print("   ✅ Paso 3: Final Save completado")
        print("\n🔗 El Prior Notice debería estar listo en FDA")
    
    def show_final_status(self, success: bool, operation_type: str):
        """Muestra estado final con información útil"""
        if success:
            print(f"\n🎯 {ProcessMessages.FINAL_SUCCESS}")
            print("📸 Se pueden tomar screenshots finales...")
            print("📁 Archivos generados en:")
            print(f"   • Data: data/")
            print(f"   • Outputs: src/orders/output/")
            print(f"   • Logs: logs/")
            print(f"   • Screenshots: logs/screenshots/")
        else:
            print(f"\n❌ El proceso de {operation_type} no se completó exitosamente")
            print("🔍 Revisa los mensajes anteriores para identificar problemas")
            print("📄 Logs detallados disponibles en: logs/")
            print("📸 Screenshots de errores disponibles en: logs/screenshots/")
        
        # Tips para próxima ejecución
        print(f"\n💡 Tips para próxima ejecución:")
        print("   • Asegúrate de tener order.csv actualizado")
        print("   • Verifica que FDA no haya cambiado su interfaz")
        print("   • Revisa logs/ para análisis detallado")
        print("   • Screenshots en logs/screenshots/ para debugging visual")
    
    def log_session_summary(self):
        """Log final con resumen de la sesión"""
        if self.performance_tracker:
            self.performance_tracker.log_session_summary()
        
        self.logger.info("👋 Sistema finalizado", module=SystemModule.MAIN.value) 