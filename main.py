#!/usr/bin/env python3
"""
Sistema FDA Automation - Script Principal
Automatiza el proceso completo de login FDA y creación de Prior Notice

Sistema migrado con:
- Gestión automática de browser (SeleniumManager)
- Rutas configurables para CSV y outputs
- Error handling robusto
- Configuración centralizada
"""

import sys
import time
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait

# Imports de la nueva arquitectura
from src.constants.timeouts import SleepTimes, ElementTimeouts
from src.constants.messages import LogMessages, UserMessages, ProcessMessages
from src.constants.paths import setup_all_directories, show_current_configuration, CSVPaths
from src.core.selenium_manager import SeleniumManager
from src.utils.selenium_helpers import WaitHelper

# Imports del sistema FDA
from src.fda.authentication.fda_login import complete_fda_login
from src.fda.prior_notice.creation.step_01_copy_selection import execute_step_01
from src.fda.prior_notice.creation.step_02_edit_information import execute_step_02
from src.fda.prior_notice.creation.step_03_final_save import execute_step_03

def setup_environment():
    """
    Configura el entorno inicial del sistema
    """
    print("🚀 SISTEMA FDA AUTOMATION")
    print("=" * 50)
    
    # Mostrar configuración actual de rutas
    show_current_configuration()
    
    # Crear directorios necesarios
    setup_all_directories()
    
    # Verificar archivo CSV
    if not CSVPaths.FDA_ORDER_FILE.exists():
        print(f"\n⚠️ ARCHIVO CSV NO ENCONTRADO")
        print(f"📁 Se esperaba: {CSVPaths.FDA_ORDER_FILE}")
        print(f"💡 Puedes ejecutar 'python3 configure_paths.py' para configurar rutas")
        print(f"📋 El archivo debe contener: guia_aerea, order_number, shipping_name")
        
        user_continue = input(f"\n{UserMessages.CONTINUE_WITHOUT_CSV}").strip().lower()
        if user_continue not in ['s', 'si', 'yes', 'y']:
            print("❌ Proceso cancelado por el usuario")
            return False
    
    print("\n✅ Entorno configurado correctamente")
    return True

def execute_prior_notice_creation(driver):
    """
    Ejecuta el proceso completo de creación de Prior Notice
    """
    print(LogMessages.STARTING_PROCESS.format(process="CREACIÓN DE PRIOR NOTICE"))
    print("=" * 60)
    
    try:
        # PASO 1: Copy Selection
        print(f"\n{ProcessMessages.STEP_INDICATOR.format(step=1, description='Copy Selection')}")
        if not execute_step_01(driver, wait=SleepTimes.SHORT_WAIT):
            print(LogMessages.PROCESS_FAILED.format(process="Paso 1 - Copy Selection"))
            return False
        
        # Pausa entre pasos
        print(f"⏸️ Pausa entre pasos...")
        time.sleep(SleepTimes.BETWEEN_STEPS)
        
        # PASO 2: Edit Information
        print(f"\n{ProcessMessages.STEP_INDICATOR.format(step=2, description='Edit Information')}")
        if not execute_step_02(driver, wait=SleepTimes.SHORT_WAIT):
            print(LogMessages.PROCESS_FAILED.format(process="Paso 2 - Edit Information"))
            return False
        
        # Pausa entre pasos
        print(f"⏸️ Pausa entre pasos...")
        time.sleep(SleepTimes.BETWEEN_STEPS)
        
        # PASO 3: Final Save
        print(f"\n{ProcessMessages.STEP_INDICATOR.format(step=3, description='Final Save')}")
        if not execute_step_03(driver, wait=SleepTimes.SHORT_WAIT):
            print(LogMessages.PROCESS_FAILED.format(process="Paso 3 - Final Save"))
            return False
        
        # Proceso completado
        print(f"\n🎉 {LogMessages.PROCESS_COMPLETED.format(process='CREACIÓN DE PRIOR NOTICE')}")
        print(ProcessMessages.SUCCESS_SUMMARY)
        print("📊 Resumen de lo ejecutado:")
        print("   ✅ Paso 1: Copy Selection completado")
        print("   ✅ Paso 2: Edit Information completado")
        print("   ✅ Paso 3: Final Save completado")
        print("\n🔗 El Prior Notice debería estar listo en FDA")
        
        return True
        
    except KeyboardInterrupt:
        print(f"\n⏹️ Proceso interrumpido por el usuario")
        return False
    except Exception as e:
        print(f"\n❌ Error inesperado durante la creación: {e}")
        print("🔍 Revisa los logs para más detalles")
        return False

def main():
    """
    Función principal del sistema FDA Automation
    """
    print("🏗️ SISTEMA FDA AUTOMATION")
    print("Automatización completa: Login + Prior Notice Creation")
    print("=" * 60)
    
    # Setup del entorno
    if not setup_environment():
        print("❌ Error en setup del entorno")
        return
    
    # Confirmación del usuario
    user_confirm = input(f"\n{UserMessages.START_PROCESS}").strip().lower()
    if user_confirm not in ['s', 'si', 'yes', 'y']:
        print("❌ Proceso cancelado por el usuario")
        return
    
    try:
        # Usar SeleniumManager para gestión automática del driver
        with SeleniumManager() as driver:
            print(f"\n🌐 {ProcessMessages.BROWSER_READY}")
            
            # FASE 1: Login a FDA
            print(f"\n{ProcessMessages.STEP_INDICATOR.format(step='LOGIN', description='Autenticación FDA')}")
            print(f"🔗 Navegando a sistema FDA...")
            driver.get("https://www.access.fda.gov")
            
            # Esperar carga inicial
            WaitHelper.wait_for_page_load(driver, ElementTimeouts.PAGE_LOAD)
            
            # Ejecutar login
            login_success = complete_fda_login(driver, WebDriverWait(driver, ElementTimeouts.DEFAULT))
            
            if not login_success:
                print("❌ Error en el proceso de login")
                return
            
            print("✅ Login completado exitosamente")
            
            # FASE 2: Creación de Prior Notice
            print(f"\n{ProcessMessages.STEP_INDICATOR.format(step='PRIOR_NOTICE', description='Automatización Prior Notice')}")
            print(f"💡 A partir de aquí, el proceso es mayormente automático")
            print(f"👤 Solo necesitarás ingresar la fecha cuando se solicite")
            
            # Ejecutar proceso de Prior Notice
            prior_notice_success = execute_prior_notice_creation(driver)
            
            if prior_notice_success:
                print(f"\n🎯 {ProcessMessages.FINAL_SUCCESS}")
                print("📸 Se pueden tomar screenshots finales...")
                print("📁 Archivos generados en:")
                print(f"   • CSV: {CSVPaths.CSV_BASE_DIR}")
                print(f"   • Outputs: {CSVPaths.EXPORTS_DIR}")
                
                # Mantener navegador abierto para verificación
                input(f"\n{UserMessages.KEEP_BROWSER_OPEN}")
            else:
                print(f"\n❌ El proceso de Prior Notice no se completó exitosamente")
                print("🔍 Revisa los mensajes anteriores para identificar problemas")
                
                # Mantener navegador para debug
                input("\n🔍 Navegador mantenido abierto para debug. Presiona Enter para cerrar...")
    
    except KeyboardInterrupt:
        print(f"\n⏹️ Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error crítico en el sistema: {e}")
        print("🆘 Revisa la configuración del sistema")
        print(f"💡 Puedes ejecutar 'python3 configure_paths.py' para reconfigurar")
    
    finally:
        print(f"\n👋 Sistema finalizado")
        print("💡 Tips para próxima ejecución:")
        print("   • Asegúrate de tener order.csv actualizado")
        print("   • Verifica que FDA no haya cambiado su interfaz")
        print("   • Usa 'python3 configure_paths.py' para cambiar carpetas")

if __name__ == "__main__":
    main() 