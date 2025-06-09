# 🚀 Sistema de Automatización FDA y Shopify

Sistema completo de automatización para gestión de **Prior Notices de FDA** y exportación de **pedidos de Shopify**, desarrollado con Selenium y Python.

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Funcionalidades](#-funcionalidades)
- [Sistema de Logging](#-sistema-de-logging)
- [Guías de Uso](#-guías-de-uso)
- [Documentación Adicional](#-documentación-adicional)
- [Solución de Problemas](#-solución-de-problemas)

## ✨ Características Principales

### 🏛️ **Automatización FDA**
- ✅ Login automático con 2FA
- ✅ Navegación a Prior Notice System
- ✅ Búsqueda y copia de prior notices existentes (sin artículos de comida)
- ✅ Creación de nuevos prior notices en 3 pasos
- ✅ Manejo de modales de confirmación
- ✅ Sistema completo de logging y monitoreo

### 🛒 **Integración Shopify**
- ✅ Exportación de pedidos a CSV
- ✅ Conversión automática de números de orden
- ✅ Extracción de FDA IDs desde metafields
- ✅ Campos personalizados (guía aérea, peso, etc.)
- ✅ Actualización masiva de guías aéreas

### 🔧 **Herramientas de Gestión**
- ✅ Sistema de logging production-ready por categorías
- ✅ Performance tracking con métricas detalladas
- ✅ Screenshots automáticos en errores
- ✅ **Sistema de scripts simplificados** (Makefile + run.py)
- ✅ Comandos tipo `npm run` para todas las operaciones
- ✅ Análisis de CSVs generados
- ✅ Deduplicación automática
- ✅ Validación de estructura de datos

## 📂 Estructura del Proyecto

```
selenium-test/
├── 📁 config/
│   └── config.py                    # Configuración general
├── 📁 data/                         # 🆕 Datos centralizados
│   ├── orders_export.csv           # Archivo principal de números de orden
│   └── 📁 samples/
│       └── order_sample.csv        # CSV de muestra para FDA
├── 📁 src/
│   ├── 📁 core/
│   │   ├── selenium_config.py       # Configuración básica Selenium
│   │   ├── selenium_manager.py      # Manager avanzado Selenium
│   │   ├── logger.py               # 🆕 Sistema centralizado de logging
│   │   └── performance.py          # 🆕 Métricas de performance
│   ├── 📁 fda/                      # 🆕 Módulos FDA organizados
│   │   ├── 📁 authentication/
│   │   │   └── fda_login.py         # Login y autenticación FDA
│   │   ├── 📁 navigation/           # Navegación FDA
│   │   └── 📁 prior_notice/
│   │       ├── 📁 creation/         # Pasos de creación
│   │       │   ├── step_01_selection.py    # 🆕 Selección (renombrado)
│   │       │   ├── step_02_edit_information.py  # Edición de información
│   │       │   └── step_03_final_save.py        # Guardado final
│   │       └── 📁 management/       # Coordinadores
│   │           └── creation_coordinator.py      # Coordinador principal
│   ├── 📁 constants/                # 🆕 Constantes centralizadas
│   │   ├── messages.py              # Mensajes de usuario
│   │   ├── paths.py                 # 🆕 Rutas fijas simplificadas
│   │   ├── selectors.py             # Selectores CSS/XPath
│   │   └── timeouts.py              # Timeouts Selenium
│   ├── 📁 utils/
│   │   ├── selenium_helpers.py      # Helpers reutilizables
│   │   └── screenshot_utils.py      # 🆕 Gestión de screenshots
│   └── 📁 orders/
│       ├── generate_csv.py          # Exportación Shopify a CSV
│       ├── order_converter.py       # Conversión de números de orden
│       ├── csv_utils.py             # Utilidades de análisis CSV
│       ├── update_guia_aerea.py     # Actualización de guía aérea
│       └── 📁 output/               # CSVs generados
├── 📁 logs/                         # 🆕 Logs organizados por categorías
│   ├── 📁 sessions/                 # Logs de sesión principal
│   ├── 📁 fda/                      # Operaciones específicas FDA
│   ├── 📁 shopify/                  # Operaciones Shopify
│   ├── 📁 selenium/                 # Debug de Selenium
│   ├── 📁 performance/              # Métricas de rendimiento
│   ├── 📁 errors/                   # Logs de errores detallados
│   └── 📁 screenshots/              # Screenshots organizados por fecha
├── 📁 docs/
│   ├── README.md                    # Esta documentación
│   ├── ENHANCED_LOGGING.md          # 🆕 Documentación completa de logging
│   └── COMMANDS_GUIDE.md            # 🆕 Guía completa de comandos
├── 📁 drivers/
│   └── chromedriver                 # Driver de Chrome
└── main.py                          # Script principal
```

## 🛠️ Instalación

### **Prerequisitos**
```bash
# macOS
brew install python3
brew install chromedriver

# Opcional: make para comandos simplificados (ya incluido en macOS)
# En Ubuntu/Debian: sudo apt install make
# En Windows: usar python run.py en lugar de make

# Verificar instalación
python3 --version
chromedriver --version
make --version  # Opcional, para comandos simplificados
```

### **Instalación del proyecto**
```bash
# Clonar/descargar el proyecto
cd selenium-test

# Instalar dependencias - Comandos simplificados
make install
# o
python run.py install

# Comando tradicional
pip install -r requirements.txt

# Setup inicial del proyecto
make setup
# o  
python run.py setup

# Verificar estructura y estado
make health-check
# o
python run.py health

# Ver comandos disponibles
make help
# o
python run.py
```

## ⚙️ Configuración

### **1. Configuración de Credenciales**

#### **Crear archivo de secretos**
```bash
# Copiar template y configurar credenciales
cp config/secrets.py.template config/secrets.py
```

#### **Editar `config/secrets.py`:**
```python
# Configuración de Shopify
SHOPIFY_CONFIG = {
    "SHOP": "tu_tienda",  # sin .myshopify.com
    "TOKEN": "shpat_tu_access_token_aqui",  # Access token de Shopify
    "API_VERSION": "2023-07"
}

# Configuración de FDA
FDA_CONFIG = {
    "USERNAME": "tu_usuario_fda",
    "PASSWORD": "tu_password_fda"
}
```

### **2. Configuración Adicional**
Edita `config/config.py` (si es necesario):
```python
# URLs FDA
FDA_LOGIN_URL = "https://www.accessdata.fda.gov/scripts/importalert/"
FDA_PRIOR_NOTICE_URL = "URL_del_sistema_prior_notice"
```

### **3. Archivo de números de orden**
Crea `data/orders_export.csv`:
```csv
Name
#1001
#1002
#1003
```

## 🎯 Funcionalidades

### 🏛️ **1. Automatización FDA**

#### **Login Automático**
```bash
# Comando simplificado
make fda
# o
python run.py fda

# Comando tradicional
python main.py
```
- Login con usuario y contraseña
- Manejo automático de 2FA
- Navegación a áreas específicas

#### **Prior Notice System**
- Acceso a "Prior Notice System Interface"
- Navegación a submissions existentes
- Selección con "NO FOOD ARTICLES" (nomenclatura actualizada)
- Proceso completo en 3 pasos coordinados

### 🛒 **2. Exportación Shopify**

#### **Exportación Básica**
```bash
# Comando simplificado
make shopify-export
# o
python run.py shopify:export

# Comando tradicional
python src/orders/generate_csv.py
```
- Lee números de orden desde `data/orders_export.csv`
- Convierte IDs cortos a largos automáticamente
- Genera CSVs separados por pedido

#### **Campos Exportados (13 campos)**
- `order_number` - Número del pedido
- `line_item_quantity` - Cantidad del producto
- `line_item_name` - Nombre del producto
- `line_item_weight` - Peso en gramos
- `guia_aerea` - Guía aérea (por defecto "01")
- `shipping_name` - Nombre del destinatario
- `shipping_address_1` - Dirección principal
- `shipping_address_2` - Dirección secundaria
- `shipping_city` - Ciudad
- `shipping_zip` - Código postal
- `shipping_province` - Provincia/Estado
- `shipping_country` - País
- `fda_id` - ID de FDA (desde metafields)

#### **Conversión de Números de Orden**
```bash
# Comando simplificado
make orders-convert
# o
python run.py orders:convert

# Comando tradicional
python src/orders/order_converter.py
```
- Convierte números cortos (#1001) a IDs largos
- Modo interactivo para múltiples conversiones
- Exportación directa por números cortos

### 🔧 **3. Herramientas de Gestión**

#### **Actualización de Guía Aérea**
```bash
# Comando simplificado
make orders-update-guia
# o
python run.py orders:guia

# Comando tradicional
python src/orders/update_guia_aerea.py
```
- Busca archivos por número de pedido
- Actualiza columna `guia_aerea` interactivamente
- Modo individual o por lotes
- Salir con `x`

#### **Análisis de CSVs**
```bash
# Comando simplificado
make orders-analyze
# o
python run.py orders:analyze

# Comando tradicional
python src/orders/csv_utils.py
```
- Lista archivos generados
- Analiza contenido y FDA IDs
- Genera reportes resumen
- Valida estructura de datos

## 🚀 Sistema de Scripts Simplificados

### **Comandos estilo npm run**
El proyecto incluye un sistema híbrido de comandos simplificados:

#### **Opción 1: Makefile (Recomendada en macOS/Linux)**
```bash
make fda                # Proceso FDA completo
make shopify-export     # Exportar de Shopify  
make logs-tail         # Monitorear logs en tiempo real
make health-check      # Health check del sistema
make help              # Ver todos los comandos
```

#### **Opción 2: Script Python (Cross-platform)**
```bash
python run.py fda           # Proceso FDA completo
python run.py shopify:export # Exportar de Shopify
python run.py logs:tail     # Monitorear logs en tiempo real  
python run.py health        # Health check del sistema
python run.py               # Ver todos los comandos
```

#### **Categorías de comandos disponibles:**
- 🏛️ **FDA**: `fda`, `fda-test`, `fda-coordinator`
- 🛒 **Shopify/Orders**: `shopify-export`, `orders-convert`, `orders-update-guia`, `orders-analyze`
- 📊 **Logs**: `logs-fda`, `logs-errors`, `logs-performance`, `logs-tail`, `logs-list`
- 🔧 **Mantenimiento**: `clean-logs`, `backup`, `health-check`, `clean-screenshots`

## 📊 Sistema de Logging

### **Características del Sistema**
- 📝 **Logging por módulos** (FDA, Shopify, Selenium, Main)
- 📊 **Performance tracking** con métricas detalladas
- 📸 **Screenshots automáticos** en errores de Selenium
- 🔍 **Session tracking** completo
- 📁 **Rotación automática** de archivos por fecha
- 🎛️ **Configuración flexible** de niveles de log

### **Estructura de Logs**
```
logs/
├── sessions/2024-01-15/session_main.log           # Sesión principal
├── fda/2024-01-15/fda_automation.log             # Operaciones FDA
├── shopify/2024-01-15/shopify_operations.log     # Operaciones Shopify
├── selenium/2024-01-15/selenium_debug.log        # Debug Selenium
├── performance/2024-01-15/performance.log        # Métricas
├── errors/2024-01-15/errors.log                  # Errores detallados
└── screenshots/2024-01-15/                       # Screenshots organizados
```

### **Uso del Sistema de Logging**
```python
from src.core.logger import get_logger

logger = get_logger()

# Logging específico por módulo
logger.info("Proceso iniciado", extra={"source_module": "fda"})
logger.error("Error encontrado", extra={"source_module": "selenium"})
```

## 📖 Guías de Uso

### **🚀 Flujo Completo: FDA + Shopify**

#### **Paso 1: Preparar números de orden**
```bash
# Crear data/orders_export.csv
echo "Name
#1001
#1002
#1003" > data/orders_export.csv
```

#### **Paso 2: Exportar pedidos de Shopify**
```bash
# Comando simplificado
make shopify-export
```
**Output esperado:**
```
🛒 Exportando pedidos de Shopify...
🚀 Iniciando exportación de pedidos (campos simplificados)
📋 Leyendo números de orden desde columna: 'Name'
   📝 '#1001' -> '1001'
   📝 '#1002' -> '1002'
   📝 '#1003' -> '1003'

📊 Resumen de procesamiento:
   ✅ Números válidos procesados: 3
   🎯 Números únicos a convertir: 3

🔄 Convirtiendo 3 números cortos a IDs largos...
✅ Encontrado: #1001 -> ID: 6263141073129
✅ Encontrado: #1002 -> ID: 6263044309225
✅ Encontrado: #1003 -> ID: 6262860808425
```

#### **Paso 3: Procesar con FDA**
```bash
# Comando simplificado
make fda
```
- Selecciona opción "Ejecutar proceso FDA completo"
- El sistema creará automáticamente Prior Notices
- Logs detallados en `logs/fda/[fecha]/`

#### **Paso 4: Actualizar guías aéreas (opcional)**
```bash
# Comando simplificado
make orders-update-guia
```

### **🔍 Análisis y Monitoreo**

#### **Revisar logs específicos**
```bash
# Comandos simplificados
make logs-fda          # Logs de FDA del día
make logs-errors       # Solo errores
make logs-performance  # Métricas de performance
make logs-tail         # Seguir en tiempo real
make logs-list         # Listar logs disponibles

# Comandos tradicionales
tail -f logs/fda/$(date +%Y-%m-%d)/fda_automation.log
cat logs/errors/$(date +%Y-%m-%d)/errors.log
grep "✅.*:" logs/performance/$(date +%Y-%m-%d)/performance.log
```

#### **Screenshots automáticos**
Los screenshots se capturan automáticamente en:
- Errores de Selenium
- Pasos importantes del proceso FDA
- Éxitos de operaciones críticas

Ubicación: `logs/screenshots/[fecha]/`

## 📚 Documentación Adicional

- **[📊 ENHANCED_LOGGING.md](./ENHANCED_LOGGING.md)** - Sistema completo de logging
- **[📖 COMMANDS_GUIDE.md](./COMMANDS_GUIDE.md)** - Guía detallada de comandos
- **[🚀 SCRIPTS_GUIDE.md](./SCRIPTS_GUIDE.md)** - Sistema de scripts Makefile + run.py
- **[🔒 GITIGNORE_UPDATES.md](./GITIGNORE_UPDATES.md)** - Actualizaciones del .gitignore

## 🔧 Solución de Problemas

### **Problemas Comunes**

#### **1. Error en números de orden**
```bash
# Verificar formato del archivo
cat data/orders_export.csv
# Debe tener header "Name" y números con #
```

#### **2. Screenshots no se generan**
```bash
# Verificar directorio de logs
ls -la logs/screenshots/
chmod 755 logs/
```

#### **3. Error de campos reservados en logging**
```bash
# El sistema usa SafeFormatter para evitar errores con campos como 'filename', 'module'
# Si aparece KeyError: "Attempt to overwrite", verificar que uses 'source_module' en lugar de 'module'
```

#### **4. Driver de Chrome no encontrado**
```bash
# macOS
brew install chromedriver
# Verificar ruta en config/config.py
```

#### **5. Archivos no encontrados**
```bash
# Verificar estructura actualizada
ls data/orders_export.csv
ls data/samples/order_sample.csv

# Verificar archivo de configuración
ls config/secrets.py
# Si no existe, copiar desde template:
cp config/secrets.py.template config/secrets.py
```

### **Logs para Debugging**
- **Errores generales**: `logs/errors/[fecha]/errors.log`
- **Problemas de Selenium**: `logs/selenium/[fecha]/selenium_debug.log`
- **Performance issues**: `logs/performance/[fecha]/performance.log`
- **Flujo FDA completo**: `logs/fda/[fecha]/fda_automation.log`

### **Testing del Sistema**
```bash
# Comandos simplificados
make health-check      # Health check completo
make fda-test         # Testing de pasos FDA
make help             # Ver todos los comandos

# Comandos tradicionales
python main.py
# → Seleccionar "Testing de componentes individuales"

python -c "from src.fda.prior_notice.management.creation_coordinator import test_individual_steps; test_individual_steps()"
```

---

## 🎯 **Estado del Proyecto**

✅ **Sistema production-ready** con logging completo  
✅ **Estructura organizada** sin archivos duplicados  
✅ **Nomenclatura consistente** (eliminado "copy" de funciones)  
✅ **Datos centralizados** en carpeta `data/`  
✅ **Logs categorizados** por módulos específicos  
✅ **Screenshots automáticos** en errores  
✅ **Performance tracking** integrado  
✅ **Error handling** robusto con SafeFormatter  

El sistema está **completamente integrado y listo para uso en producción**. 🚀

---

## 🚀 **Comenzar Rápido**

```bash
# Verificar estado del sistema
make health-check

# Proceso FDA completo
make fda

# Ver logs en tiempo real
make logs-tail

# Ver ayuda completa
make help
```

**¡Sistema con comandos simplificados listo para uso productivo!** ⚡