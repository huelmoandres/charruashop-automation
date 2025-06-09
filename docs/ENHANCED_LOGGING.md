# 📊 Sistema de Logging Avanzado - FDA/Shopify Automation

## 🎯 **Visión General**

Este sistema de logging "Production-Ready" proporciona capacidades avanzadas de monitoreo, debugging y análisis de performance para la automatización FDA/Shopify.

### ✨ **Características Principales**

- 📝 **Logging por módulos** (FDA, Shopify, Selenium, Main)
- 📊 **Performance tracking** con métricas detalladas
- 📸 **Screenshots automáticos** en errores de Selenium
- 🔍 **Session tracking** completo
- 📁 **Rotación automática** de archivos por fecha
- 🎛️ **Configuración flexible** de niveles de log
- 📈 **Análisis de tendencias** y estadísticas
- 🚨 **Error handling** robusto con stack traces
- 🛡️ **SafeFormatter** para campos reservados de Python

---

## 🏗️ **Arquitectura del Sistema**

```
logs/
├── sessions/                     # Logs de sesión principal
│   └── 2024-01-15/
│       └── 2024-01-15_session_main.log
├── fda/                         # Operaciones específicas FDA
│   └── 2024-01-15/
│       └── 2024-01-15_fda_automation.log
├── shopify/                     # Operaciones Shopify
│   └── 2024-01-15/
│       └── 2024-01-15_shopify_operations.log
├── selenium/                    # Debug de Selenium
│   └── 2024-01-15/
│       └── 2024-01-15_selenium_debug.log
├── performance/                 # Métricas de rendimiento
│   └── 2024-01-15/
│       └── 2024-01-15_performance.log
├── errors/                      # Logs de errores detallados
│   └── 2024-01-15/
│       └── 2024-01-15_errors.log
└── screenshots/                 # Screenshots organizados por fecha
    └── 2024-01-15/
        ├── error_login_failed_143022.png
        ├── step_selection_143055.png
        └── success_prior_notice_completed_143127.png

src/
├── core/
│   ├── logger.py                # Sistema central de logging con SafeFormatter
│   ├── performance.py           # Métricas de rendimiento
│   └── selenium_manager.py      # SeleniumManager con logging integrado
└── utils/
    └── screenshot_utils.py      # Gestión de screenshots
```

---

## 🚀 **Guía de Uso Rápido**

### 1. **Ejecutar con Sistema Mejorado**

```bash
# El sistema está integrado en el main.py existente
python3 main.py

# El logging se activa automáticamente
```

### 2. **Inicializar en tu Código**

```python
from src.core.logger import get_logger
from src.core.performance import create_performance_tracker

# Obtener logger
logger = get_logger()

# Usar logging con SafeFormatter (evita conflictos con campos reservados)
logger.info("Proceso iniciado", extra={"source_module": "main"})
logger.error("Error encontrado", extra={"source_module": "fda"}, exc_info=True)

# Performance tracking
performance_tracker = create_performance_tracker(logger)
with performance_tracker.track("operacion_importante"):
    # Tu código aquí
    pass
```

---

## 📝 **Ejemplos de Uso**

### **Logging Básico por Módulos**

```python
logger = get_logger()

# Logs específicos por módulo (IMPORTANTE: usar 'source_module', no 'module')
logger.info("Navegando a FDA", extra={"source_module": "selenium"})
logger.info("Procesando order", extra={"source_module": "fda"})
logger.info("Exportando CSV", extra={"source_module": "shopify"})
logger.error("Error en login", extra={"source_module": "fda"}, exc_info=True)

# Screenshots con nombre seguro (usar 'screenshot_filename', no 'filename')
logger.info("Screenshot capturado", extra={
    "source_module": "selenium",
    "screenshot_filename": "error_login.png"
})
```

### **Performance Tracking**

```python
performance_tracker = create_performance_tracker(logger)

# Tracking manual
performance_tracker.start_metric("fda_login")
# ... tu código ...
performance_tracker.finish_metric("fda_login", success=True)

# Context manager (recomendado)
with performance_tracker.track("prior_notice_creation"):
    execute_prior_notice_steps()

# Obtener estadísticas
stats = performance_tracker.get_step_statistics("fda_login")
print(f"Tiempo promedio: {stats['timing_stats']['avg_time']:.2f}s")
```

### **Screenshots Automáticos**

```python
# El sistema captura automáticamente screenshots en:
# ✅ Errores de Selenium
# ✅ Pasos importantes del proceso
# ✅ Éxitos de operaciones críticas

# Manual (opcional)
screenshot_manager.capture_step_screenshot(driver, "custom_step", 1)
screenshot_manager.capture_error_screenshot(driver, "custom_error", exception)
```

---

## 📊 **Análisis de Logs**

### **Archivos Generados**

| Ubicación | Propósito | Contenido |
|-----------|-----------|-----------|
| `logs/sessions/[fecha]/session_main.log` | Flujo principal | Inicio/fin de sesión, decisiones importantes |
| `logs/fda/[fecha]/fda_automation.log` | Procesos FDA | Login, Prior Notice, navegación |
| `logs/shopify/[fecha]/shopify_operations.log` | Operaciones Shopify | CSV export, API calls |
| `logs/selenium/[fecha]/selenium_debug.log` | Debug Selenium | Interacciones con browser, elementos |
| `logs/performance/[fecha]/performance.log` | Métricas | Tiempos de ejecución, estadísticas |
| `logs/errors/[fecha]/errors.log` | Errores detallados | Stack traces, contexto de errores |

### **Formato de Logs**

```
[2024-01-15 14:30:22] [    INFO] [automation.fda] [Session: fda_automation_20240115_143022] ✅ Login a FDA completado exitosamente
[2024-01-15 14:30:25] [   ERROR] [automation.selenium] [Session: fda_automation_20240115_143022] ❌ Error navegando a URL: TimeoutException
[2024-01-15 14:30:25] [    INFO] [automation.performance] [Session: fda_automation_20240115_143022] ✅ fda_login: 15.34s
```

---

## 🎛️ **Configuración Avanzada**

### **Niveles de Log**

```python
# DEBUG: Información muy detallada (solo archivos)
logger.debug("Elemento encontrado: #submit-button", extra={"source_module": "selenium"})

# INFO: Información general (archivos + consola)
logger.info("Proceso iniciado correctamente", extra={"source_module": "main"})

# WARNING: Advertencias importantes
logger.warning("Elemento no encontrado, reintentando...", extra={"source_module": "selenium"})

# ERROR: Errores manejables
logger.error("Fallo en operación, continuando...", extra={"source_module": "fda"}, exc_info=True)

# CRITICAL: Errores críticos del sistema
logger.critical("Error crítico, deteniendo proceso", extra={"source_module": "main"}, exc_info=True)
```

### **SafeFormatter - Campos Seguros**

```python
# ✅ CORRECTO: Usar campos seguros
logger.info("Procesando archivo", extra={
    "source_module": "fda",           # No 'module' (reservado)
    "screenshot_filename": "step1.png",  # No 'filename' (reservado)
    "step_number": 1,
    "action": "selection"
})

# ❌ INCORRECTO: Campos reservados (causan KeyError)
logger.info("Procesando archivo", extra={
    "module": "fda",        # ❌ Reservado por Python logging
    "filename": "step1.png"  # ❌ Reservado por Python logging
})
```

---

## 🔍 **Debugging y Troubleshooting**

### **Problemas Comunes Resueltos**

1. **Error de campos reservados (SOLUCIONADO)**
   ```bash
   # Antes: KeyError: "Attempt to overwrite 'filename' in LogRecord"
   # Ahora: SafeFormatter maneja automáticamente campos faltantes
   ```

2. **Logs no se generan**
   ```bash
   # Verificar que existe el directorio
   ls -la logs/
   
   # Verificar permisos
   chmod 755 logs/
   ```

3. **Screenshots fallan**
   ```python
   # Verificar que el driver está activo
   if selenium_manager.screenshot_manager:
       selenium_manager.screenshot_manager.capture_screenshot(...)
   ```

### **Sistema AutomationLogger**

```python
# El sistema tiene propiedades específicas para cada tipo de log
from src.core.logger import AutomationLogger

logger = AutomationLogger.get_instance()

# Loggers específicos por categoría
logger.main_logger.info("Sesión iniciada")
logger.fda_logger.info("Navegando a FDA")
logger.shopify_logger.info("Exportando pedidos")
logger.selenium_logger.debug("Elemento encontrado")
logger.error_logger.error("Error crítico", exc_info=True)
logger.performance_logger.info("Métrica registrada")
```

---

## 🔧 **Integración en Módulos Existentes**

### **Módulos FDA**
```python
# src/fda/authentication/fda_login.py
logger.info("Iniciando login a FDA", extra={"source_module": "fda"})
logger.info("Introduciendo credenciales", extra={"source_module": "fda"})
logger.info("Esperando código 2FA", extra={"source_module": "fda"})
```

### **Módulos Orders/Shopify**
```python
# src/orders/generate_csv.py
logger.info("Conectando con Shopify API", extra={"source_module": "shopify"})
logger.info("Procesando pedido", extra={"source_module": "shopify", "order_id": order_id})
```

### **Módulos Utils/Selenium**
```python
# src/utils/selenium_helpers.py
logger.debug("Buscando elemento", extra={"source_module": "selenium", "selector": selector})
logger.warning("Elemento no encontrado, reintentando", extra={"source_module": "selenium"})
```

---

## 📈 **Performance Tracking Integrado**

### **Creation Coordinator con Métricas**
```python
# El coordinator tiene performance tracking integrado
performance_tracker = PerformanceTracker(logger)

with performance_tracker.track("complete_prior_notice_process"):
    with performance_tracker.track("step_01_selection"):
        complete_step_01_selection()
    
    with performance_tracker.track("step_02_edit_information"):
        complete_step_02_edit_information()
    
    with performance_tracker.track("step_03_final_save"):
        complete_step_03_final_save()

# Métricas automáticas en logs/performance/
```

---

## 📞 **Soporte y Comandos de Análisis**

### **Análisis por Categorías**
```bash
# Solo logs de operaciones FDA
tail -f logs/fda/2024-01-15/2024-01-15_fda_automation.log

# Solo errores del día
cat logs/errors/2024-01-15/2024-01-15_errors.log

# Solo performance del último mes
ls logs/performance/2024-01-*/
```

### **Búsquedas Específicas**
```bash
# Analizar solo problemas de Selenium
grep "ERROR" logs/selenium/*/selenium_debug.log

# Ver métricas de performance
grep "✅.*:" logs/performance/*/performance.log

# Buscar errores de campos reservados (ya no deberían existir)
grep "Attempt to overwrite" logs/errors/*/errors.log
```

### **Screenshots por Fecha**
```bash
# Ver screenshots del día
ls -la logs/screenshots/$(date +%Y-%m-%d)/

# Screenshots de errores específicos
ls logs/screenshots/*/error_*.png
```

---

## 🗂️ **Beneficios de la Estructura Organizada**

### **Separación Lógica por Módulos**
- **FDA logs**: Solo operaciones de automatización FDA
- **Shopify logs**: Solo exportaciones y API calls
- **Selenium logs**: Solo debug de interacciones web
- **Performance logs**: Solo métricas y estadísticas
- **Error logs**: Solo errores con stack traces completos

### **Rotación Automática por Fecha**
- Logs organizados por fecha automáticamente
- Fácil limpieza de logs antiguos
- Archivado natural para auditoría

### **SafeFormatter Integrado**
- Manejo automático de campos reservados de Python
- No más errores `KeyError: "Attempt to overwrite 'filename'"`
- Compatibilidad completa con el sistema de logging estándar

---

## 🎯 **Estado Actual del Sistema**

✅ **Integración Completa**: Todos los módulos principales tienen logging  
✅ **SafeFormatter**: Manejo robusto de campos reservados  
✅ **Performance Tracking**: Métricas automáticas en todos los procesos  
✅ **Screenshots Automáticos**: Captura en errores y pasos importantes  
✅ **Logs Categorizados**: Separación lógica por tipo de operación  
✅ **Session Tracking**: Identificación única de sesiones  
✅ **Error Handling**: Stack traces completos y contexto detallado  

---

**¡El sistema está completamente integrado, probado y listo para producción!** 🎯 

### **Comando de Prueba Rápida**
```bash
python main.py
# → Seleccionar "Testing de componentes individuales"
# → Verificar logs en logs/[categoria]/[fecha]/
``` 