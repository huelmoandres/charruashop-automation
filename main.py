#!/usr/bin/env python3
"""
Sistema FDA Automation - Script Principal
Automatiza el proceso completo de login FDA y creación de Prior Notice

Sistema migrado con:
- Gestión automática de browser (SeleniumManager)
- Sistema de logging avanzado con performance tracking
- Screenshots automáticos en errores
- Rutas configurables para CSV y outputs
- Error handling robusto
- Configuración centralizada
"""

import sys
import time
from pathlib import Path
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait

# Imports de la nueva arquitectura
from src.constants.timeouts import SleepTimes, ElementTimeouts
from src.constants.messages import LogMessages, UserMessages, ProcessMessages
from src.constants.paths import ensure_directories, show_paths, ORDER_SAMPLE_FILE
from src.core.selenium_manager import SeleniumManager
from src.utils.selenium_helpers import WaitHelper

# Imports del sistema de logging avanzado
from src.core.logger import init_logging, get_logger
from src.core.performance import create_performance_tracker
from src.utils.screenshot_utils import create_screenshot_manager

# Imports del sistema FDA
from src.fda.authentication.fda_login import complete_fda_login
from src.fda.prior_notice.creation.step_01_selection import execute_step_01
from src.fda.prior_notice.creation.step_02_edit_information import execute_step_02
from src.fda.prior_notice.creation.step_03_final_save import execute_step_03

def setup_environment():
    """
    Configura el entorno inicial del sistema con logging mejorado
    """
    logger = get_logger()
    logger.info("🚀 SISTEMA FDA AUTOMATION INICIADO", module='main')
    
    print("🚀 SISTEMA FDA AUTOMATION")
    print("=" * 50)
    
    # Mostrar configuración actual de rutas
    logger.debug("Mostrando configuración de rutas", module='main')
    show_paths()
    
    # Crear directorios necesarios
    logger.debug("Creando directorios del sistema", module='main')
    ensure_directories()
    
    # Verificar archivo CSV
    if not ORDER_SAMPLE_FILE.exists():
        logger.warning(f"Archivo CSV no encontrado: {ORDER_SAMPLE_FILE}", module='main')
        print(f"\n⚠️ ARCHIVO CSV NO ENCONTRADO")
        print(f"📁 Se esperaba: {ORDER_SAMPLE_FILE}")
        print(f"💡 El archivo order_sample.csv debe estar en data/samples/")
        print(f"📋 El archivo debe contener: guia_aerea, order_number, shipping_name")
        
        user_continue = input(f"\n{UserMessages.CONTINUE_WITHOUT_CSV}").strip().lower()
        if user_continue not in ['s', 'si', 'yes', 'y']:
            logger.info("Proceso cancelado por el usuario (sin CSV)", module='main')
            print("❌ Proceso cancelado por el usuario")
            return False
    else:
        logger.info(f"Archivo CSV encontrado: {ORDER_SAMPLE_FILE}", module='main')
    
    logger.info("✅ Entorno configurado correctamente", module='main')
    print("\n✅ Entorno configurado correctamente")
    return True

def execute_prior_notice_creation(driver, performance_tracker, screenshot_manager):
    """
    Ejecuta el proceso completo de creación de Prior Notice con tracking
    """
    logger = get_logger()
    logger.info("🔄 Iniciando proceso de creación de Prior Notice", module='fda')
    
    print(LogMessages.STARTING_PROCESS.format(process="CREACIÓN DE PRIOR NOTICE"))
    print("=" * 60)
    
    try:
        # PASO 1: Copy Selection
        logger.info("📋 Ejecutando Paso 1: Copy Selection", module='fda')
        print(f"\n{ProcessMessages.STEP_INDICATOR.format(step=1, description='Copy Selection')}")
        
        with performance_tracker.track("fda_step_01_copy_selection"):
            step1_success = execute_step_01(driver, wait=SleepTimes.SHORT_WAIT)
        
        if not step1_success:
            logger.error("❌ Fallo en Paso 1 - Copy Selection", module='fda')
            if screenshot_manager:
                screenshot_manager.capture_error_screenshot(driver, "step1_copy_selection_failed")
            print(LogMessages.PROCESS_FAILED.format(process="Paso 1 - Copy Selection"))
            return False
        
        logger.info("✅ Paso 1 completado exitosamente", module='fda')
        if screenshot_manager:
            screenshot_manager.capture_success_screenshot(driver, "step1_copy_selection_completed")
        
        # Pausa entre pasos
        logger.debug(f"⏸️ Pausa entre pasos ({SleepTimes.BETWEEN_STEPS}s)", module='fda')
        print(f"⏸️ Pausa entre pasos...")
        time.sleep(SleepTimes.BETWEEN_STEPS)
        
        # PASO 2: Edit Information
        logger.info("📝 Ejecutando Paso 2: Edit Information", module='fda')
        print(f"\n{ProcessMessages.STEP_INDICATOR.format(step=2, description='Edit Information')}")
        
        with performance_tracker.track("fda_step_02_edit_information"):
            step2_success = execute_step_02(driver, wait=SleepTimes.SHORT_WAIT)
        
        if not step2_success:
            logger.error("❌ Fallo en Paso 2 - Edit Information", module='fda')
            if screenshot_manager:
                screenshot_manager.capture_error_screenshot(driver, "step2_edit_information_failed")
            print(LogMessages.PROCESS_FAILED.format(process="Paso 2 - Edit Information"))
            return False
        
        logger.info("✅ Paso 2 completado exitosamente", module='fda')
        if screenshot_manager:
            screenshot_manager.capture_success_screenshot(driver, "step2_edit_information_completed")
        
        # Pausa entre pasos
        logger.debug(f"⏸️ Pausa entre pasos ({SleepTimes.BETWEEN_STEPS}s)", module='fda')
        print(f"⏸️ Pausa entre pasos...")
        time.sleep(SleepTimes.BETWEEN_STEPS)
        
        # PASO 3: Final Save
        logger.info("💾 Ejecutando Paso 3: Final Save", module='fda')
        print(f"\n{ProcessMessages.STEP_INDICATOR.format(step=3, description='Final Save')}")
        
        with performance_tracker.track("fda_step_03_final_save"):
            step3_success = execute_step_03(driver, wait=SleepTimes.SHORT_WAIT)
        
        if not step3_success:
            logger.error("❌ Fallo en Paso 3 - Final Save", module='fda')
            if screenshot_manager:
                screenshot_manager.capture_error_screenshot(driver, "step3_final_save_failed")
            print(LogMessages.PROCESS_FAILED.format(process="Paso 3 - Final Save"))
            return False
        
        logger.info("✅ Paso 3 completado exitosamente", module='fda')
        if screenshot_manager:
            screenshot_manager.capture_success_screenshot(driver, "step3_final_save_completed")
        
        # Proceso completado
        logger.info("🎉 PROCESO DE PRIOR NOTICE COMPLETADO EXITOSAMENTE", module='fda')
        print(f"\n🎉 {LogMessages.PROCESS_COMPLETED.format(process='CREACIÓN DE PRIOR NOTICE')}")
        print(ProcessMessages.SUCCESS_SUMMARY)
        print("📊 Resumen de lo ejecutado:")
        print("   ✅ Paso 1: Copy Selection completado")
        print("   ✅ Paso 2: Edit Information completado")
        print("   ✅ Paso 3: Final Save completado")
        print("\n🔗 El Prior Notice debería estar listo en FDA")
        
        # Screenshot final de éxito
        if screenshot_manager:
            screenshot_manager.capture_success_screenshot(driver, "prior_notice_creation_completed")
        
        return True
        
    except KeyboardInterrupt:
        logger.warning("⏹️ Proceso interrumpido por el usuario", module='fda')
        print(f"\n⏹️ Proceso interrumpido por el usuario")
        return False
    except Exception as e:
        logger.error(f"❌ Error inesperado durante la creación: {e}", module='fda', exception=e)
        if screenshot_manager:
            screenshot_manager.capture_error_screenshot(driver, "prior_notice_creation_error", e)
        print(f"\n❌ Error inesperado durante la creación: {e}")
        print("🔍 Revisa los logs para más detalles")
        return False

def main():
    """
    Función principal del sistema FDA Automation con logging avanzado
    """
    # Generar ID único para esta sesión
    session_id = f"fda_automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Inicializar sistema de logging
    logger = init_logging(session_id)
    logger.info("🏗️ SISTEMA FDA AUTOMATION INICIADO", module='main')
    logger.info(f"Session ID: {session_id}", module='main')
    
    print("🏗️ SISTEMA FDA AUTOMATION")
    print("Automatización completa: Login + Prior Notice Creation")
    print(f"🔍 Session ID: {session_id}")
    print("=" * 60)
    
    # Inicializar sistemas de tracking
    performance_tracker = create_performance_tracker(logger)
    screenshot_manager = create_screenshot_manager(logger)
    
    # Setup del entorno
    if not setup_environment():
        logger.error("❌ Error en setup del entorno", module='main')
        print("❌ Error en setup del entorno")
        return
    
    # Confirmación del usuario
    user_confirm = input(f"\n{UserMessages.START_PROCESS}").strip().lower()
    if user_confirm not in ['s', 'si', 'yes', 'y']:
        logger.info("❌ Proceso cancelado por el usuario", module='main')
        print("❌ Proceso cancelado por el usuario")
        return
    
    logger.info("✅ Usuario confirmó inicio del proceso", module='main')
    
    try:
        # Usar SeleniumManager para gestión automática del driver
        with performance_tracker.track("selenium_initialization"):
            selenium_manager = SeleniumManager()
            driver = selenium_manager.start_driver()
        
        try:
            logger.info("🌐 Browser y driver inicializados correctamente", module='selenium')
            print(f"\n🌐 {ProcessMessages.BROWSER_READY}")
            
            # FASE 1: Login a FDA
            logger.info("🔐 Iniciando proceso de login a FDA", module='fda')
            print(f"\n{ProcessMessages.STEP_INDICATOR.format(step='LOGIN', description='Autenticación FDA')}")
            print(f"🔗 Navegando a sistema FDA...")
            
            with performance_tracker.track("fda_navigation"):
                driver.get("https://www.access.fda.gov")
                # Screenshot de navegación
                if screenshot_manager:
                    screenshot_manager.capture_step_screenshot(driver, "navigation_fda")
            
            # Esperar carga inicial
            with performance_tracker.track("page_load_wait"):
                WaitHelper.wait_for_page_load(driver, ElementTimeouts.PAGE_LOAD)
            
            # Ejecutar login
            with performance_tracker.track("fda_login_process"):
                login_success = complete_fda_login(driver, WebDriverWait(driver, ElementTimeouts.DEFAULT))
            
            if not login_success:
                logger.error("❌ Error en el proceso de login", module='fda')
                if screenshot_manager:
                    screenshot_manager.capture_error_screenshot(driver, "fda_login_failed")
                print("❌ Error en el proceso de login")
                return
            
            logger.info("✅ Login a FDA completado exitosamente", module='fda')
            if screenshot_manager:
                screenshot_manager.capture_success_screenshot(driver, "fda_login_success")
            print("✅ Login completado exitosamente")
            
            # FASE 2: Creación de Prior Notice
            logger.info("📋 Iniciando automatización de Prior Notice", module='fda')
            print(f"\n{ProcessMessages.STEP_INDICATOR.format(step='PRIOR_NOTICE', description='Automatización Prior Notice')}")
            print(f"💡 A partir de aquí, el proceso es mayormente automático")
            print(f"👤 Solo necesitarás ingresar la fecha cuando se solicite")
            
            # Ejecutar proceso de Prior Notice
            prior_notice_success = execute_prior_notice_creation(driver, performance_tracker, screenshot_manager)
            
            if prior_notice_success:
                logger.info("🎯 PROCESO COMPLETO EXITOSO", module='main')
                print(f"\n🎯 {ProcessMessages.FINAL_SUCCESS}")
                print("📸 Se pueden tomar screenshots finales...")
                print("📁 Archivos generados en:")
                print(f"   • Data: data/")
                print(f"   • Outputs: src/orders/output/")
                print(f"   • Logs: logs/")
                print(f"   • Screenshots: logs/screenshots/")
                
                # Mantener navegador abierto para verificación
                input(f"\n{UserMessages.KEEP_BROWSER_OPEN}")
            else:
                logger.error("❌ El proceso de Prior Notice no se completó exitosamente", module='main')
                print(f"\n❌ El proceso de Prior Notice no se completó exitosamente")
                print("🔍 Revisa los mensajes anteriores para identificar problemas")
                print("📄 Logs detallados disponibles en: logs/")
                print("📸 Screenshots de errores disponibles en: logs/screenshots/")
                
                # Mantener navegador para debug
                input("\n🔍 Navegador mantenido abierto para debug. Presiona Enter para cerrar...")
        
        finally:
            # Cerrar selenium manager
            if 'selenium_manager' in locals():
                selenium_manager.close_driver()
    
    except KeyboardInterrupt:
        logger.warning("⏹️ Proceso interrumpido por el usuario", module='main')
        print(f"\n⏹️ Proceso interrumpido por el usuario")
    except Exception as e:
        logger.critical(f"❌ Error crítico en el sistema: {e}", module='main', exception=e)
        print(f"\n❌ Error crítico en el sistema: {e}")
        print("🆘 Revisa la configuración del sistema")
        print(f"💡 Revisa la configuración en config/secrets.py")
        print("📄 Logs detallados en: logs/")
        
        # Screenshot de error crítico si hay driver disponible
        if 'driver' in locals() and screenshot_manager:
            try:
                screenshot_manager.capture_error_screenshot(driver, "critical_system_error", e)
            except:
                pass
    
    finally:
        # Log final con resumen de la sesión
        if performance_tracker:
            performance_tracker.log_session_summary()
        
        logger.info("👋 Sistema finalizado", module='main')
        print(f"\n👋 Sistema finalizado")
        print("💡 Tips para próxima ejecución:")
        print("   • Asegúrate de tener order.csv actualizado")
        print("   • Verifica que FDA no haya cambiado su interfaz")
        print("   • Revisa logs/ para análisis detallado")
        print("   • Screenshots en logs/screenshots/ para debugging visual")

if __name__ == "__main__":
    main() 