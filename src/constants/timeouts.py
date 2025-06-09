"""
Timeouts centralizados para todo el sistema
Permite ajustar tiempos de espera de forma consistente
"""

# Timeouts para Selenium WebDriver
DEFAULT_WAIT = 10
SHORT_WAIT = 5
LONG_WAIT = 15
TABLE_WAIT = 20  # Para cargas de tabla que pueden demorar

# Timeouts para sleep explícitos (usar con moderación)
class SleepTimes:
    """Tiempos de sleep para operaciones específicas"""
    
    # Cargas de página
    PAGE_LOAD = 2
    HEAVY_PAGE_LOAD = 5  # Para tablas y contenido pesado
    
    # Interacciones básicas
    CLICK_PROCESSING = 0.5
    SCROLL = 0.3
    INPUT_CLEAR = 0.2
    
    # Formularios
    FORM_LOAD = 1.5
    FIELD_UPDATE = 0.8
    VALIDATION = 1
    
    # Modales y popups
    MODAL_APPEAR = 1
    MODAL_PROCESSING = 2
    
    # Entre pasos de proceso
    STEP_TRANSITION = 2
    BETWEEN_STEPS = 2
    
    # Guardar y procesar
    SAVE_PROCESSING = 3
    FINAL_PROCESSING = 5
    
    # Waits cortos
    SHORT_WAIT = 1
    
    # Específicos para FDA
    WAIT_TABLE_LOAD = 5  # CRÍTICO - La tabla FDA demora
    FDA_TABLE_LOAD = 5  # CRÍTICO - La tabla FDA demora (mantenemos ambos para compatibilidad)
    FDA_COPY_PROCESSING = 3
    FDA_SAVE_PROCESSING = 2

# Timeouts para diferentes tipos de elementos
class ElementTimeouts:
    """Timeouts específicos por tipo de elemento"""
    
    # Timeout por defecto
    DEFAULT = DEFAULT_WAIT
    SHORT = SHORT_WAIT
    LONG = LONG_WAIT
    
    # Por tipo de elemento
    BUTTON = SHORT_WAIT
    INPUT = DEFAULT_WAIT
    SELECT = DEFAULT_WAIT
    TABLE = TABLE_WAIT
    MODAL = DEFAULT_WAIT
    NAVIGATION = DEFAULT_WAIT
    PAGE_LOAD = DEFAULT_WAIT
    LOADING = LONG_WAIT  # Para indicadores de carga 