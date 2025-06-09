"""
Sistema de Logging Avanzado para FDA/Shopify Automation
Características:
- Logs por módulo (FDA, Shopify, Selenium)
- Screenshots automáticos en errores
- Tracking de performance
- Session tracking
- Rotación automática de archivos
- Configuración por ambiente (DEBUG/PRODUCTION)
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import json
import traceback
from functools import wraps
import time

class SafeFormatter(logging.Formatter):
    """Formatter personalizado que maneja campos faltantes graciosamente"""
    
    def format(self, record):
        # Asegurar que session_id esté presente
        if not hasattr(record, 'session_id'):
            record.session_id = 'no_session'
        
        # Asegurar que otros campos comunes estén presentes
        if not hasattr(record, 'user_id'):
            record.user_id = 'system'
            
        return super().format(record)

class AutomationLogger:
    """
    Logger central para el sistema de automatización
    """
    
    def __init__(self, session_id: Optional[str] = None):
        """
        Inicializa el sistema de logging
        
        Args:
            session_id: ID único para esta sesión de automatización
        """
        self.session_id = session_id or self._generate_session_id()
        self.start_time = datetime.now()
        self.logs_dir = Path("logs")
        self.screenshots_dir = self.logs_dir / "screenshots"
        
        # Crear directorios si no existen
        self._ensure_directories()
        
        # Configurar loggers por módulo
        self.loggers = {}
        self._setup_loggers()
        
        # Tracking de sesión
        self.session_events = []
        self.performance_metrics = {}
        
        # Log inicial de sesión
        self._log_session_start()
    
    # Propiedades para acceso directo a loggers específicos
    @property
    def main_logger(self):
        """Logger principal de sesión"""
        return self.loggers['main']
    
    @property
    def fda_logger(self):
        """Logger específico para operaciones FDA"""
        return self.loggers['fda']
    
    @property
    def shopify_logger(self):
        """Logger específico para operaciones Shopify"""
        return self.loggers['shopify']
    
    @property
    def selenium_logger(self):
        """Logger específico para debug de Selenium"""
        return self.loggers['selenium']
    
    @property
    def error_logger(self):
        """Logger específico para errores"""
        return self.loggers['errors']
    
    @property
    def performance_logger(self):
        """Logger específico para métricas de performance"""
        return self.loggers['performance']
    
    def start_session(self, session_id: str):
        """Inicia una nueva sesión con ID específico"""
        self.session_id = session_id
        self._log_session_start()
    
    def _generate_session_id(self) -> str:
        """Genera un ID único para la sesión"""
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def _ensure_directories(self):
        """Crea los directorios necesarios para logs organizados por categorías"""
        self.logs_dir.mkdir(exist_ok=True)
        self.screenshots_dir.mkdir(exist_ok=True)
        
        # Crear estructura de directorios por categoría
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Directorios principales por módulo/tipo
        subdirs = [
            'sessions',      # Logs de sesión principal
            'fda',          # Operaciones específicas FDA  
            'shopify',      # Operaciones Shopify
            'selenium',     # Debug de Selenium
            'performance',  # Métricas de rendimiento
            'errors'        # Logs de errores detallados
        ]
        
        for subdir in subdirs:
            (self.logs_dir / subdir / today).mkdir(parents=True, exist_ok=True)
        
        # Screenshots por fecha
        (self.screenshots_dir / today).mkdir(parents=True, exist_ok=True)
    
    def _setup_loggers(self):
        """Configura loggers específicos por módulo en subcarpetas organizadas"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Configuración de loggers por módulo con rutas organizadas
        modules = {
            'main': ('sessions', 'session_main.log'),
            'fda': ('fda', 'fda_automation.log'),
            'shopify': ('shopify', 'shopify_operations.log'),
            'selenium': ('selenium', 'selenium_debug.log'),
            'errors': ('errors', 'errors.log'),
            'performance': ('performance', 'performance.log')
        }
        
        for module, (subdir, filename) in modules.items():
            logger = logging.getLogger(f'automation.{module}')
            logger.setLevel(logging.DEBUG)
            
            # Handler para archivo específico del módulo en su subcarpeta
            file_handler = logging.FileHandler(
                self.logs_dir / subdir / today / f"{today}_{filename}",
                encoding='utf-8'
            )
            
            # Formatter detallado usando SafeFormatter
            formatter = SafeFormatter(
                '[%(asctime)s] [%(levelname)8s] [%(name)s] [Session: %(session_id)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            
            # Handler para consola (solo INFO y superior)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter(
                '%(levelname)s: %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
            
            self.loggers[module] = logger
    
    def _log_session_start(self):
        """Log del inicio de sesión con información del entorno"""
        self.info("Sistema de logging iniciado", module='main')
        self.info(f"Session ID: {self.session_id}", module='main')
        self.info(f"Timestamp: {self.start_time}", module='main')
        self.info(f"Logs directory: {self.logs_dir.absolute()}", module='main')
        
        # Log de configuración del entorno y estructura de directorios
        env_info = {
            "python_version": f"{os.sys.version}",
            "working_directory": str(Path.cwd()),
            "session_id": self.session_id,
            "logs_structure": {
                "sessions": str(self.logs_dir / "sessions"),
                "fda": str(self.logs_dir / "fda"),
                "shopify": str(self.logs_dir / "shopify"),
                "selenium": str(self.logs_dir / "selenium"),
                "performance": str(self.logs_dir / "performance"),
                "errors": str(self.logs_dir / "errors"),
                "screenshots": str(self.screenshots_dir)
            }
        }
        self.debug(f"Environment info: {json.dumps(env_info, indent=2)}", module='main')
    
    def _get_logger(self, module: str) -> logging.Logger:
        """Obtiene el logger para un módulo específico"""
        if module not in self.loggers:
            module = 'main'  # Fallback al logger principal
        return self.loggers[module]
    
    def _add_session_context(self, record):
        """Agrega contexto de sesión a los logs"""
        record.session_id = self.session_id
        return record
    
    # Métodos públicos de logging por nivel
    def debug(self, message: str, module: str = 'main', **kwargs):
        """Log nivel DEBUG"""
        logger = self._get_logger(module)
        extra = {'session_id': self.session_id}
        extra.update(kwargs)
        logger.debug(message, extra=extra)
    
    def info(self, message: str, module: str = 'main', **kwargs):
        """Log nivel INFO"""
        logger = self._get_logger(module)
        extra = {'session_id': self.session_id}
        extra.update(kwargs)
        logger.info(message, extra=extra)
        
        # Agregar a tracking de sesión
        self.session_events.append({
            'timestamp': datetime.now().isoformat(),
            'level': 'INFO',
            'module': module,
            'message': message
        })
    
    def warning(self, message: str, module: str = 'main', **kwargs):
        """Log nivel WARNING"""
        logger = self._get_logger(module)
        extra = {'session_id': self.session_id}
        extra.update(kwargs)
        logger.warning(message, extra=extra)
    
    def error(self, message: str, module: str = 'main', exception: Optional[Exception] = None, **kwargs):
        """Log nivel ERROR con detalles de excepción"""
        logger = self._get_logger(module)
        extra = {'session_id': self.session_id}
        extra.update(kwargs)
        
        # Log básico del error
        logger.error(message, extra=extra)
        
        # Log detallado en el logger de errores
        error_logger = self._get_logger('errors')
        error_details = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'module': module,
            'message': message,
            'traceback': traceback.format_exc() if exception else None
        }
        
        error_logger.error(f"ERROR DETAILS: {json.dumps(error_details, indent=2)}", extra=extra)
        
        # Agregar a tracking de sesión
        self.session_events.append({
            'timestamp': datetime.now().isoformat(),
            'level': 'ERROR',
            'module': module,
            'message': message,
            'exception': str(exception) if exception else None
        })
    
    def critical(self, message: str, module: str = 'main', exception: Optional[Exception] = None, **kwargs):
        """Log nivel CRITICAL"""
        logger = self._get_logger(module)
        extra = {'session_id': self.session_id}
        extra.update(kwargs)
        logger.critical(message, extra=extra)
        
        # También logear en errors
        self.error(f"CRITICAL: {message}", module=module, exception=exception, **kwargs)

# Decorador para logging automático de funciones
def log_function_call(module: str = 'main', level: str = 'INFO'):
    """
    Decorador para loguear automáticamente llamadas a funciones
    
    Args:
        module: Módulo donde logear
        level: Nivel de log
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Obtener instancia del logger (asume que está disponible globalmente)
            logger = getattr(wrapper, '_automation_logger', None)
            
            if logger:
                func_name = f"{func.__module__}.{func.__name__}" if hasattr(func, '__module__') else func.__name__
                
                # Log de inicio
                if level.upper() == 'DEBUG':
                    logger.debug(f"🔧 Iniciando función: {func_name}", module=module)
                else:
                    logger.info(f"🔧 Ejecutando: {func_name}", module=module)
                
                start_time = time.time()
                
                try:
                    result = func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    
                    # Log de éxito
                    logger.info(f"✅ Completado: {func_name} ({execution_time:.2f}s)", module=module)
                    return result
                    
                except Exception as e:
                    execution_time = time.time() - start_time
                    
                    # Log de error
                    logger.error(f"❌ Error en {func_name} ({execution_time:.2f}s): {e}", 
                               module=module, exception=e)
                    raise
            else:
                # Si no hay logger, ejecutar normalmente
                return func(*args, **kwargs)
        
        return wrapper
    return decorator

# Instancia global del logger (se inicializa cuando se necesite)
_global_logger: Optional[AutomationLogger] = None

def get_logger() -> AutomationLogger:
    """Obtiene la instancia global del logger"""
    global _global_logger
    if _global_logger is None:
        _global_logger = AutomationLogger()
    return _global_logger

# Método estático para compatibilidad 
AutomationLogger.get_instance = staticmethod(get_logger)

def init_logging(session_id: Optional[str] = None) -> AutomationLogger:
    """
    Inicializa el sistema de logging para una nueva sesión
    
    Args:
        session_id: ID opcional para la sesión
        
    Returns:
        Instancia del logger configurado
    """
    global _global_logger
    _global_logger = AutomationLogger(session_id)
    
    # Configurar el decorador para usar este logger
    log_function_call._automation_logger = _global_logger
    
    return _global_logger 