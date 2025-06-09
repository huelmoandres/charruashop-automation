# 🚀 Guía de Scripts - UX OPTIMIZADO

Sistema híbrido de comandos **súper rápidos** para FDA Automation, con shortcuts de 1 letra para máxima productividad.

## ⚡ **NUEVO: Shortcuts Súper Rápidos**

### **Comandos de 1 Letra (MÁXIMA VELOCIDAD):**
```bash
make s          # Status sistema (1 segundo)
make l          # Últimas líneas log
make c          # Limpieza rápida
make h          # Health check
make p          # Performance
```

### **Dos Formas de Ejecutar:**

#### **Opción 1: Makefile (MÁS RÁPIDA - Recomendada)**
```bash
make <comando>
```

#### **Opción 2: Script Python (Cross-platform)**
```bash
python run.py <comando>
```

---

## 🏛️ **Comandos FDA**

### **🆕 FDA con Múltiples Aliases (NUEVO):**
```bash
# Todas estas formas ejecutan FDA:
make fda        # Original
make start      # Intuitivo
make dev        # Desarrollo  
make run        # Estándar
make go         # Súper rápido

# Equivalente en python:
python run.py fda / start / dev / run / go
```
- Ejecuta `main.py` completo
- Mismo comando, múltiples formas de recordarlo

### **FDA Proceso Directo**
```bash
# Makefile
make fda-full

# run.py  
python run.py fda:full
```
- Proceso FDA sin menú
- Para automatización

### **Testing de Pasos**
```bash
# Makefile
make fda-test

# run.py
python run.py fda:test
```
- Testing pasos individuales
- Debugging

---

## 🛒 **Comandos Shopify/Orders**

### **Exportar Pedidos de Shopify**
```bash
# Makefile
make shopify-export

# run.py
python run.py shopify:export
```
- Conecta con Shopify API
- Genera CSVs de pedidos

### **Convertir Números de Orden**
```bash
# Makefile
make orders-convert

# run.py
python run.py orders:convert
```
- Convierte IDs cortos a largos
- Modo interactivo

### **Actualizar Guías Aéreas**
```bash
# Makefile
make orders-update-guia

# run.py
python run.py orders:guia
```
- Actualiza campo `guia_aerea` en CSVs
- Búsqueda automática por número de pedido

### **Analizar CSVs**
```bash
# Makefile
make orders-analyze

# run.py
python run.py orders:analyze
```
- Lista archivos generados
- Reportes y análisis de contenido

---

## 📊 **🆕 Comandos de Monitoreo SÚPER RÁPIDOS**

### **Status y Monitoring (1 Letra):**
```bash
make s          # Status sistema (1 segundo)
make l          # Últimas 5 líneas (1 segundo)
make ls         # Estadísticas completas (2 segundos)
make h          # Health check (1 segundo)
make p          # Performance check (2 segundos)
```

### **Logs Específicos:**
```bash
make logs       # Últimas 10 líneas
make errors     # Errores recientes
make last       # Últimas 3 líneas
make size       # Tamaño de logs
```

### **Logs Avanzados:**
```bash
# Makefile
make logs-fda

# run.py
python run.py logs:fda
```
- Logs FDA del día actual

### **Seguir Logs en Tiempo Real**
```bash
# Makefile
make logs-tail

# run.py
python run.py logs:tail
```
- Sigue logs en tiempo real
- Ctrl+C para salir

---

## 🔧 **Comandos de Mantenimiento**

### **🆕 Limpieza Súper Rápida:**
```bash
make c          # Limpieza rápida (3 segundos)
```
- Comprime logs antiguos
- Elimina archivos temporales

### **Limpieza Avanzada:**
```bash
# Makefile
make clean-logs

# run.py
python run.py clean:logs
```
- Elimina logs >30 días
- Libera espacio en disco

### **Health Check:**
```bash
make h          # Health check rápido (1 segundo)

# Versión completa:
python run.py health
```
- Verifica estado del sistema
- Verifica estructura de directorios
- Comprueba archivos críticos
- Revisa espacio en disco

### **Limpiar Screenshots Antiguos**
```bash
# Makefile
make clean-screenshots

# run.py
python run.py clean:screenshots
```
- Elimina screenshots más antiguos de 7 días

---

## 📦 **Comandos de Setup**

### **Instalar Dependencias**
```bash
# Makefile
make install

# run.py
python run.py install
```
- Instala desde `requirements.txt`

### **Setup Inicial**
```bash
# Makefile
make setup

# run.py
python run.py setup
```
- Crea directorios necesarios
- Configuración inicial

---

## 🎯 **Aliases y Shortcuts**

### **Aliases en run.py**
```bash
python run.py start    # = python run.py fda
python run.py dev      # = python run.py fda  
python run.py test     # = python run.py fda:test
```

### **Comandos Más Usados**
```bash
# Desarrollo diario
make fda                  # Proceso FDA principal
make logs-tail           # Monitorear en tiempo real
make health-check        # Verificar estado

# Shopify workflow
make shopify-export      # Exportar pedidos
make orders-update-guia  # Actualizar guías
make orders-analyze      # Analizar resultados

# Mantenimiento
make clean-logs          # Limpiar logs antiguos
make backup             # Backup de datos
```

---

## 🔍 **Ejemplos de Uso Típicos**

### **Workflow FDA Completo**
```bash
# 1. Health check
make health-check

# 2. Ejecutar proceso FDA
make fda

# 3. Monitorear logs (en otra terminal)
make logs-tail

# 4. Ver errores si los hay
make logs-errors
```

### **Workflow Shopify**
```bash
# 1. Exportar pedidos
make shopify-export

# 2. Actualizar guías aéreas
make orders-update-guia

# 3. Analizar resultados
make orders-analyze

# 4. Ver logs de Shopify
make logs-list
```

### **Mantenimiento Semanal**
```bash
# 1. Health check
make health-check

# 2. Backup de datos
make backup

# 3. Limpiar logs antiguos
make clean-logs

# 4. Limpiar screenshots
make clean-screenshots
```

---

## 🆚 **Makefile vs run.py - ¿Cuándo usar cuál?**

### **Usar Makefile cuando:**
✅ Estés en macOS/Linux  
✅ Quieras comandos más cortos  
✅ Desarrollo habitual  

### **Usar run.py cuando:**
✅ Necesites compatibilidad Windows  
✅ Quieras output más detallado  
✅ Prefieras sintaxis Python  

---

## 📚 **Referencias Rápidas**

### **Ver todos los comandos:**
```bash
make help           # Makefile
python run.py       # run.py (sin argumentos)
```

### **Estructura de logs:**
```
logs/
├── sessions/2024-01-15/session_main.log
├── fda/2024-01-15/fda_automation.log
├── shopify/2024-01-15/shopify_operations.log
├── selenium/2024-01-15/selenium_debug.log
├── performance/2024-01-15/performance.log
└── errors/2024-01-15/errors.log
```

### **Archivos importantes:**
```
data/orders_export.csv    # Input de números de orden
config/config.py         # Configuración FDA/Shopify
src/orders/output/       # CSVs generados
backups/                 # Backups automáticos
```

---

**¡Sistema de comandos listo para uso productivo!** 🚀

**Comando recomendado para empezar:** `make health-check` 