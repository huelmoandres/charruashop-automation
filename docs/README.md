# 🚀 Sistema de Automatización FDA y Shopify

Sistema completo de automatización para gestión de **Prior Notices de FDA** y exportación de **pedidos de Shopify**, desarrollado con Selenium y Python.

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Funcionalidades](#-funcionalidades)
- [Guías de Uso](#-guías-de-uso)
- [Archivos de Configuración](#-archivos-de-configuración)
- [Documentación Adicional](#-documentación-adicional)
- [Solución de Problemas](#-solución-de-problemas)

## ✨ Características Principales

### 🏛️ **Automatización FDA**
- ✅ Login automático con 2FA
- ✅ Navegación a Prior Notice System
- ✅ Búsqueda y copia de prior notices existentes
- ✅ Creación de nuevos prior notices
- ✅ Manejo de modales de confirmación

### 🛒 **Integración Shopify**
- ✅ Exportación de pedidos a CSV
- ✅ Conversión automática de números de orden
- ✅ Extracción de FDA IDs desde metafields
- ✅ Campos personalizados (guía aérea, peso, etc.)

### 🔧 **Herramientas de Gestión**
- ✅ Actualización masiva de guía aérea
- ✅ Análisis de CSVs generados
- ✅ Deduplicación automática
- ✅ Validación de estructura de datos

## 📂 Estructura del Proyecto

```
selenium-test/
├── 📁 config/
│   └── config.py                    # Configuración general
├── 📁 src/
│   ├── 📁 core/
│   │   ├── selenium_config.py       # Configuración básica Selenium
│   │   └── selenium_manager.py      # Manager avanzado Selenium
│   ├── 📁 fda/                      # 🆕 Módulos FDA organizados
│   │   ├── 📁 authentication/
│   │   │   └── fda_login.py         # Login y autenticación FDA
│   │   ├── 📁 navigation/           # Navegación FDA
│   │   └── 📁 prior_notice/
│   │       ├── 📁 creation/         # Pasos de creación
│   │       └── 📁 management/       # Coordinadores
│   ├── 📁 constants/                # 🆕 Constantes centralizadas
│   │   ├── messages.py              # Mensajes de usuario
│   │   ├── paths.py                 # Rutas configurables
│   │   ├── selectors.py             # Selectores CSS/XPath
│   │   └── timeouts.py              # Timeouts Selenium
│   ├── 📁 utils/
│   │   └── selenium_helpers.py      # Helpers reutilizables
│   └── 📁 orders/
│       ├── generate_csv.py          # Exportación Shopify a CSV
│       ├── order_converter.py       # Conversión de números de orden
│       ├── csv_utils.py             # Utilidades de análisis CSV
│       ├── update_guia_aerea.py     # Actualización de guía aérea
│       └── 📁 output/               # CSVs generados
├── 📁 docs/
│   ├── README.md                    # Esta documentación
│   └── COMMANDS_GUIDE.md            # 🆕 Guía completa de comandos
├── 📁 csv_data/                     # 🆕 Datos CSV (inglés)
├── 📁 results/                      # 🆕 Resultados (inglés)
├── 📁 drivers/
│   └── chromedriver                 # Driver de Chrome
├── main.py                          # Script principal
├── configure_paths.py               # 🆕 Configuración de rutas
└── orders_export.csv               # Archivo de números de orden (usuario)
```

## 🛠️ Instalación

### **Prerequisitos**
```bash
# macOS
brew install python3
brew install chromedriver

# Verificar instalación
python3 --version
chromedriver --version
```

### **Instalación del proyecto**
```bash
# Clonar/descargar el proyecto
cd selenium-test

# Instalar dependencias
pip install selenium requests beautifulsoup4

# Verificar estructura
python main.py --help
```

## ⚙️ Configuración

### **1. Configuración FDA**
Edita `config/config.py`:
```python
# Credenciales FDA
FDA_USERNAME = "tu_usuario_fda"
FDA_PASSWORD = "tu_password_fda"

# URLs FDA
FDA_LOGIN_URL = "https://www.accessdata.fda.gov/scripts/importalert/"
FDA_PRIOR_NOTICE_URL = "URL_del_sistema_prior_notice"
```

### **2. Configuración de Rutas**
```bash
python configure_paths.py
```
- Configura carpetas para CSV (por defecto: `csv_data`)
- Configura carpetas para resultados (por defecto: `results`)
- Personaliza rutas según tus preferencias

### **3. Configuración Shopify**
Edita `src/orders/generate_csv.py`:
```python
# Configuración Shopify
SHOP = "tu_tienda"  # sin .myshopify.com
TOKEN = "tu_access_token"
```

### **4. Archivo de números de orden**
Crea `orders_export.csv`:
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
python main.py
```
- Login con usuario y contraseña
- Manejo automático de 2FA
- Navegación a áreas específicas

#### **Prior Notice System**
```bash
python src/prior_notice_creation/creation_coordinator.py
```
- Acceso a "Prior Notice System Interface"
- Navegación a submissions existentes
- Copia de prior notices con "COPY WITH NO FOOD ARTICLES"

### 🛒 **2. Exportación Shopify**

#### **Exportación Básica**
```bash
python src/orders/generate_csv.py
```
- Lee números de orden desde `orders_export.csv`
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
python src/orders/order_converter.py
```
- Convierte números cortos (#1001) a IDs largos
- Modo interactivo para múltiples conversiones
- Exportación directa por números cortos

### 🔧 **3. Herramientas de Gestión**

#### **Actualización de Guía Aérea**
```bash
python src/orders/update_guia_aerea.py
```
- Busca archivos por número de pedido
- Actualiza columna `guia_aerea` interactivamente
- Modo individual o por lotes
- Salir con `x`

#### **Análisis de CSVs**
```bash
python src/orders/csv_utils.py
```
- Lista archivos generados
- Analiza contenido y FDA IDs
- Genera reportes resumen
- Valida estructura de datos

## 📖 Guías de Uso

### **🚀 Flujo Completo: FDA + Shopify**

#### **Paso 1: Preparar números de orden**
```bash
# Crear orders_export.csv
echo "Name
#1001
#1002
#1003" > orders_export.csv
```

#### **Paso 2: Exportar pedidos de Shopify**
```bash
python src/orders/generate_csv.py
```
**Output esperado:**
```
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

📦 Procesando pedido: 6263141073129
✅ CSV generado: src/orders/output/order_1001_20231215_143022.csv
```

#### **Paso intermedio: Configurar rutas (primera vez)**
```bash
python configure_paths.py
# Configura carpetas según tus preferencias
# Por defecto: csv_data/, results/, screenshots/
```

#### **Paso 3: Actualizar guías aéreas**
```bash
python src/orders/update_guia_aerea.py

# Seleccionar opción 1 (interactivo)
# Ingresar número de pedido: 1001
# Ingresar nuevo valor: ABC123
# Confirmar cambios
```

#### **Paso 4: Procesar en FDA**
```bash
python main.py

# Sistema se conecta automáticamente
# Navega a Prior Notice System
# Usa datos de CSVs para crear submissions
```

### **🔄 Flujos Específicos**

#### **Solo conversión de números**
```bash
python src/orders/order_converter.py
# Modo interactivo para convertir números sin exportar
```

#### **Análisis de archivos existentes**
```bash
python src/orders/csv_utils.py
# Reportes y análisis de CSVs en output/
```

#### **Actualización masiva de guía aérea**
```bash
python src/orders/update_guia_aerea.py
# Seleccionar opción 2 para actualización por lotes
```

## 📋 Archivos de Configuración

### **orders_export.csv** (Requerido)
```csv
Name
#1001
#1002
#1003
```
**Formatos aceptados:**
- Con `#`: `#1001`, `#1002`
- Sin `#`: `1001`, `1002`
- Columnas: `Name`, `order_number`, `numero_orden`, `order`, `pedido`, `number`

### **config/config.py**
```python
# Credenciales FDA
FDA_USERNAME = "usuario"
FDA_PASSWORD = "password"

# Configuración Chrome
CHROME_USER_DATA_DIR = "/Users/usuario/Library/Application Support/Google/Chrome"
CHROMEDRIVER_PATH = "./chromedriver"

# URLs
FDA_LOGIN_URL = "https://www.accessdata.fda.gov/scripts/importalert/"
```

### **Configuración Shopify** (en generate_csv.py)
```python
API_VERSION = "2023-07"
SHOP = "tu_tienda"  # sin .myshopify.com
TOKEN = "shpat_tu_token_aqui"
```

## 📚 Documentación Adicional

### **Guía Completa de Comandos**
Para información detallada sobre todos los comandos disponibles:
```bash
# Ver guía completa de comandos
cat docs/COMMANDS_GUIDE.md
```

**Incluye:**
- 🚀 Todos los comandos principales y auxiliares
- 🏛️ Comandos específicos del sistema FDA
- 🛒 Scripts de Shopify/Orders explicados
- 📁 Estructura de archivos detallada
- 🎯 Flujos de trabajo paso a paso
- ⚡ Referencias rápidas y troubleshooting

### **Configuración de Rutas**
El sistema permite personalizar todas las carpetas:
```bash
python configure_paths.py
```
- Configura ubicación de CSV (`csv_data` por defecto)
- Configura carpeta de resultados (`results` por defecto)
- Personaliza rutas de screenshots y logs

## 🔧 Solución de Problemas

### **Error: ChromeDriver no encontrado**
```bash
# macOS
brew install chromedriver
# O descargar desde https://chromedriver.chromium.org/
```

### **Error: Shopify API 401 Unauthorized**
```python
# Verificar token en src/orders/generate_csv.py
TOKEN = "shpat_token_correcto"
```

### **Error: No se encuentran archivos CSV**
```bash
# Verificar que existe orders_export.csv
ls -la orders_export.csv

# Verificar formato del CSV
cat orders_export.csv
```

### **Error: Selenium TimeoutException**
```python
# Aumentar timeouts en selenium_config.py
IMPLICIT_WAIT = 20  # segundos
EXPLICIT_WAIT = 30  # segundos
```

### **Error: No se encuentra orden en Shopify**
- Verificar que el número de orden existe
- Confirmar que no tiene caracteres especiales
- Revisar que la tienda está correcta

### **Error: FDA 2FA no funciona**
- Verificar credenciales en config.py
- Confirmar que 2FA está configurado
- Revisar que la app 2FA funciona manualmente

## 🎉 Funcionalidades Avanzadas

### **Deduplicación Automática**
- El sistema elimina automáticamente números de orden duplicados
- Muestra estadísticas de duplicados encontrados
- Procesa cada pedido único solo una vez

### **Manejo de Errores Robusto**
- Reintentos automáticos en llamadas API
- Manejo de timeouts de Selenium
- Validación de entrada de usuario tolerante

### **Análisis Detallado**
- Reportes de productos con/sin FDA ID
- Estadísticas de exportación
- Validación de estructura de CSVs

### **Modo Batch**
- Actualización masiva de guías aéreas
- Procesamiento de múltiples pedidos
- Exportación por lotes

---

## 📞 Soporte

Para problemas o preguntas:
1. Revisar logs de error en consola
2. Verificar configuración en archivos config
3. Confirmar que todos los prerequisitos están instalados
4. Validar formato de archivos CSV de entrada

**¡Sistema listo para automatizar tu flujo FDA + Shopify! 🚀**