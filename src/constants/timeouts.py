"""
Timeouts centralizados para todo el sistema
Permite ajustar tiempos de espera de forma consistente
Incluye timeouts adaptativos basados en performance
"""

import time
from typing import Dict, Optional

# Timeouts para Selenium WebDriver
DEFAULT_WAIT = 10
SHORT_WAIT = 5
LONG_WAIT = 15
TABLE_WAIT = 20  # Para cargas de tabla que pueden demorar

# Timeouts para sleep explícitos (usar con moderación)
class SleepTimes:
    """Tiempos de sleep para operaciones específicas (optimizados)"""
    
    # Cargas de página (reducidos)
    PAGE_LOAD = 1.5       # Reducido de 2
    HEAVY_PAGE_LOAD = 3   # Reducido de 5
    
    # Interacciones básicas (optimizadas)
    CLICK_PROCESSING = 0.3  # Reducido de 0.5
    SCROLL = 0.2           # Reducido de 0.3
    INPUT_CLEAR = 0.1      # Reducido de 0.2
    
    # Formularios (optimizados)
    FORM_LOAD = 1          # Reducido de 1.5
    FIELD_UPDATE = 0.5     # Reducido de 0.8
    VALIDATION = 0.8       # Reducido de 1
    
    # Modales y popups (optimizados)
    MODAL_APPEAR = 0.8     # Reducido de 1
    MODAL_PROCESSING = 1.5 # Reducido de 2
    
    # Entre pasos de proceso (optimizados)
    STEP_TRANSITION = 1.5  # Reducido de 2
    BETWEEN_STEPS = 1.5    # Reducido de 2
    
    # Guardar y procesar (optimizados)
    SAVE_PROCESSING = 2    # Reducido de 3
    FINAL_PROCESSING = 3   # Reducido de 5
    
    # Waits cortos
    SHORT_WAIT = 0.8       # Reducido de 1
    
    # Específicos para FDA (optimizados)
    WAIT_TABLE_LOAD = 3    # Reducido de 5 - optimizado con búsqueda paralela
    FDA_TABLE_LOAD = 3     # Reducido de 5 - optimizado con búsqueda paralela
    FDA_COPY_PROCESSING = 2 # Reducido de 3
    FDA_SAVE_PROCESSING = 1.5 # Reducido de 2

# Timeouts para diferentes tipos de elementos
class ElementTimeouts:
    """Timeouts específicos por tipo de elemento (optimizados)"""
    
    # Timeout por defecto (optimizados)
    DEFAULT = 8            # Reducido de 10
    SHORT = 3              # Reducido de 5
    LONG = 12              # Reducido de 15
    
    # Por tipo de elemento (optimizados)
    BUTTON = 3             # Reducido de 5
    INPUT = 5              # Reducido de 10
    SELECT = 5             # Reducido de 10
    TABLE = 15             # Reducido de 20
    MODAL = 6              # Reducido de 10
    NAVIGATION = 8         # Reducido de 10
    PAGE_LOAD = 8          # Reducido de 10
    LOADING = 10           # Reducido de 15

class AdaptiveTimeouts:
    """
    Sistema de timeouts adaptativos que se ajustan según el performance del sistema
    """
    
    def __init__(self):
        self._performance_history: Dict[str, list] = {}
        self._base_multiplier = 1.0
        self._slow_threshold = 2.0  # segundos
        self._fast_threshold = 0.5  # segundos
    
    def record_operation_time(self, operation_name: str, elapsed_time: float):
        """
        Registra el tiempo de una operación para ajustar timeouts futuros
        """
        if operation_name not in self._performance_history:
            self._performance_history[operation_name] = []
        
        # Mantener solo las últimas 10 mediciones
        history = self._performance_history[operation_name]
        history.append(elapsed_time)
        if len(history) > 10:
            history.pop(0)
        
        # Ajustar multiplicador basado en performance promedio
        avg_time = sum(history) / len(history)
        
        if avg_time > self._slow_threshold:
            self._base_multiplier = min(1.5, self._base_multiplier + 0.1)
        elif avg_time < self._fast_threshold:
            self._base_multiplier = max(0.7, self._base_multiplier - 0.05)
    
    def get_adaptive_timeout(self, base_timeout: int, operation_name: str = None) -> int:
        """
        Obtiene un timeout adaptativo basado en el performance histórico
        """
        adaptive_timeout = int(base_timeout * self._base_multiplier)
        
        # Timeouts específicos por operación si hay historial
        if operation_name and operation_name in self._performance_history:
            history = self._performance_history[operation_name]
            if len(history) >= 3:
                avg_time = sum(history[-3:]) / 3  # Promedio de últimas 3
                operation_multiplier = max(0.5, min(2.0, avg_time / self._fast_threshold))
                adaptive_timeout = int(base_timeout * operation_multiplier)
        
        # Límites de seguridad
        return max(2, min(30, adaptive_timeout))
    
    def get_performance_stats(self) -> Dict:
        """Obtiene estadísticas de performance"""
        stats = {
            "base_multiplier": self._base_multiplier,
            "operations_tracked": len(self._performance_history),
            "recent_operations": {}
        }
        
        for operation, times in self._performance_history.items():
            if times:
                stats["recent_operations"][operation] = {
                    "avg_time": f"{sum(times) / len(times):.2f}s",
                    "last_time": f"{times[-1]:.2f}s",
                    "samples": len(times)
                }
        
        return stats

# Instancia global de timeouts adaptativos
adaptive_timeouts = AdaptiveTimeouts()

class SmartTimeout:
    """
    Clase para manejar timeouts inteligentes con contexto
    """
    
    @staticmethod
    def for_element_type(element_type: str, adaptive: bool = True) -> int:
        """
        Obtiene timeout optimizado para un tipo de elemento específico
        """
        base_timeouts = {
            "button": ElementTimeouts.BUTTON,
            "input": ElementTimeouts.INPUT,
            "select": ElementTimeouts.SELECT,
            "table": ElementTimeouts.TABLE,
            "modal": ElementTimeouts.MODAL,
            "navigation": ElementTimeouts.NAVIGATION,
            "loading": ElementTimeouts.LOADING
        }
        
        base_timeout = base_timeouts.get(element_type, ElementTimeouts.DEFAULT)
        
        if adaptive:
            return adaptive_timeouts.get_adaptive_timeout(base_timeout, element_type)
        return base_timeout
    
    @staticmethod
    def with_context(base_timeout: int, context: str, performance_history: Optional[list] = None) -> int:
        """
        Ajusta timeout basado en contexto y historial de performance
        """
        # Ajustes por contexto
        context_multipliers = {
            "fda_table": 0.8,      # Optimizado con búsqueda paralela
            "heavy_page": 1.2,
            "network_dependent": 1.3,
            "user_interaction": 0.7,
            "background_processing": 1.1
        }
        
        multiplier = context_multipliers.get(context, 1.0)
        adjusted_timeout = int(base_timeout * multiplier)
        
        # Ajuste adicional basado en historial si se proporciona
        if performance_history and len(performance_history) >= 2:
            recent_avg = sum(performance_history[-2:]) / 2
            if recent_avg > 2.0:  # Si operaciones recientes son lentas
                adjusted_timeout = int(adjusted_timeout * 1.2)
            elif recent_avg < 0.5:  # Si operaciones recientes son rápidas
                adjusted_timeout = int(adjusted_timeout * 0.8)
        
        return max(2, min(25, adjusted_timeout)) 