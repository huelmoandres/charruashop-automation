# 🚀 Makefile para FDA Automation - SISTEMA OPTIMIZADO
# Uso: make <comando>
# 
# Desarrollado por: Andrés Huelmo & Christian Huelmo

.PHONY: help install fda fda-full fda-test shopify-export orders-convert orders-update-guia orders-analyze logs-stats logs-clean logs-view logs-compress clean-auto health performance s l ls c h p logs errors last size start dev run go shopify-upload-metafields shopify-export-fda-mapping

# 🏛️ Comandos principales FDA (OPTIMIZADO)
fda:
	@echo "🏛️ Ejecutando proceso FDA completo optimizado..."
	python main.py

fda-full:
	@echo "🏛️ Ejecutando proceso FDA directo optimizado..."
	python main.py

fda-test:
	@echo "🧪 Testing sistema optimizado..."
	python -c "from src.core.optimized_logger import init_optimized_logging; logger = init_optimized_logging(); logger.info('Sistema de prueba', module='test')"

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

# 📊 Comandos de logs y monitoreo (OPTIMIZADO)
logs-stats:
	@echo "📊 Estadísticas de logs optimizados..."
	python src/utils/log_cleaner.py

logs-clean:
	@echo "🧹 Limpieza automática de logs..."
	python -c "from src.utils.log_cleaner import LogCleaner; LogCleaner().compress_old_logs()"

logs-view:
	@echo "👁️ Mostrando logs recientes optimizados..."
	tail -20 logs/fda_automation.log

logs-compress:
	@echo "🗜️ Comprimiendo logs antiguos..."
	python -c "from src.utils.log_cleaner import LogCleaner; LogCleaner().full_cleanup()"

# 🔧 Comandos de mantenimiento (OPTIMIZADO)
clean-auto:
	@echo "🧹 Limpieza automática completa..."
	python -c "from src.utils.log_cleaner import LogCleaner; LogCleaner().full_cleanup()"

health:
	@echo "🔍 Verificando estado del sistema optimizado..."
	python -c "from src.core.optimized_logger import get_optimized_logger; logger = get_optimized_logger(); print('✅ Sistema optimizado funcionando')"

performance:
	@echo "📈 Análisis de performance..."
	python -c "from src.core.performance import get_global_performance_tracker; tracker = get_global_performance_tracker(); print(tracker.get_current_stats())"

# ⚡ SHORTCUTS RÁPIDOS (UX mejorado)
s:
	@python -c "from src.core.optimized_logger import get_optimized_logger; logger = get_optimized_logger(); print('✅ Sistema OK')"

l:
	@tail -5 logs/fda_automation.log

ls:
	@python src/utils/log_cleaner.py

c:
	@python -c "from src.utils.log_cleaner import LogCleaner; LogCleaner().full_cleanup(); print('🧹 Limpieza completada')"

h:
	@python -c "from src.core.optimized_logger import get_optimized_logger; logger = get_optimized_logger(); print('💚 Sistema saludable')"

p:
	@python -c "from src.core.performance import get_global_performance_tracker; print('📊 Performance OK')"

g:
	@echo "🖥️ Iniciando interfaz gráfica..."
	streamlit run streamlit_app.py

logs:
	@tail -10 logs/fda_automation.log

errors:
	@grep -i error logs/fda_automation.log | tail -5 || echo "✅ Sin errores recientes"

last:
	@tail -3 logs/fda_automation.log

size:
	@du -sh logs/

# Aliases adicionales para FDA
start:
	@echo "🏛️ Iniciando FDA automation..."
	python main.py

dev:
	@echo "🏛️ Modo desarrollo FDA..."
	python main.py

run:
	@echo "🏛️ Ejecutando FDA..."
	python main.py

go:
	@echo "🏛️ ¡Vamos! FDA automation..."
	python main.py

# 🖥️ Comandos GUI
gui:
	@echo "🖥️ Iniciando interfaz gráfica Streamlit..."
	streamlit run streamlit_app.py

streamlit:
	@echo "🖥️ Iniciando Streamlit..."
	streamlit run streamlit_app.py

# 📦 Comandos de instalación y setup
install:
	@echo "📦 Instalando dependencias..."
	pip install -r requirements.txt

install-dev:
	@echo "🔧 Instalando dependencias de desarrollo..."
	pip install -e .

setup:
	@echo "🚀 Setup inicial optimizado del proyecto..."
	python -c "from src.core.optimized_logger import init_optimized_logging; logger = init_optimized_logging(); logger.info('Setup completado', module='setup')"
	@echo "✅ Setup optimizado completado"

# 📋 Ayuda
help:
	@echo "🚀 FDA Automation - UX OPTIMIZADO - Comandos disponibles:"
	@echo ""
	@echo "⚡ SHORTCUTS SÚPER RÁPIDOS (NUEVO):"
	@echo "  make s                - Status sistema (1 letra!)"
	@echo "  make l                - Últimas 5 líneas de log"
	@echo "  make ls               - Estadísticas logs"
	@echo "  make c                - Limpieza rápida"
	@echo "  make h                - Health check rápido"
	@echo "  make p                - Performance check"
	@echo "  make logs             - Últimas 10 líneas"
	@echo "  make errors           - Últimos errores"
	@echo "  make last             - Últimas 3 líneas"
	@echo "  make size             - Tamaño de logs"
	@echo ""
	@echo "🏛️ FDA Commands:"
	@echo "  make fda / start / dev / run / go - FDA automation"
	@echo "  make fda-full         - Proceso FDA directo"
	@echo "  make fda-test         - Testing sistema"
	@echo ""
	@echo "🖥️ GUI Interface:"
	@echo "  make g / gui          - Abrir interfaz gráfica Streamlit"
	@echo ""
	@echo "📊 Logs & Monitoring:"
	@echo "  make logs-stats       - Estadísticas completas"
	@echo "  make logs-clean       - Limpieza automática"
	@echo "  make logs-view        - Ver logs recientes"
	@echo "  make logs-compress    - Comprimir logs antiguos"
	@echo ""
	@echo "🔧 Maintenance:"
	@echo "  make clean-auto       - Limpieza completa"
	@echo "  make health           - Health check completo"
	@echo "  make performance      - Análisis performance completo"
	@echo ""
	@echo "💡 TIP: Usa comandos de 1 letra para máxima velocidad!"
	@echo "💡 Ejemplos: 'make s' 'make l' 'make c' ⚡"
	@echo ""

shopify-upload-metafields:
	@echo "🛒 Subiendo códigos FDA y fabricante a Shopify (metafields)..."
	python src/shopify/upload_fda_metafields.py

shopify-export-fda-mapping:
	@echo "🛒 Exportando productos para mapeo FDA..."
	python src/shopify/export_products_for_fda_mapping.py

# Default target
.DEFAULT_GOAL := help 