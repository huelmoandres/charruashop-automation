# ⚡ Optimizaciones de Performance FDA/Shopify Automation

> **Desarrollado por:** Andrés Huelmo & Christian Huelmo

Esta documentación detalla las optimizaciones de performance implementadas en el sistema para mejorar la velocidad y eficiencia de la automatización.

## 📊 Resumen de Mejoras

### **Mejoras de Velocidad:**
- 🚀 **20-40% reducción** en tiempos de espera
- ⚡ **Búsquedas más rápidas** con sistema de caché
- 🔄 **Detección paralela** de elementos
- 📸 **Screenshots asíncronos** sin bloquear el proceso principal

### **Mejoras de Eficiencia:**
- 💾 **Menor uso de disco** con compresión automática
- 🧹 **Auto-limpieza** de archivos antiguos
- 🧠 **Timeouts inteligentes** que aprenden del uso
- 📈 **Análisis en tiempo real** con cache optimizado

## 🔍 Sistema de Caché de Selectores

### **Funcionamiento:**
```python
# ElementCache singleton que almacena selectores exitosos
cache = ElementCache()

# Al encontrar un elemento exitosamente, se cachea el selector
cache.cache_selector("button_submit", "//button[@id='submit-btn']")

# En búsquedas futuras, se prueba el selector cacheado primero
cached_selector = cache.get_selector("button_submit")
```

### **Beneficios:**
- ✅ **Búsquedas instantáneas** para elementos frecuentes
- ✅ **Hit rate tracking** para monitoreo
- ✅ **Auto-invalidación** de cache obsoleto
- ✅ **Thread-safe** con locks

### **Estadísticas de Cache:**
```bash
# Ver estadísticas de cache en logs
make logs-performance
# Output: Cache hit rate: 78.5%, 127 hits, 35 misses
```

## 🔄 Búsqueda Paralela de Elementos

### **Tecnología:**
- **ThreadPoolExecutor** para concurrencia
- **Timeout optimizado** por thread
- **Fallback automático** a búsqueda secuencial

### **Implementación:**
```python
# Búsqueda paralela con múltiples selectores
selectors_dict = {
    "submit_button": "//button[@type='submit']",
    "save_button": "//button[contains(text(), 'Save')]",
    "continue_button": "//button[contains(text(), 'Continue')]"
}

# Se ejecutan todas las búsquedas en paralelo
element_name, element = OptimizedWaitHelper.wait_for_any_element(
    driver, selectors_dict, timeout=3
)
```

### **Ventajas:**
- ⚡ **Detección simultánea** de múltiples elementos
- 🎯 **Primer elemento disponible** gana
- 🔄 **Fallback inteligente** si falla
- 📊 **Tracking de performance** por selector

## ⏱️ Timeouts Adaptativos

### **Sistema de Aprendizaje:**
```python
# El sistema aprende de operaciones pasadas
adaptive_timeouts.record_operation_time("fda_login", 2.3)
adaptive_timeouts.record_operation_time("fda_login", 1.8)
adaptive_timeouts.record_operation_time("fda_login", 2.1)

# Ajusta timeouts automáticamente
smart_timeout = adaptive_timeouts.get_adaptive_timeout(base_timeout=10, "fda_login")
# Resultado: timeout optimizado basado en historial (ej: 8 segundos)
```

### **Categorías de Timeouts:**
| Operación | Timeout Base | Timeout Optimizado | Mejora |
|-----------|-------------|-------------------|---------|
| Búsqueda de botones | 5s | 3s | 40% |
| Carga de páginas | 10s | 8s | 20% |
| Procesos FDA | 15s | 12s | 20% |
| Modales | 10s | 6s | 40% |

### **Contextos Inteligentes:**
```python
# Timeouts específicos por contexto
timeout = SmartTimeout.with_context(
    base_timeout=10, 
    context="fda_table",  # Optimizado para tablas FDA
    performance_history=[1.2, 1.5, 1.8]  # Historial reciente
)
```

## 📸 Screenshots Optimizados

### **OptimizedScreenshotManager:**
- 🖼️ **Compresión automática** con Pillow
- ⚡ **Captura asíncrona** en background
- 🗑️ **Auto-limpieza** de archivos >7 días
- 📊 **Límite configurable** por día

### **Configuración:**
```python
# Screenshot manager optimizado
screenshot_manager = OptimizedScreenshotManager(
    max_screenshots=100,    # Máximo por día
    compress_images=True    # Compresión automática
)

# Captura asíncrona
screenshot_manager.capture_screenshot_async(driver, "step_completed")
```

### **Optimizaciones de Compresión:**
- 📐 **Redimensionamiento** automático a 1920x1080 max
- 🗜️ **Compresión PNG** con nivel 6
- 💾 **Ahorro de espacio** ~60-80%
- 🔄 **Procesamiento background** sin bloquear

## 📊 Performance Tracking Avanzado

### **OptimizedPerformanceTracker:**
```python
# Tracking con cache de estadísticas
with performance_tracker.track("fda_process") as metric:
    # Operación automáticamente trackeada
    execute_fda_process()
    # Estadísticas actualizadas automáticamente
```

### **Características:**
- 📈 **Cache de estadísticas** (TTL: 30s)
- 🔄 **Análisis en tiempo real**
- 📊 **Trends de operaciones**
- 💾 **Reportes JSON** detallados

### **Métricas Disponibles:**
```bash
# Ver métricas de performance
make logs-performance

# Ejemplo de output:
# ✅ fda_login: 2.1s
# ✅ element_search: 0.3s (cache hit)
# ⚡ screenshot_capture: 0.1s (async)
# 📊 Cache hit rate: 82.3%
```

## 🔧 Comandos de Monitoreo

### **Verificar Performance:**
```bash
# Health check con métricas de performance
make health-check

# Ver logs de performance
make logs-performance

# Monitorear en tiempo real
make logs-tail
```

### **Estadísticas Detalladas:**
```bash
# Usar run.py para estadísticas específicas
python run.py health           # Health check completo
python run.py logs:performance # Solo logs de performance
```

## 📈 Resultados Esperados

### **Antes de Optimizaciones:**
- ⏱️ Proceso FDA completo: ~45-60 segundos
- 🔍 Búsqueda de elementos: 5-10 segundos promedio
- 📸 Screenshots: 2-3 segundos cada uno
- 💾 Uso de disco: ~500MB screenshots/día

### **Después de Optimizaciones:**
- ⚡ Proceso FDA completo: ~30-40 segundos (33% mejora)
- 🚀 Búsqueda de elementos: 1-3 segundos promedio (70% mejora)
- 📱 Screenshots: 0.1-0.5 segundos (90% mejora)
- 💾 Uso de disco: ~150MB screenshots/día (70% reducción)

## 🧪 Testing de Performance

### **Benchmarks Automáticos:**
```python
# El sistema automáticamente compara performance
# contra baseline establecido en primera ejecución

# Alertas automáticas si performance degrada >20%
if current_performance < baseline * 0.8:
    logger.warning("Performance degradation detected")
```

### **Métricas Clave:**
- 📊 **Success Rate:** >95% target
- ⚡ **Cache Hit Rate:** >70% target  
- 🎯 **Timeout Efficiency:** <10% timeout occurrences
- 💾 **Storage Efficiency:** <200MB/day screenshots

## 🔧 Configuración Avanzada

### **Personalizar Caché:**
```python
# En src/utils/selenium_helpers.py
cache = ElementCache()
cache.clear_cache()  # Limpiar cache manualmente
stats = cache.get_stats()  # Ver estadísticas
```

### **Ajustar Timeouts:**
```python
# En src/constants/timeouts.py
# Modificar valores base si es necesario
ElementTimeouts.DEFAULT = 8  # Ya optimizado de 10 a 8
SleepTimes.PAGE_LOAD = 1.5   # Ya optimizado de 2 a 1.5
```

### **Screenshots Configuration:**
```python
# Ajustar límites de screenshots
screenshot_manager = OptimizedScreenshotManager(
    max_screenshots=50,     # Reducir si es necesario
    compress_images=False   # Desactivar compresión si se prefiere velocidad
)
```

## 🚀 Próximas Optimizaciones

### **En Desarrollo:**
- 🧠 **Machine Learning** para predicción de timeouts
- 🔄 **Pool de conexiones** para requests HTTP
- 📱 **Mobile-first** screenshot optimization
- 🎯 **Predictive element detection**

### **Roadmap:**
1. **Q1:** Implementar ML timeouts
2. **Q2:** Optimizar requests HTTP
3. **Q3:** Enhanced mobile support
4. **Q4:** Predictive algorithms

---

**📋 Para más información técnica, consulta el código en:**
- `src/utils/selenium_helpers.py` - Sistema de caché y búsqueda paralela
- `src/constants/timeouts.py` - Timeouts adaptativos
- `src/utils/screenshot_utils.py` - Screenshots optimizados
- `src/core/performance.py` - Performance tracking avanzado 