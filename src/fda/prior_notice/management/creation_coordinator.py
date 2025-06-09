"""
Coordinador de creación de Prior Notices
Maneja el flujo completo de creación paso a paso
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from src.core.selenium_config import setup_chrome_driver, setup_wait
from src.fda.authentication import complete_fda_login
from ..creation.step_01_selection import complete_step_01_selection
from ..creation.step_02_edit_information import execute_step_02
from ..creation.step_03_final_save import complete_step_03_final_save
from src.core.logger import AutomationLogger
from src.core.performance import PerformanceTracker
import time

# Inicializar logger
logger = AutomationLogger.get_instance()
performance = PerformanceTracker.get_instance()

def navigate_to_prior_notice_system_only(driver, wait):
    """
    Solo navega al Prior Notice System sin hacer la copia
    """
    logger.fda_logger.info("=== NAVEGANDO AL PRIOR NOTICE SYSTEM ===")
    
    try:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC
        
        logger.fda_logger.debug("Buscando enlace del Prior Notice System Interface")
        
        # Buscar el enlace del Prior Notice System Interface
        prior_notice_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@title='Prior Notice System Interface']"))
        )
        
        prior_notice_link.click()
        logger.fda_logger.info("✅ Navegando a Prior Notice System Interface")
        
        time.sleep(2)
        
        # Navegar a submissions
        logger.fda_logger.debug("Buscando botón de submissions")
        submissions_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@routerlink='/submissions']"))
        )
        
        submissions_button.click()
        logger.fda_logger.info("✅ Navegando a Previous Submissions & Drafts")
        
        time.sleep(2)
        logger.fda_logger.info("=== NAVEGACIÓN AL PRIOR NOTICE SYSTEM COMPLETADA ===")
        return True
        
    except Exception as e:
        logger.fda_logger.error("Error navegando al Prior Notice System", extra={"error": str(e)})
        logger.error_logger.error("Prior Notice System navigation failed", extra={
            "source_module": "fda_creation_coordinator",
            "function": "navigate_to_prior_notice_system_only",
            "error": str(e)
        })
        return False

def execute_creation_steps(driver, wait):
    """
    Ejecuta solo los pasos de creación (sin login inicial)
    Para usar cuando ya se tiene una sesión activa
    """
    logger.fda_logger.info("🚀 EJECUTANDO PASOS DE CREACIÓN DE PRIOR NOTICE")
    
    try:
        with performance.measure("prior_notice_creation_complete"):
            # Paso 1: Selection no food articles
            logger.fda_logger.info("1️⃣ EJECUTANDO PASO 1: SELECTION")
            
            with performance.measure("step_01_selection"):
                if not complete_step_01_selection(driver, wait):
                    logger.fda_logger.error("❌ Error en Paso 1")
                    return False
            
            logger.fda_logger.info("✅ Paso 1 completado exitosamente")
            logger.fda_logger.debug("Esperando entre pasos...")
            time.sleep(2)
            
            # Paso 2: Edit Information
            logger.fda_logger.info("2️⃣ EJECUTANDO PASO 2: EDIT INFORMATION")
            
            with performance.measure("step_02_edit_information"):
                if not execute_step_02(driver):
                    logger.fda_logger.error("❌ Error en Paso 2")
                    return False
            
            logger.fda_logger.info("✅ Paso 2 completado exitosamente")
            
            # Paso 3: Final Save
            logger.fda_logger.info("3️⃣ EJECUTANDO PASO 3: FINAL SAVE")
            
            with performance.measure("step_03_final_save"):
                if not complete_step_03_final_save(driver, wait):
                    logger.fda_logger.error("❌ Error en Paso 3")
                    return False
            
            logger.fda_logger.info("✅ Paso 3 completado exitosamente")
            
            # Resumen final
            logger.fda_logger.info("🎉 PASOS DE CREACIÓN COMPLETADOS")
            logger.fda_logger.info("✅ Pasos ejecutados:", extra={
                "step_1": "Selection (no food articles)",
                "step_2": "Edit Information (trackingNumber, state, portOfArrivalDate)",
                "step_3": "Final Save"
            })
            
            return True
        
    except Exception as e:
        logger.fda_logger.error("Error en pasos de creación", extra={"error": str(e)})
        logger.error_logger.error("Creation steps failed", extra={
            "source_module": "fda_creation_coordinator",
            "function": "execute_creation_steps",
            "error": str(e)
        })
        return False

def coordinate_prior_notice_creation():
    """
    Coordina todo el proceso de creación de Prior Notice
    """
    logger.fda_logger.info("🚀 INICIANDO COORDINADOR DE CREACIÓN DE PRIOR NOTICE")
    
    session_id = f"prior_notice_creation_{int(time.time())}"
    logger.start_session(session_id)
    
    driver = None
    
    try:
        with performance.measure("complete_prior_notice_coordination"):
            # Configurar driver
            logger.fda_logger.info("🔧 Configurando driver de Selenium...")
            driver = setup_chrome_driver()
            wait = setup_wait(driver)
            
            # Paso previo: Login y navegación
            logger.fda_logger.info("🏛️ Ejecutando login y navegación inicial...")
            
            with performance.measure("fda_login_and_navigation"):
                if not complete_fda_login(driver, wait):
                    logger.fda_logger.error("❌ Error en login FDA")
                    return False
                
                if not navigate_to_prior_notice_system_only(driver, wait):
                    logger.fda_logger.error("❌ Error navegando al Prior Notice System")
                    return False
            
            # Ejecutar pasos de creación
            if execute_creation_steps(driver, wait):
                logger.fda_logger.info("🎉 PROCESO COMPLETO TERMINADO")
                logger.fda_logger.info("💡 El Prior Notice está listo para continuar con pasos adicionales")
                
                # Mostrar resumen de performance
                performance.print_summary()
                
                # Mantener navegador abierto
                input("\n⏸️ Presiona Enter para cerrar el navegador...")
                
                return True
            else:
                logger.fda_logger.error("❌ Error en los pasos de creación")
                return False
        
    except KeyboardInterrupt:
        logger.fda_logger.warning("⚠️ Proceso interrumpido por el usuario")
        return False
        
    except Exception as e:
        logger.fda_logger.error("Error inesperado en coordinador", extra={"error": str(e)})
        logger.error_logger.error("Coordination process failed", extra={
            "source_module": "fda_creation_coordinator",
            "function": "coordinate_prior_notice_creation",
            "error": str(e)
        })
        return False
        
    finally:
        if driver:
            driver.quit()
            logger.fda_logger.info("�� Driver cerrado")

def test_individual_steps():
    """
    Función para probar pasos individuales
    """
    print("🧪 MODO TESTING - PASOS INDIVIDUALES")
    print("=" * 50)
    
    print("Selecciona qué paso quieres probar:")
    print("1. Solo Paso 1 (Selection)")
    print("2. Solo Paso 2 (Edit Information)")
    print("3. Solo Paso 3 (Final Save)")
    print("4. Ambos pasos en secuencia")
    print("5. Debug - Inspeccionar elementos")
    
    try:
        choice = int(input("\nSelecciona opción (1-5): "))
        
        driver = setup_chrome_driver()
        wait = setup_wait(driver)
        
        # Login inicial requerido para cualquier opción
        print("\n🏛️ Ejecutando login inicial...")
        if not complete_fda_login(driver, wait):
            print("❌ Error en login")
            return
        
        if not navigate_to_prior_notice_system_only(driver, wait):
            print("❌ Error navegando al sistema")
            return
        
        if choice == 1:
            complete_step_01_selection(driver, wait)
        elif choice == 2:
            # Para paso 2 necesitamos haber ejecutado paso 1 primero
            print("⚠️ Para probar Paso 2, primero ejecutamos Paso 1...")
            if complete_step_01_selection(driver, wait):
                time.sleep(2)  # Reducido
                execute_step_02(driver)
        elif choice == 3:
            # Para paso 3 necesitamos haber ejecutado paso 2 primero
            print("⚠️ Para probar Paso 3, primero ejecutamos Paso 2...")
            if execute_step_02(driver):
                time.sleep(1.5)  # Reducido
                complete_step_03_final_save(driver, wait)
        elif choice == 4:
            if complete_step_01_selection(driver, wait):
                time.sleep(2)  # Reducido
                if execute_step_02(driver):
                    time.sleep(1.5)  # Reducido
                    complete_step_03_final_save(driver, wait)
        elif choice == 5:
            from .step_02_edit_information import debug_step_02
            debug_step_02(driver)
        
        input("\n⏸️ Presiona Enter para cerrar...")
        driver.quit()
        
    except ValueError:
        print("❌ Entrada inválida")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🎯 COORDINADOR DE PRIOR NOTICE CREATION")
    print("=" * 60)
    
    print("Selecciona modo de ejecución:")
    print("1. Proceso completo (Recomendado)")
    print("2. Testing individual de pasos")
    
    try:
        mode = int(input("\nSelecciona modo (1-2): "))
        
        if mode == 1:
            coordinate_prior_notice_creation()
        elif mode == 2:
            test_individual_steps()
        else:
            print("❌ Opción inválida")
            
    except ValueError:
        print("❌ Entrada inválida")
    except KeyboardInterrupt:
        print("\n👋 Operación cancelada") 