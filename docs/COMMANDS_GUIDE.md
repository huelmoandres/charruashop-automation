# 📖 Guía Completa de Comandos y Archivos

Este proyecto tiene dos funcionalidades principales:
1. **🏛️ Automatización FDA** - Sistema principal para crear Prior Notices en FDA
2. **🛒 Procesamiento Shopify** - Scripts auxiliares para exportar pedidos de Shopify

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
- Utiliza la nueva arquitectura organizada

**Funciones principales:**
- `main_fda_process()` - Proceso completo FDA
- `main_menu()` - Menú interactivo principal
- `test_individual_components()` - Testing de componentes

---

### 2. **Configuración de Rutas**

```bash
python configure_paths.py
```

**¿Qué hace?**
- Script interactivo para configurar carpetas del proyecto
- Permite personalizar dónde se guardan CSV, resultados, screenshots
- Actualiza automáticamente las rutas en `src/constants/paths.py`

**Configuraciones:**
- Carpeta CSV (por defecto: `csv_data`)
- Carpeta de resultados (por defecto: `results`) 
- Carpeta de screenshots (por defecto: `screenshots`)

---

## 🏛️ Sistema FDA - Comandos Específicos

### 3. **Coordinador de Creación de Prior Notices**

```bash
python -c "from src.fda.prior_notice.management.creation_coordinator import coordinate_prior_notice_creation; coordinate_prior_notice_creation()"
```

**¿Qué hace?**
- Ejecuta el proceso completo de creación de Prior Notice
- Login → Navegación → Paso 1 → Paso 2 → Paso 3
- Versión standalone sin menú principal

### 4. **Testing de Pasos Individuales**

```bash
python -c "from src.fda.prior_notice.management.creation_coordinator import test_individual_steps; test_individual_steps()"
```

**¿Qué hace?**
- Permite probar pasos individuales de creación
- Útil para debugging y desarrollo
- Opciones: Paso 1, Paso 2, Paso 3, o secuencia completa

---

## 🛒 Sistema Shopify - Scripts Auxiliares

### 5. **Generador de CSV desde Shopify**

```bash
python src/orders/generate_csv.py
```

**¿Qué hace?**
- Conecta con Shopify API para obtener datos de pedidos
- Lee números de orden desde `orders_export.csv`
- Genera CSVs individuales con datos de productos y envío
- Incluye FDA ID de metafields

**Campos exportados:**
- order_number, line_item_quantity, line_item_name
- line_item_weight, guia_aerea, shipping_* 
- fda_id

### 6. **Convertidor de Órdenes**

```bash
python src/orders/order_converter.py
```

**¿Qué hace?**
- Convierte números de orden cortos a IDs largos de Shopify
- Exporta múltiples pedidos por número
- Función auxiliar para procesamiento en lote

### 7. **Actualizador de Guías Aéreas**

```bash
python src/orders/update_guia_aerea.py
```

**¿Qué hace?**
- Permite actualizar el campo `guia_aerea` en CSVs existentes
- Input interactivo para números de pedido
- Actualiza archivos CSV generados previamente

### 8. **Utilidades CSV**

```bash
python src/orders/csv_utils.py
```

**¿Qué hace?**
- Lista todos los CSVs generados en `src/orders/output/`
- Genera reportes resumen de archivos procesados
- Funciones de utilidad para manejo de CSV

---

## 📁 Estructura de Archivos Explicada

### **🔧 Archivos de Configuración**

| Archivo | Propósito |
|---------|-----------|
| `config/config.py` | Credenciales FDA, Shopify tokens, rutas ChromeDriver |
| `src/constants/paths.py` | Rutas de carpetas configurables |
| `src/constants/selectors.py` | Selectores CSS/XPath centralizados |
| `src/constants/timeouts.py` | Timeouts para Selenium |
| `src/constants/messages.py` | Mensajes de usuario centralizados |

### **🏛️ Módulos FDA**

| Módulo | Propósito |
|--------|-----------|
| `src/fda/authentication/` | Login y autenticación FDA |
| `src/fda/navigation/` | Navegación dentro del sistema FDA |
| `src/fda/prior_notice/creation/` | Pasos individuales de creación |
| `src/fda/prior_notice/management/` | Coordinadores y gestores |

### **🛒 Módulos Shopify/Orders**

| Módulo | Propósito |
|--------|-----------|
| `src/orders/generate_csv.py` | Generación de CSV desde API |
| `src/orders/order_converter.py` | Conversión de números de orden |
| `src/orders/update_guia_aerea.py` | Actualización de guías |
| `src/orders/csv_utils.py` | Utilidades y reportes |

### **🔧 Módulos Core**

| Módulo | Propósito |
|--------|-----------|
| `src/core/selenium_config.py` | Configuración básica Selenium |
| `src/core/selenium_manager.py` | Manager avanzado Selenium |
| `src/utils/selenium_helpers.py` | Helpers reutilizables |

---

## 🎯 Flujos de Trabajo Típicos

### **Flujo FDA Completo:**

1. **Configurar rutas** (primera vez):
   ```bash
   python configure_paths.py
   ```

2. **Verificar configuración** en `config/config.py`:
   - Credenciales FDA correctas
   - Ruta ChromeDriver válida

3. **Ejecutar proceso FDA**:
   ```bash
   python main.py
   ```

### **Flujo Shopify → FDA:**

1. **Preparar archivo de órdenes** `orders_export.csv`:
   ```csv
   order_number
   1001
   1002
   1003
   ```

2. **Generar CSVs desde Shopify**:
   ```bash
   python src/orders/generate_csv.py
   ```

3. **Usar CSV generado para FDA** (manual)

### **Flujo de Testing/Debug:**

1. **Probar componentes individuales**:
   ```bash
   python main.py # → opción Testing
   ```

2. **Debug pasos específicos**:
   ```bash
   python -c "from src.fda.prior_notice.management.creation_coordinator import test_individual_steps; test_individual_steps()"
   ```

---

## 📋 Archivos de Datos

### **Entrada requerida:**
- `orders_export.csv` - Números de orden para procesar
- `config/config.py` - Credenciales y configuración

### **Salida generada:**
- `csv_data/` - CSVs organizados por tipo
- `results/` - Screenshots, logs, reportes
- `src/orders/output/` - CSVs generados por Shopify

---

## ⚡ Comandos Rápidos

```bash
# Setup inicial
python configure_paths.py

# FDA proceso completo  
python main.py

# Shopify: generar CSVs
python src/orders/generate_csv.py

# Utilidades CSV
python src/orders/csv_utils.py

# Testing componentes
python -c "from src.fda.prior_notice.management.creation_coordinator import test_individual_steps; test_individual_steps()"
```

---

## 🔍 Troubleshooting

### **Error de rutas:**
```bash
python configure_paths.py  # Reconfigurar carpetas
```

### **Error de ChromeDriver:**
- Verificar `config/config.py` → `CHROMEDRIVER_PATH`
- Descargar ChromeDriver compatible

### **Error de credenciales FDA:**
- Verificar `config/config.py` → `USERNAME`, `PASSWORD`

### **Error Shopify API:**
- Verificar token en `src/orders/generate_csv.py`

---

**💡 Tip:** Usa `python main.py` para acceso a todas las funciones principales con menú interactivo. 