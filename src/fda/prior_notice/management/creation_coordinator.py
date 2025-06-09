"""
Coordinador de creación de Prior Notices
Maneja el flujo completo de creación paso a paso
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from src.core.selenium_config import setup_chrome_driver, setup_wait
from src.fda.authentication import complete_fda_login
from ..creation.step_01_copy_selection import complete_step_01_copy_selection
from ..creation.step_02_edit_information import execute_step_02
from ..creation.step_03_final_save import complete_step_03_final_save
import time

def navigate_to_prior_notice_system_only(driver, wait):
    """
    Solo navega al Prior Notice System sin hacer la copia
    """
    try:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC
        
        print("🔍 Navegando al Prior Notice System...")
        
        # Buscar el enlace del Prior Notice System Interface
        prior_notice_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@title='Prior Notice System Interface']"))
        )
        
        prior_notice_link.click()
        print("✅ Navegando a Prior Notice System Interface")
        
        time.sleep(2)
        
        # Navegar a submissions
        submissions_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@routerlink='/submissions']"))
        )
        
        submissions_button.click()
        print("✅ Navegando a Previous Submissions & Drafts")
        
        time.sleep(2)
        return True
        
    except Exception as e:
        print(f"❌ Error navegando al Prior Notice System: {e}")
        return False

def execute_creation_steps(driver, wait):
    """
    Ejecuta solo los pasos de creación (sin login inicial)
    Para usar cuando ya se tiene una sesión activa
    """
    print("🚀 EJECUTANDO PASOS DE CREACIÓN DE PRIOR NOTICE")
    print("=" * 50)
    
    try:
        # Paso 1: Copy with no food articles
        print("\n1️⃣ EJECUTANDO PASO 1: COPY SELECTION")
        if not complete_step_01_copy_selection(driver, wait):
            print("❌ Error en Paso 1")
            return False
        
        print("\n✅ Paso 1 completado exitosamente")
        print("⏳ Esperando entre pasos...")
        time.sleep(2)
        
        # Paso 2: Edit Information
        print("\n2️⃣ EJECUTANDO PASO 2: EDIT INFORMATION")
        if not execute_step_02(driver):
            print("❌ Error en Paso 2")
            return False
        
        print("\n✅ Paso 2 completado exitosamente")
        
        # Paso 3: Final Save
        print("\n3️⃣ EJECUTANDO PASO 3: FINAL SAVE")
        if not complete_step_03_final_save(driver, wait):
            print("❌ Error en Paso 3")
            return False
        
        print("\n✅ Paso 3 completado exitosamente")
        
        # Resumen final
        print("\n🎉 PASOS DE CREACIÓN COMPLETADOS")
        print("=" * 50)
        print("✅ Pasos ejecutados:")
        print("   1️⃣ Copy with no food articles")
        print("   2️⃣ Edit Information (trackingNumber, state, portOfArrivalDate)")
        print("   3️⃣ Final Save")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en pasos de creación: {e}")
        return False

def coordinate_prior_notice_creation():
    """
    Coordina todo el proceso de creación de Prior Notice
    """
    print("🚀 INICIANDO COORDINADOR DE CREACIÓN DE PRIOR NOTICE")
    print("=" * 60)
    
    driver = None
    
    try:
        # Configurar driver
        print("🔧 Configurando driver de Selenium...")
        driver = setup_chrome_driver()
        wait = setup_wait(driver)
        
        # Paso previo: Login y navegación
        print("\n🏛️ Ejecutando login y navegación inicial...")
        if not complete_fda_login(driver, wait):
            print("❌ Error en login FDA")
            return False
        
        if not navigate_to_prior_notice_system_only(driver, wait):
            print("❌ Error navegando al Prior Notice System")
            return False
        
        # Ejecutar pasos de creación
        if execute_creation_steps(driver, wait):
            print("\n🎉 PROCESO COMPLETO TERMINADO")
            print("💡 El Prior Notice está listo para continuar con pasos adicionales")
            
            # Mantener navegador abierto
            input("\n⏸️ Presiona Enter para cerrar el navegador...")
            
            return True
        else:
            print("❌ Error en los pasos de creación")
            return False
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Proceso interrumpido por el usuario")
        return False
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
        
    finally:
        if driver:
            driver.quit()
            print("🔧 Driver cerrado")

def test_individual_steps():
    """
    Función para probar pasos individuales
    """
    print("🧪 MODO TESTING - PASOS INDIVIDUALES")
    print("=" * 50)
    
    print("Selecciona qué paso quieres probar:")
    print("1. Solo Paso 1 (Copy Selection)")
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
            complete_step_01_copy_selection(driver, wait)
        elif choice == 2:
            # Para paso 2 necesitamos haber ejecutado paso 1 primero
            print("⚠️ Para probar Paso 2, primero ejecutamos Paso 1...")
            if complete_step_01_copy_selection(driver, wait):
                time.sleep(2)  # Reducido
                execute_step_02(driver)
        elif choice == 3:
            # Para paso 3 necesitamos haber ejecutado paso 2 primero
            print("⚠️ Para probar Paso 3, primero ejecutamos Paso 2...")
            if execute_step_02(driver):
                time.sleep(1.5)  # Reducido
                complete_step_03_final_save(driver, wait)
        elif choice == 4:
            if complete_step_01_copy_selection(driver, wait):
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