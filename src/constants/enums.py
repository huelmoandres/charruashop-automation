"""
Enums y estructuras de datos centralizadas para el sistema FDA/Shopify
Mejora type safety y elimina magic strings
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, List, Optional

class ProcessStep(Enum):
    """Pasos del proceso FDA"""
    LOGIN = "LOGIN"
    NAVIGATION = "NAVIGATION"
    STEP_01_SELECTION = "STEP_01"
    STEP_02_EDIT_INFO = "STEP_02"
    STEP_03_FINAL_SAVE = "STEP_03"
    COMPLETED = "COMPLETED"

class OperationType(Enum):
    """Tipos de operaciones del sistema"""
    FDA_AUTOMATION = "fda_automation"
    SHOPIFY_EXPORT = "shopify_export"
    ORDER_CONVERSION = "order_conversion"
    MAINTENANCE = "maintenance"
    TESTING = "testing"

class LogLevel(Enum):
    """Niveles de logging"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class ScreenshotType(Enum):
    """Tipos de screenshots"""
    STEP = "step"
    SUCCESS = "success"
    ERROR = "error"
    NAVIGATION = "navigation"
    DEBUG = "debug"

class SystemModule(Enum):
    """Módulos del sistema para logging"""
    MAIN = "main"
    FDA = "fda"
    SHOPIFY = "shopify"
    SELENIUM = "selenium"
    PERFORMANCE = "performance"
    MAINTENANCE = "maintenance"

class UserResponse(Enum):
    """Respuestas válidas del usuario"""
    YES = auto()
    NO = auto()
    
    @classmethod
    def from_string(cls, response: str) -> Optional['UserResponse']:
        """Convierte string de usuario a enum"""
        response = response.strip().lower()
        if response in ['s', 'si', 'yes', 'y', '1', 'true']:
            return cls.YES
        elif response in ['n', 'no', '0', 'false']:
            return cls.NO
        return None

@dataclass
class ProcessResult:
    """Resultado de un proceso"""
    success: bool
    step: ProcessStep
    message: str
    error: Optional[str] = None
    duration: Optional[float] = None
    metadata: Optional[Dict] = None

@dataclass
class ElementLocator:
    """Localizador de elemento optimizado"""
    primary_selector: str
    fallback_selectors: List[str]
    element_type: str
    description: str
    timeout_context: Optional[str] = None
    
    @property
    def all_selectors(self) -> List[str]:
        """Todos los selectores disponibles"""
        return [self.primary_selector] + self.fallback_selectors

@dataclass 
class SystemConfiguration:
    """Configuración centralizada del sistema"""
    session_id: str
    operation_type: OperationType
    debug_mode: bool = False
    max_retries: int = 3
    screenshot_enabled: bool = True
    performance_tracking: bool = True
    
class ConfigurationError(Exception):
    """Error de configuración del sistema"""
    pass

class ProcessError(Exception):
    """Error durante proceso de automatización"""
    def __init__(self, message: str, step: ProcessStep, original_error: Optional[Exception] = None):
        super().__init__(message)
        self.step = step
        self.original_error = original_error 