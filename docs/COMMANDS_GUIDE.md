# 📖 Guía Completa de Comandos y Archivos

Este proyecto tiene dos funcionalidades principales:
1. **🏛️ Automatización FDA** - Sistema principal para crear Prior Notices en FDA
2. **🛒 Procesamiento Shopify** - Scripts auxiliares para exportar pedidos de Shopify

---

## ⚡ **NUEVO: Shortcuts Súper Rápidos (UX Optimizado)**

### **Comandos de 1 Letra para Máxima Productividad:**

| Comando | Función | Tiempo |
|---------|---------|--------|
| `make s` | Status sistema | ~1s |
| `make l` | Últimas 5 líneas log | ~1s |
| `make ls` | Estadísticas logs | ~2s |
| `make c` | Limpieza rápida | ~3s |
| `make h` | Health check | ~1s |
| `make p` | Performance check | ~2s |
| `make logs` | Últimas 10 líneas | ~1s |
| `make errors` | Ver errores recientes | ~2s |
| `make last` | Últimas 3 líneas | ~1s |
| `make size` | Tamaño de logs | ~1s |

### **Múltiples Formas de Ejecutar FDA:**

```bash
# Todas estas formas inician FDA automation:
make fda        # Comando original
make start      # Intuitivo  
make dev        # Desarrollo
make run        # Estándar
make go         # Súper rápido

# Equivalente con python run.py:
python run.py fda / start / dev / run / go
```

### **Comandos Cross-Platform:**

**Makefile (macOS/Linux - MÁS RÁPIDO):**
```bash
make s          # Status instantáneo
make l          # Ver logs
make fda        # Ejecutar FDA
```

**Python run.py (Todas las plataformas):**
```bash
python run.py s      # Status
python run.py l      # Ver logs  
python run.py fda    # Ejecutar FDA
```

---

## 🚀 Comandos Principales

### 1. **Archivo Principal - FDA Automation**

```bash
python main.py
```

**¿Qué hace?**
- Archivo principal del proyecto
- Automatiza el proceso completo de creación de Prior Notices en FDA
- Incluye login, navegación y creación paso a paso
- Sistema de logging production-ready integrado

**Funciones principales:**
- `main_fda_process()` - Proceso completo FDA
- `main_menu()` - Menú interactivo principal
- `test_individual_components()` - Testing de componentes

---

## 🏛️ Sistema FDA - Comandos Específicos

### 2. **Coordinador de Creación de Prior Notices**

```bash
python -c "from src.fda.prior_notice.management.creation_coordinator import coordinate_prior_notice_creation; coordinate_prior_notice_creation()"
```

**¿Qué hace?**
- Ejecuta el proceso completo de creación de Prior Notice
- Login → Navegación → Paso 1 → Paso 2 → Paso 3
- Versión standalone sin menú principal
- Performance tracking automático

### 3. **Testing de Pasos Individuales**

```bash
python -c "from src.fda.prior_notice.management.creation_coordinator import test_individual_steps; test_individual_steps()"
```

**¿Qué hace?**
- Permite probar pasos individuales de creación
- Útil para debugging y desarrollo
- Opciones: Paso 1 (Selección), Paso 2, Paso 3, o secuencia completa

---

## 🛒 Sistema Shopify - Scripts Auxiliares

### 4. **Generador de CSV desde Shopify**

```bash
python src/orders/generate_csv.py
```

**¿Qué hace?**
- Conecta con Shopify API para obtener datos de pedidos
- Lee números de orden desde `data/orders_export.csv`
- Genera CSVs individuales con datos de productos y envío
- Incluye FDA ID de metafields
- Logging automático en `logs/shopify/`

**Campos exportados:**
- order_number, line_item_quantity, line_item_name
- line_item_weight, guia_aerea, shipping_* 
- fda_id

### 5. **Convertidor de Órdenes**

```bash
python src/orders/order_converter.py
```

**¿Qué hace?**
- Convierte números de orden cortos a IDs largos de Shopify
- Exporta múltiples pedidos por número
- Función auxiliar para procesamiento en lote

### 6. **Actualizador de Guías Aéreas**

```bash
python src/orders/update_guia_aerea.py
```

**¿Qué hace?**
- Permite actualizar el campo `guia_aerea` en CSVs existentes
- Input interactivo para números de pedido
- Actualiza archivos CSV generados previamente
- Busca automáticamente en `src/orders/output/`

### 7. **Utilidades CSV**

```bash
python src/orders/csv_utils.py
```

**¿Qué hace?**
- Lista todos los CSVs generados en `src/orders/output/`
- Genera reportes resumen de archivos procesados
- Funciones de utilidad para manejo de CSV
- Análisis de FDA IDs y validación de estructura

---

## 📁 Estructura de Archivos Explicada

### **🔧 Archivos de Configuración**

| Archivo | Propósito |
|---------|-----------|
| `config/config.py` | Credenciales FDA, Shopify tokens, rutas ChromeDriver |
| `src/constants/paths.py` | Rutas fijas simplificadas (data/, logs/, output/) |
| `src/constants/selectors.py` | Selectores CSS/XPath centralizados |
| `src/constants/timeouts.py` | Timeouts para Selenium |
| `src/constants/messages.py` | Mensajes de usuario centralizados |

### **🏛️ Módulos FDA**

| Módulo | Propósito |
|--------|-----------|
| `src/fda/authentication/fda_login.py` | Login y autenticación FDA con logging |
| `src/fda/navigation/` | Navegación dentro del sistema FDA |
| `src/fda/prior_notice/creation/step_01_selection.py` | Selección (renombrado sin "copy") |
| `src/fda/prior_notice/creation/step_02_edit_information.py` | Edición de información |
| `src/fda/prior_notice/creation/step_03_final_save.py` | Guardado final |
| `src/fda/prior_notice/management/creation_coordinator.py` | Coordinador principal con performance tracking |

### **🛒 Módulos Shopify/Orders**

| Módulo | Propósito |
|--------|-----------|
| `src/orders/generate_csv.py` | Generación de CSV desde API con logging |
| `src/orders/order_converter.py` | Conversión de números de orden |
| `src/orders/update_guia_aerea.py` | Actualización de guías |
| `src/orders/csv_utils.py` | Utilidades y reportes |

### **🔧 Módulos Core**

| Módulo | Propósito |
|--------|-----------|
| `src/core/selenium_config.py` | Configuración básica Selenium |
| `src/core/selenium_manager.py` | Manager avanzado Selenium |
| `src/core/logger.py` | Sistema centralizado de logging con SafeFormatter |
| `src/core/performance.py` | Métricas de performance y tracking |
| `src/utils/selenium_helpers.py` | Helpers reutilizables con logging |
| `src/utils/screenshot_utils.py` | Gestión de screenshots automáticos |

---

## 🎯 Flujos de Trabajo Típicos

### **Flujo FDA Completo:**

1. **Verificar configuración** en `config/config.py`:
   - Credenciales FDA correctas
   - Ruta ChromeDriver válida

2. **Ejecutar proceso FDA**:
   ```bash
   python main.py
   ```

3. **Monitorear logs**:
   ```bash
   # Ver logs en tiempo real
   tail -f logs/fda/$(date +%Y-%m-%d)/fda_automation.log
   ```

### **Flujo Shopify → FDA:**

1. **Preparar archivo de órdenes** `data/orders_export.csv`:
   ```csv
   Name
   #1001
   #1002
   #1003
   ```

2. **Generar CSVs desde Shopify**:
   ```bash
   python src/orders/generate_csv.py
   ```

3. **Usar CSV generado para FDA** (proceso manual)

4. **Revisar logs de Shopify**:
   ```bash
   cat logs/shopify/$(date +%Y-%m-%d)/shopify_operations.log
   ```

### **Flujo de Testing/Debug:**

1. **Probar componentes individuales**:
   ```bash
   python main.py # → opción Testing
   ```

2. **Debug pasos específicos**:
   ```bash
   python -c "from src.fda.prior_notice.management.creation_coordinator import test_individual_steps; test_individual_steps()"
   ```

3. **Revisar logs de errores**:
   ```bash
   cat logs/errors/$(date +%Y-%m-%d)/errors.log
   ```

---

## 📋 Archivos de Datos

### **Estructura de Datos Centralizada:**
```
data/
├── orders_export.csv          # Números de orden para procesar
└── samples/
    └── order_sample.csv       # CSV de muestra para FDA
```

### **Entrada requerida:**
- `data/orders_export.csv` - Números de orden para procesar
- `config/config.py` - Credenciales y configuración

### **Salida generada:**
- `src/orders/output/` - CSVs generados por Shopify
- `logs/` - Logs organizados por categorías y fecha
- `logs/screenshots/` - Screenshots automáticos

---

## 📊 Sistema de Logging Integrado

### **Categorías de Logs:**
```bash
# Ver logs específicos por categoría
tail -f logs/sessions/$(date +%Y-%m-%d)/session_main.log      # Sesión principal
tail -f logs/fda/$(date +%Y-%m-%d)/fda_automation.log        # Operaciones FDA
tail -f logs/shopify/$(date +%Y-%m-%d)/shopify_operations.log # Operaciones Shopify
tail -f logs/selenium/$(date +%Y-%m-%d)/selenium_debug.log   # Debug Selenium
tail -f logs/performance/$(date +%Y-%m-%d)/performance.log   # Métricas
tail -f logs/errors/$(date +%Y-%m-%d)/errors.log            # Errores detallados
```

### **Screenshots Automáticos:**
```bash
# Ver screenshots del día
ls -la logs/screenshots/$(date +%Y-%m-%d)/

# Screenshots de errores
ls logs/screenshots/*/error_*.png

# Screenshots de pasos exitosos
ls logs/screenshots/*/step_*.png
```

---

## 🔧 Comandos de Análisis y Monitoreo

### **Análisis de Performance:**
```bash
# Ver métricas de tiempo de ejecución
grep "✅.*:" logs/performance/*/performance.log

# Estadísticas de pasos específicos
grep "step_01_selection" logs/performance/*/performance.log
```

### **Búsqueda de Errores:**
```bash
# Errores recientes
grep "ERROR" logs/errors/$(date +%Y-%m-%d)/errors.log

# Problemas de Selenium
grep "TimeoutException\|NoSuchElementException" logs/selenium/*/selenium_debug.log

# Errores de campos reservados (ya no deberían existir)
grep "Attempt to overwrite" logs/errors/*/errors.log
```

### **Monitoreo de Operaciones FDA:**
```bash
# Progreso de login
grep "Login\|2FA\|Autenticación" logs/fda/*/fda_automation.log

# Progreso de pasos
grep "Step 0[1-3]" logs/fda/*/fda_automation.log

# Éxitos y completaciones
grep "✅.*completado\|exitosamente" logs/fda/*/fda_automation.log
```

---

## ⚡ Comandos Rápidos

```bash
# Proceso FDA completo  
python main.py

# Shopify: generar CSVs
python src/orders/generate_csv.py

# Utilidades CSV
python src/orders/csv_utils.py

# Testing componentes
python -c "from src.fda.prior_notice.management.creation_coordinator import test_individual_steps; test_individual_steps()"

# Ver logs del día en tiempo real
tail -f logs/fda/$(date +%Y-%m-%d)/fda_automation.log

# Análisis rápido de errores
cat logs/errors/$(date +%Y-%m-%d)/errors.log

# Ver screenshots recientes
ls -la logs/screenshots/$(date +%Y-%m-%d)/
```

---

## 🎯 Cambios Importantes Implementados

### **✅ Limpieza de Nomenclatura:**
- Eliminadas funciones con "copy" en el nombre
- `step_01_copy_selection.py` → `step_01_selection.py`
- `select_copy_with_no_food_articles()` → `select_no_food_articles()`

### **✅ Estructura de Datos Simplificada:**
- Datos centralizados en `data/`
- Eliminadas carpetas: `capturas/`, `results/`, `csv_data/`
- Rutas fijas en lugar de sistema configurable

### **✅ Sistema de Logging Production-Ready:**
- Logs categorizados por módulos
- SafeFormatter para campos reservados
- Performance tracking automático
- Screenshots en errores

### **✅ Error Handling Robusto:**
- Manejo de campos reservados (`filename`, `module`)
- Uso de `source_module` y `screenshot_filename`
- Stack traces completos con contexto

---

## 🔍 Troubleshooting Rápido

### **Problema: Archivos no encontrados**
```bash
# Verificar estructura de datos
ls data/orders_export.csv
ls data/samples/order_sample.csv
```

### **Problema: Logs no se generan**
```bash
# Verificar directorios de logs
ls -la logs/
chmod 755 logs/
```

### **Problema: Screenshots fallan**
```bash
# Verificar directorio de screenshots
ls -la logs/screenshots/
```

### **Problema: Error de logging**
```bash
# Verificar que no uses campos reservados
grep -r '"module":\|"filename":' src/
# Debe usar "source_module" y "screenshot_filename"
```

---

**¡Sistema completo, organizado y production-ready!** 🚀

### **Para más detalles:**
- Ver `docs/README.md` - Documentación completa
- Ver `docs/ENHANCED_LOGGING.md` - Sistema de logging detallado 