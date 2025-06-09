# 🚀 Makefile para FDA/Shopify Automation
# Uso: make <comando>

.PHONY: help install fda fda-full fda-test shopify-export orders-convert orders-update-guia orders-analyze logs-fda logs-errors logs-performance logs-tail clean-logs backup health-check

# 🏛️ Comandos principales FDA
fda:
	@echo "🏛️ Ejecutando proceso FDA completo..."
	python main.py

fda-full:
	@echo "🏛️ Ejecutando proceso FDA directo..."
	python -c "from main import main_fda_process; main_fda_process()"

fda-test:
	@echo "🧪 Testing de pasos individuales..."
	python -c "from src.fda.prior_notice.management.creation_coordinator import test_individual_steps; test_individual_steps()"

fda-coordinator:
	@echo "🎯 Ejecutando coordinador FDA..."
	python -c "from src.fda.prior_notice.management.creation_coordinator import coordinate_prior_notice_creation; coordinate_prior_notice_creation()"

# 🛒 Comandos Shopify/Orders
shopify-export:
	@echo "🛒 Exportando pedidos de Shopify..."
	python src/orders/generate_csv.py

orders-convert:
	@echo "🔄 Convertidor de números de orden..."
	python src/orders/order_converter.py

orders-update-guia:
	@echo "✈️ Actualizador de guías aéreas..."
	python src/orders/update_guia_aerea.py

orders-analyze:
	@echo "📊 Analizando CSVs generados..."
	python src/orders/csv_utils.py

# 📊 Comandos de logs y monitoreo
logs-fda:
	@echo "📊 Mostrando logs de FDA del día..."
	python scripts/log_viewer.py fda

logs-errors:
	@echo "🚨 Mostrando logs de errores..."
	python scripts/log_viewer.py errors

logs-performance:
	@echo "⚡ Mostrando logs de performance..."
	python scripts/log_viewer.py performance

logs-tail:
	@echo "👁️ Siguiendo logs en tiempo real (Ctrl+C para salir)..."
	python scripts/log_viewer.py tail

logs-list:
	@echo "📁 Listando logs disponibles..."
	python scripts/log_viewer.py list

# 🔧 Comandos de mantenimiento
clean-logs:
	@echo "🗑️ Limpiando logs antiguos..."
	python scripts/maintenance.py clean-logs

backup:
	@echo "💾 Creando backup de datos..."
	python scripts/maintenance.py backup

health-check:
	@echo "🔍 Verificando estado del sistema..."
	python scripts/maintenance.py health

clean-screenshots:
	@echo "🖼️ Limpiando screenshots antiguos..."
	python scripts/maintenance.py clean-screenshots

# 📦 Comandos de instalación y setup
install:
	@echo "📦 Instalando dependencias..."
	pip install -r requirements.txt

install-dev:
	@echo "🔧 Instalando dependencias de desarrollo..."
	pip install -e .

setup:
	@echo "🚀 Setup inicial del proyecto..."
	python scripts/maintenance.py init
	@echo "✅ Setup completado"

# 📋 Ayuda
help:
	@echo "🚀 FDA/Shopify Automation - Comandos disponibles:"
	@echo ""
	@echo "🏛️ FDA Commands:"
	@echo "  make fda              - Proceso FDA completo (menú interactivo)"
	@echo "  make fda-full         - Proceso FDA directo"
	@echo "  make fda-test         - Testing de pasos individuales"
	@echo "  make fda-coordinator  - Ejecutar coordinador FDA"
	@echo ""
	@echo "🛒 Shopify/Orders Commands:"
	@echo "  make shopify-export       - Exportar pedidos de Shopify"
	@echo "  make orders-convert       - Convertir números de orden"
	@echo "  make orders-update-guia   - Actualizar guías aéreas"
	@echo "  make orders-analyze       - Analizar CSVs generados"
	@echo ""
	@echo "📊 Logs & Monitoring:"
	@echo "  make logs-fda         - Ver logs de FDA del día"
	@echo "  make logs-errors      - Ver logs de errores"
	@echo "  make logs-performance - Ver logs de performance"
	@echo "  make logs-tail        - Seguir logs en tiempo real"
	@echo "  make logs-list        - Listar logs disponibles"
	@echo ""
	@echo "🔧 Maintenance:"
	@echo "  make clean-logs       - Limpiar logs antiguos (>30 días)"
	@echo "  make backup           - Backup de carpeta data/"
	@echo "  make health-check     - Health check del sistema"
	@echo "  make clean-screenshots - Limpiar screenshots antiguos"
	@echo ""
	@echo "📦 Setup:"
	@echo "  make install          - Instalar dependencias"
	@echo "  make install-dev      - Instalar en modo desarrollo"
	@echo "  make setup            - Setup inicial del proyecto"
	@echo ""

# Default target
.DEFAULT_GOAL := help 