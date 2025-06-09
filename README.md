# 🚀 Sistema de Automatización FDA y Shopify

> **Desarrollado por:** Andrés Huelmo & Christian Huelmo

Sistema completo de automatización para gestión de **Prior Notices de FDA** y exportación de **pedidos de Shopify**, desarrollado con Selenium y Python.

## ⚡ Inicio Rápido

```bash
# Verificar estado del sistema
make health-check

# Proceso FDA completo
make fda

# Exportar pedidos de Shopify
make shopify-export

# Ver ayuda completa
make help
```

## 🚀 Comandos Principales

### **Makefile (Recomendado en macOS/Linux)**
```bash
make fda                # Proceso FDA completo
make shopify-export     # Exportar de Shopify  
make logs-tail         # Monitorear logs en tiempo real
make health-check      # Health check del sistema
make help              # Ver todos los comandos
```

### **Script Python (Cross-platform)**
```bash
python run.py fda           # Proceso FDA completo
python run.py shopify:export # Exportar de Shopify
python run.py logs:tail     # Monitorear logs en tiempo real  
python run.py health        # Health check del sistema
python run.py               # Ver todos los comandos
```

## 📚 Documentación Completa

La documentación completa está organizada en la carpeta `docs/`:

- **[📋 README Principal](docs/README.md)** - Documentación completa del proyecto
- **[🚀 SCRIPTS_GUIDE](docs/SCRIPTS_GUIDE.md)** - Sistema de scripts Makefile + run.py
- **[📊 ENHANCED_LOGGING](docs/ENHANCED_LOGGING.md)** - Sistema completo de logging
- **[📖 COMMANDS_GUIDE](docs/COMMANDS_GUIDE.md)** - Guía detallada de comandos
- **[⚡ PERFORMANCE_OPTIMIZATIONS](docs/PERFORMANCE_OPTIMIZATIONS.md)** - Optimizaciones de performance avanzadas
- **[🔒 GITIGNORE_UPDATES](docs/GITIGNORE_UPDATES.md)** - Actualizaciones del .gitignore

## 🛠️ Instalación Rápida

```bash
# Instalar dependencias
make install

# Setup inicial
make setup

# Configurar credenciales
cp config/secrets.py.template config/secrets.py
# Editar config/secrets.py con tus credenciales

# Verificar que todo funciona
make health-check
```

## ✨ Características Principales

- 🏛️ **Automatización FDA** - Login, navegación y creación de Prior Notices
- 🛒 **Integración Shopify** - Exportación automática de pedidos
- 📊 **Sistema de Logging** - Logs categorizados y performance tracking
- 🚀 **Comandos Simplificados** - Sistema tipo `npm run`
- 📸 **Screenshots Automáticos** - Captura en errores
- 🔧 **Herramientas de Mantenimiento** - Backup, limpieza, health check
- ⚡ **Optimizaciones de Performance** - Caché de selectores, búsqueda paralela, timeouts adaptativos

## 🎯 Estado del Proyecto

✅ **Sistema production-ready** con logging completo  
✅ **Estructura organizada** sin archivos duplicados  
✅ **Comandos simplificados** estilo npm run  
✅ **Datos centralizados** en carpeta `data/`  
✅ **Documentación completa** en carpeta `docs/`  
✅ **Cross-platform** compatible (Makefile + Python)  
✅ **Performance optimizado** con caché inteligente y timeouts adaptativos  

---

**Para documentación detallada, consulta [docs/README.md](docs/README.md)** 📖 