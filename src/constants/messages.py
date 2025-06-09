"""
Mensajes centralizados para el sistema
Facilita internacionalización y mantenimiento
"""

class LogMessages:
    """Mensajes de logging y consola"""
    
    # Inicio y fin
    STARTING_PROCESS = "🚀 INICIANDO {process}"
    PROCESS_COMPLETED = "✅ {process} COMPLETADO"
    PROCESS_FAILED = "❌ ERROR EN {process}"
    
    # Búsqueda de elementos
    SEARCHING_ELEMENT = "🔍 Buscando {element}..."
    ELEMENT_FOUND = "✅ {element} encontrado"
    ELEMENT_NOT_FOUND = "❌ No se pudo encontrar {element}"
    
    # Clics y acciones
    CLICKING_ELEMENT = "🖱️ Haciendo clic en {element}..."
    CLICK_SUCCESS = "✅ {element} clickeado exitosamente"
    CLICK_FAILED = "❌ Error haciendo clic en {element}"
    
    # Navegación
    NAVIGATING_TO = "🔍 Navegando a {destination}..."
    NAVIGATION_SUCCESS = "✅ Navegación exitosa a {destination}"
    NAVIGATION_FAILED = "❌ Error navegando a {destination}"
    
    # Datos y formularios
    READING_DATA = "📋 Leyendo datos desde {source}..."
    DATA_FOUND = "✅ Datos encontrados: {data}"
    UPDATING_FIELD = "📝 Actualizando campo {field}..."
    FIELD_UPDATED = "✅ Campo {field} actualizado con: {value}"

class UserMessages:
    """Mensajes para interacción con usuario"""
    
    # Instrucciones
    ENTER_DATE = "\n📅 Ingresa la fecha (MM/DD/YYYY): "
    DATE_FORMAT_HELP = """
📅 INSTRUCCIONES PARA FECHA DE LLEGADA AL PUERTO:
🎯 Este es un campo de fecha de Angular Material
📝 Formato requerido: MM/DD/YYYY (formato americano)
💡 Ejemplos válidos:
   • 01/15/2024 (15 de enero de 2024)
   • 12/25/2023 (25 de diciembre de 2023)
   • 03/08/2024 (8 de marzo de 2024)
⚠️  IMPORTANTE: Usar SIEMPRE formato MM/DD/YYYY
"""
    
    # Confirmaciones y prompts
    START_PROCESS = "¿Iniciar el proceso de automatización? (s/n): "
    CONTINUE_WITHOUT_CSV = "¿Continuar sin archivo CSV? (s/n): "
    FIELD_CORRECT = "¿El campo se ve correcto en pantalla? (s/n): "
    CONTINUE_PROCESS = "⏸️ Presiona Enter para continuar..."
    KEEP_BROWSER_OPEN = "✅ Proceso completado. Presiona Enter para cerrar el navegador..."
    CLOSE_BROWSER = "⏸️ Presiona Enter para cerrar el navegador..."
    
    # Errores de usuario
    EMPTY_DATE = "⚠️ La fecha no puede estar vacía. Por favor ingresa una fecha."
    INVALID_DATE_FORMAT = "❌ Formato inválido. Debe ser exactamente MM/DD/YYYY"
    INVALID_DATE_VALUES = "⚠️ Fecha inválida. Verifica el mes y día."

class ProcessMessages:
    """Mensajes específicos para procesos del sistema"""
    
    # FDA Login
    FDA_LOGIN_START = "🏛️ INICIANDO LOGIN EN FDA"
    FDA_LOGIN_SUCCESS = "✅ Login FDA exitoso"
    TOKEN_REQUEST = "🔐 Ingresa el token de autenticación 2FA: "
    
    # Prior Notice
    PRIOR_NOTICE_CREATION = "📋 CREACIÓN DE PRIOR NOTICE"
    STEP_EXECUTION = "{step_number}️⃣ EJECUTANDO {step_name}"
    COPY_SELECTION = "PASO 1: SELECCIÓN DE TIPO DE COPIA"
    EDIT_INFORMATION = "PASO 2: EDITAR INFORMACIÓN"
    FINAL_SAVE = "PASO 3: GUARDAR FINAL Y CONFIRMACIÓN"
    
    # Shopify/CSV
    CSV_PROCESSING = "📄 PROCESANDO ARCHIVOS CSV"
    ORDER_CONVERSION = "🔄 CONVIRTIENDO NÚMEROS DE PEDIDO"
    
    # Resúmenes
    CHANGES_SUMMARY = "📋 Resumen de cambios:"
    ACTIONS_PERFORMED = "📋 Acciones realizadas:"
    SUCCESS_SUMMARY = "🎉 Proceso completado exitosamente"
    FINAL_SUCCESS = "🎯 PROCESO GENERAL COMPLETADO CON ÉXITO"
    
    # Indicadores de paso
    STEP_INDICATOR = "📋 PASO {step}: {description}"
    
    # Estados del sistema
    BROWSER_READY = "Navegador iniciado y listo" 