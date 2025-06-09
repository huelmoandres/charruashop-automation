#!/usr/bin/env python3
"""
Sistema FDA Automation - Versión Refactorizada
Automatiza el proceso completo de login FDA y creación de Prior Notice

> **Desarrollado por:** Andrés Huelmo & Christian Huelmo

Mejoras implementadas:
- Refactoring de funciones largas en componentes pequeños
- Eliminación de código duplicado 
- Optimización de imports centralizados
- Mejores estructuras de datos con enums y dataclasses
- Manejo de errores estructurado
- Type hints mejorados
"""

# Imports optimizados centralizados
from src.utils.import_optimizer import (
    setup_common_environment, ImportStatus, require_selenium
)
from src.constants.enums import (
    OperationType, SystemModule, ProcessStep, ProcessResult
)
from src.core.process_manager import ProcessManager
from src.core.selenium_manager import SeleniumManager
from src.optimizations.screenshot_manager import OptimizedScreenshotManager as ScreenshotManager
from src.optimizations.performance_tracker import OptimizedPerformanceTracker as PerformanceTracker
from src.core.logging_config import init_logging


@require_selenium()
def main():
    """
    Función principal del sistema FDA Automation refactorizado
    Usa ProcessManager para descomponer funciones largas
    """
    # Setup inicial del entorno
    env_status = setup_common_environment()
    
    # Validar dependencias críticas
    if not ImportStatus.validate_required_dependencies(['selenium']):
        print("❌ No se pueden ejecutar procesos web sin Selenium")
        return
    
    # Inicializar sistemas
    logger = init_logging()
    performance_tracker = PerformanceTracker(logger)  
    screenshot_manager = ScreenshotManager(logger)
    
    # Crear ProcessManager con todas las dependencias
    process_manager = ProcessManager(
        logger=logger,
        performance_tracker=performance_tracker,
        screenshot_manager=screenshot_manager
    )
    
    try:
        # Inicializar sesión
        config = process_manager.initialize_session("fda_automation")
        
        print("🏗️ SISTEMA FDA AUTOMATION REFACTORIZADO")
        print("Automatización completa: Login + Prior Notice Creation")
        print(f"🔍 Session ID: {config.session_id}")
        print("=" * 60)
        print("\n💡 Características mejoradas:")
        print("   • Funciones descompuestas en componentes pequeños")
        print("   • Imports optimizados y centralizados")  
        print("   • Estructuras de datos type-safe con enums")
        print("   • Manejo de errores estructurado")
        print("   • Eliminación de código duplicado")
        
        # Confirmar inicio del proceso
        if not process_manager.get_user_confirmation(
            "¿Deseas continuar con el proceso de automatización FDA? (s/n): "
        ):
            print("❌ Proceso cancelado por el usuario")
            return
        
        # Inicializar Selenium con manejo optimizado
        with SeleniumManager() as selenium_manager:
            driver = selenium_manager.start_driver()
            
            print(f"\n🌐 Browser inicializado correctamente")
            
            # FASE 1: Navegación inicial
            nav_result = process_manager.execute_navigation(
                driver, "https://www.access.fda.gov"
            )
            
            if not nav_result.success:
                print(f"❌ Error en navegación: {nav_result.error}")
                return
            
            print("✅ Navegación exitosa a FDA")
            
            # FASE 2: Proceso de Login
            login_result = process_manager.execute_login_process(driver)
            
            if not login_result.success:
                print(f"❌ Error en login: {login_result.error}")
                return
            
            print("✅ Login completado exitosamente")
            
            # FASE 3: Proceso completo de Prior Notice
            prior_notice_result = process_manager.execute_complete_prior_notice_process(driver)
            
            # Mostrar estado final
            process_manager.show_final_status(
                prior_notice_result.success, 
                "Prior Notice Creation"
            )
            
            if prior_notice_result.success:
                # Mantener navegador abierto para verificación
                input("\n🔍 Proceso completado. Navegador mantenido abierto para verificación. Presiona Enter para cerrar...")
            else:
                # Mantener navegador para debug
                input(f"\n🔍 Error en proceso: {prior_notice_result.error}. Navegador mantenido para debug. Presiona Enter para cerrar...")
    
    except KeyboardInterrupt:
        logger.warning("⏹️ Proceso interrumpido por el usuario", module=SystemModule.MAIN.value)
        print(f"\n⏹️ Proceso interrumpido por el usuario")
    except Exception as e:
        logger.critical(f"❌ Error crítico en el sistema: {e}", module=SystemModule.MAIN.value, exception=e)
        print(f"\n❌ Error crítico en el sistema: {e}")
        print("🆘 Revisa la configuración del sistema")
        
    finally:
        # Log final con resumen de la sesión
        process_manager.log_session_summary()
        print(f"\n👋 Sistema finalizado")


class FDAAutomationSystem:
    """
    Clase principal del sistema FDA - Alternativa orientada a objetos
    Demuestra refactoring adicional usando clases
    """
    
    def __init__(self):
        self.env_status = setup_common_environment()
        self.logger = init_logging()
        self.performance_tracker = PerformanceTracker(self.logger)
        self.screenshot_manager = ScreenshotManager(self.logger)
        self.process_manager = ProcessManager(
            logger=self.logger,
            performance_tracker=self.performance_tracker,
            screenshot_manager=self.screenshot_manager
        )
        self.config = None
    
    def validate_system_requirements(self) -> bool:
        """Valida requerimientos del sistema"""
        if not ImportStatus.validate_required_dependencies(['selenium']):
            print("❌ No se pueden ejecutar procesos web sin Selenium")
            return False
        return True
    
    def initialize_session(self) -> bool:
        """Inicializa una nueva sesión"""
        try:
            self.config = self.process_manager.initialize_session("fda_automation")
            return True
        except Exception as e:
            self.logger.error(f"Error inicializando sesión: {e}", module=SystemModule.MAIN.value)
            return False
    
    def show_system_info(self):
        """Muestra información del sistema"""
        print("🏗️ SISTEMA FDA AUTOMATION (Clase-Based)")
        print("Automatización orientada a objetos")
        print(f"🔍 Session ID: {self.config.session_id}")
        print("=" * 60)
    
    def run_automation_process(self) -> ProcessResult:
        """Ejecuta el proceso completo de automatización"""
        try:
            with SeleniumManager() as selenium_manager:
                driver = selenium_manager.start_driver()
                
                # Navegación
                nav_result = self.process_manager.execute_navigation(
                    driver, "https://www.access.fda.gov"
                )
                if not nav_result.success:
                    return nav_result
                
                # Login
                login_result = self.process_manager.execute_login_process(driver)
                if not login_result.success:
                    return login_result
                
                # Prior Notice
                return self.process_manager.execute_complete_prior_notice_process(driver)
                
        except Exception as e:
            error_msg = f"Error en proceso de automatización: {e}"
            self.logger.error(error_msg, module=SystemModule.MAIN.value, exception=e)
            
            return ProcessResult(
                success=False,
                step=ProcessStep.COMPLETED,
                message="Error en automatización",
                error=error_msg
            )
    
    def run(self):
        """Método principal para ejecutar el sistema"""
        if not self.validate_system_requirements():
            return
        
        if not self.initialize_session():
            print("❌ Error inicializando el sistema")
            return
        
        self.show_system_info()
        
        if not self.process_manager.get_user_confirmation(
            "¿Deseas continuar con el proceso de automatización FDA? (s/n): "
        ):
            print("❌ Proceso cancelado por el usuario")
            return
        
        result = self.run_automation_process()
        
        self.process_manager.show_final_status(
            result.success, 
            "Automatización FDA"
        )
        
        # Log final
        self.process_manager.log_session_summary()


if __name__ == "__main__":
    # Opción 1: Función principal refactorizada
    main()
    
    # Opción 2: Sistema orientado a objetos (descomenta para usar)
    # system = FDAAutomationSystem()
    # system.run() 