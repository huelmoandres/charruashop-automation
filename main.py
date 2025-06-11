#!/usr/bin/env python3
"""
Sistema FDA Automation - Script Principal Refactorizado
Automatiza el proceso completo de login FDA y creación de Prior Notice

> **Desarrollado por:** Andrés Huelmo & Christian Huelmo

Sistema optimizado con:
- Refactoring completo eliminando funciones largas
- Código duplicado eliminado con templates reutilizables  
- Imports optimizados y centralizados
- Type safety con enums y dataclasses
- Arquitectura modular y mantenible
- ProcessManager para gestión estructurada
"""

# Imports optimizados con logging mejorado
from src.utils.import_optimizer import (
    setup_common_environment, ImportStatus, require_selenium
)
from src.constants.enums import (
    OperationType, SystemModule, ProcessStep, UserResponse
)
from src.core.process_manager import ProcessManager
from src.core.selenium_manager import SeleniumManager
from src.utils.screenshot_utils import OptimizedScreenshotManager as ScreenshotManager
from src.core.performance import OptimizedPerformanceTracker as PerformanceTracker
from src.core.optimized_logger import init_optimized_logging
from src.constants.paths import ORDER_SAMPLE_FILE
from src.constants.messages import UserMessages
import argparse
import inspect
import os


def validate_csv_file(logger) -> bool:
    """
    Valida archivo CSV con logging optimizado
    """
    if not ORDER_SAMPLE_FILE.exists():
        logger.warning(f"Archivo CSV no encontrado", module="main")
        print(f"\n⚠️ ARCHIVO CSV NO ENCONTRADO")
        print(f"📁 Se esperaba: {ORDER_SAMPLE_FILE}")
        print(f"💡 El archivo order_sample.csv debe estar en data/samples/")
        print(f"📋 El archivo debe contener: guia_aerea, order_number, shipping_name")
        
        user_input = input(f"\n{UserMessages.CONTINUE_WITHOUT_CSV}")
        response = UserResponse.from_string(user_input)
        
        if response != UserResponse.YES:
            logger.info("Proceso cancelado por el usuario (sin CSV)", module="main")
            print("❌ Proceso cancelado por el usuario")
            return False
    else:
        logger.info("Archivo CSV encontrado", module="main")
    
    return True


def setup_environment():
    """
    Configura el entorno con logging optimizado anti-spam
    """
    # Setup común optimizado
    env_status = setup_common_environment()
    
    # Verificar dependencias críticas
    if not ImportStatus.validate_required_dependencies(['selenium']):
        print("❌ No se pueden ejecutar procesos web sin Selenium")
        return False
    
    # Inicializar logger optimizado
    logger = init_optimized_logging()
    logger.info("Sistema iniciado", module="main")
    
    print("🚀 FDA AUTOMATION - UX OPTIMIZADO")
    print("=" * 50)
    print("⚡ Sistema rápido y limpio:")
    print("   ✅ Logging inteligente")
    print("   ✅ Performance optimizado") 
    print("   ✅ Comandos súper rápidos")
    print("   ✅ Feedback mejorado")
    
    # Validar archivo CSV con nuevo sistema
    if not validate_csv_file(logger):
        return False
    
    logger.info("Entorno configurado", module="main")
    print("\n✅ Todo listo para usar")
    print("💡 TIP: Usa 'make s' o 'python run.py s' para check rápido")
    return True


@require_selenium()
def main():
    """
    Función principal con logging optimizado sin spam
    Sistema limpio y eficiente
    """
    # Vaciar el log antes de iniciar
    log_path = "logs/fda_automation.log"
    if os.path.exists(log_path):
        with open(log_path, "w") as f:
            f.truncate(0)

    # === NUEVO: Argumentos de línea de comandos ===
    parser = argparse.ArgumentParser(description="FDA Automation CLI")
    parser.add_argument('--headless', action='store_true', help='Ejecutar Chrome en modo headless')
    parser.add_argument('--debug', action='store_true', help='Activar modo debug')
    parser.add_argument('--screenshots', action='store_true', default=True, help='Capturar screenshots (por defecto sí)')
    parser.add_argument('--no-screenshots', action='store_false', dest='screenshots', help='No capturar screenshots')
    parser.add_argument('--no-input', action='store_true', help='No pedir input al usuario (modo automático para GUI)')
    args = parser.parse_args()
    headless = args.headless
    debug = args.debug
    screenshots = args.screenshots
    no_input = args.no_input
    # === FIN ARGUMENTOS ===

    # Setup inicial del entorno con verificación de dependencias
    if not setup_environment():
        print("❌ Error en setup del entorno")
        return
    
    # Inicializar sistemas optimizados
    if 'debug' in inspect.signature(init_optimized_logging).parameters:
        logger = init_optimized_logging(debug=debug)
    else:
        logger = init_optimized_logging()
    performance_tracker = PerformanceTracker(logger)  
    screenshot_manager = ScreenshotManager(logger) if screenshots else None
    
    # Crear ProcessManager con todas las dependencias
    process_manager = ProcessManager(
        logger=logger,
        performance_tracker=performance_tracker,
        screenshot_manager=screenshot_manager
    )
    
    try:
        # Inicializar sesión con configuración estructurada
        config = process_manager.initialize_session("fda_automation")
        print(f"🔍 Sesión: {config.session_id}")
        print("=" * 50)
        
        # Confirmar inicio con validación mejorada
        if no_input:
            user_confirmed = True
        else:
            user_confirmed = process_manager.get_user_confirmation(UserMessages.START_PROCESS)
        if not user_confirmed:
            print("❌ Cancelado")
            return
        
        # Inicializar Selenium con gestión optimizada
        with SeleniumManager(headless=headless) as driver:
            print(f"\n🌐 Browser OK")
            
            # FASE 1: Navegación inicial usando ProcessManager
            print("⚡ Navegando a FDA...")
            nav_result = process_manager.execute_navigation(
                driver, "https://www.access.fda.gov"
            )
            
            if not nav_result.success:
                print(f"❌ Error navegación: {nav_result.error}")
                return
            
            print("✅ FDA conectado")
            
            # FASE 2: Proceso de Login usando ProcessManager
            print("⚡ Iniciando login...")
            login_result = process_manager.execute_login_process(driver)
            
            if not login_result.success:
                print(f"❌ Error login: {login_result.error}")
                return
            
            print("✅ Login OK")
            
            # FASE 3: Proceso completo de Prior Notice
            print("⚡ Procesando Prior Notice...")
            prior_notice_result = process_manager.execute_complete_prior_notice_process(driver)
            
            # Mostrar estado final compacto
            if prior_notice_result.success:
                print("🎉 ¡Prior Notice creado exitosamente!")
                if not no_input:
                    input(f"\n⏸️ Browser abierto para verificar. Presiona Enter para cerrar...")
            else:
                print(f"❌ Error: {prior_notice_result.error}")
                if not no_input:
                    input(f"\n🔍 Browser abierto para debug. Presiona Enter para cerrar...")
    
    except KeyboardInterrupt:
        logger.warning("Proceso interrumpido", module="main")
        print(f"\n⏹️ Interrumpido")
    except Exception as e:
        logger.critical("Error crítico", module="main", exception=e)
        print(f"\n❌ Error: {e}")
        print("🆘 Usa 'make errors' para ver detalles")
        
    finally:
        # Log final compacto
        process_manager.log_session_summary()
        print(f"\n👋 Finalizado")
        print("💡 TIP: 'make l' para ver últimos logs")


if __name__ == "__main__":
    main() 