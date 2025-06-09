# 🔒 Actualizaciones de .gitignore

## ✅ **Cambios Realizados**

### **📊 Datos y CSVs**
```bash
# AGREGADO - Nueva estructura de datos
data/                           # Ignora carpeta data/ completa
!data/samples/                  # EXCEPCIÓN: mantiene samples/
!data/samples/order_sample.csv  # EXCEPCIÓN: mantiene archivo de muestra

# ACTUALIZADO - CSV de entrada movido
data/orders_export.csv          # Antes: orders_export.csv (raíz)
```

### **📝 Sistema de Logs**
```bash
# AGREGADO - Logs específicos por categoría
logs/sessions/     # Logs de sesión principal
logs/fda/         # Operaciones FDA
logs/shopify/     # Operaciones Shopify
logs/selenium/    # Debug Selenium
logs/performance/ # Métricas de rendimiento
logs/errors/      # Errores detallados
logs/screenshots/ # Screenshots automáticos
```

### **🚀 Sistema de Scripts**
```bash
# AGREGADO - Archivos generados por scripts
backups/          # Backups automáticos
backup_*/         # Backups timestamped
backup_data_*/    # Backups específicos de data/

# AGREGADO - Archivos temporales de scripts
*.tmp
*.temp
script_output_*
maintenance_*
command_output_*
script_log_*

# AGREGADO - Cache de comandos
.command_cache/
.make_cache/
```

## 🎯 **Archivos MANTENIDOS en Git**

### **✅ Scripts del Sistema**
- `Makefile` - Comandos principales
- `run.py` - Runner Python cross-platform
- `scripts/` - Utilidades de logging y mantenimiento
- `SCRIPTS_GUIDE.md` - Documentación de scripts
- `requirements.txt` - Dependencias del proyecto

### **✅ Configuración**
- `config/secrets.py.template` - Template para credenciales
- `config/config.py.template` - Template de configuración

### **✅ Datos de Muestra**
- `data/samples/order_sample.csv` - Archivo de muestra para FDA

## 🚫 **Archivos IGNORADOS**

### **🔒 Datos Sensibles**
- `data/orders_export.csv` - Contiene números de pedidos reales
- `config/secrets.py` - Credenciales FDA y Shopify
- `src/orders/output/` - CSVs generados con datos de clientes

### **📝 Logs y Temporales**
- `logs/` - Todos los logs del sistema
- `backups/` - Backups automáticos
- Archivos `*.log`, `*.tmp`, `*.temp`

### **🛠️ Archivos Generados**
- Cache de comandos
- Outputs de scripts
- Archivos de mantenimiento

## 🔍 **Verificación**

### **Comandos para verificar .gitignore:**
```bash
# Ver archivos siendo trackeados
git status --porcelain

# Verificar si un archivo está siendo ignorado
git check-ignore archivo.txt

# Ver todos los archivos ignorados
git status --ignored

# Verificar archivos importantes NO están ignorados
git check-ignore Makefile run.py scripts/ || echo "✅ OK"
```

## 📋 **Estructura Final de Archivos**

### **🟢 Trackeados por Git:**
```
selenium-test/
├── Makefile                    # Sistema de comandos
├── run.py                      # Runner Python
├── requirements.txt            # Dependencias
├── SCRIPTS_GUIDE.md           # Documentación scripts
├── scripts/                    # Utilidades
├── src/                        # Código fuente
├── docs/                       # Documentación
├── config/
│   ├── config.py.template      # Template configuración
│   └── secrets.py.template     # Template credenciales
└── data/samples/
    └── order_sample.csv        # Muestra para FDA
```

### **🔴 Ignorados por Git:**
```
selenium-test/
├── data/orders_export.csv      # Datos de pedidos
├── config/secrets.py           # Credenciales reales
├── logs/                       # Todos los logs
├── backups/                    # Backups automáticos
├── src/orders/output/          # CSVs generados
└── env/                        # Virtual environment
```

## 🎯 **Beneficios**

✅ **Seguridad**: Credenciales y datos sensibles protegidos  
✅ **Limpieza**: Repository sin archivos temporales o generados  
✅ **Funcionalidad**: Scripts y templates disponibles para todos  
✅ **Flexibilidad**: Samples incluidos para setup rápido  
✅ **Mantenimiento**: Logs y backups ignorados automáticamente  

**¡.gitignore optimizado para el sistema de scripts y estructura final!** 🚀 