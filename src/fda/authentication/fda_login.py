from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config.config import FDA_LOGIN_URL, USERNAME, PASSWORD
from src.core.logger import AutomationLogger
import time

# Inicializar logger
logger = AutomationLogger.get_instance()

def navigate_to_login(driver):
    """
    Navega a la página de login de FDA
    """
    logger.fda_logger.info("Iniciando navegación a página de login FDA", extra={"url": FDA_LOGIN_URL})
    driver.get(FDA_LOGIN_URL)
    logger.fda_logger.info("Navegación a página de login FDA completada")

def fill_login_form(driver, wait):
    """
    Completa el formulario de login con usuario, contraseña y checkbox
    """
    logger.fda_logger.info("Iniciando llenado de formulario de login")
    
    try:
        # Completar campo de usuario
        logger.fda_logger.debug("Localizando campo de usuario")
        username_field = wait.until(EC.presence_of_element_located((By.NAME, "userName")))
        username_field.clear()
        username_field.send_keys(USERNAME)
        logger.fda_logger.debug("Campo de usuario completado")
        
        # Completar campo de contraseña
        logger.fda_logger.debug("Localizando campo de contraseña")
        password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_field.clear()
        password_field.send_keys(PASSWORD)
        logger.fda_logger.debug("Campo de contraseña completado")
        
        # Marcar checkbox "understand"
        logger.fda_logger.debug("Localizando checkbox 'understand'")
        understand_checkbox = wait.until(EC.element_to_be_clickable((By.NAME, "understand")))
        if not understand_checkbox.is_selected():
            understand_checkbox.click()
            logger.fda_logger.debug("Checkbox 'understand' marcado")
        
        logger.fda_logger.info("Formulario de login completado exitosamente")
    except Exception as e:
        logger.fda_logger.error("Error llenando formulario de login", extra={"error": str(e)})
        raise

def submit_login_form(driver, wait):
    """
    Envía el formulario de login
    """
    logger.fda_logger.info("Enviando formulario de login")
    
    try:
        login_link = wait.until(EC.element_to_be_clickable((By.ID, "login")))
        login_link.click()
        logger.fda_logger.info("Formulario de login enviado exitosamente")
    except Exception as e:
        logger.fda_logger.error("Error enviando formulario de login", extra={"error": str(e)})
        raise

def handle_two_factor_auth(driver, wait, no_input=False):
    """
    Maneja la autenticación de dos factores
    """
    logger.fda_logger.info("Iniciando proceso de autenticación de dos factores")
    try:
        logger.fda_logger.debug("Esperando página de verificación")
        token_field = wait.until(EC.presence_of_element_located((By.ID, "oneTimePassword")))
        if no_input:
            logger.fda_logger.info("[NO-INPUT] Esperando que el usuario ingrese el token manualmente en el navegador (espera robusta por cambio de URL)")
            print("⏳ Esperando que completes el 2FA en la ventana de Chrome. Si ves un error de código inválido, vuelve a intentarlo. El proceso continuará automáticamente cuando el login sea exitoso.")
            from selenium.common.exceptions import TimeoutException
            from selenium.webdriver.support.ui import WebDriverWait
            import time
            url_token = driver.current_url
            start_time = time.time()
            max_wait = 1800  # 30 minutos
            error_logged = False
            last_log_time = 0
            while True:
                # Verificar si la URL cambió (login exitoso)
                if driver.current_url != url_token:
                    print("✅ Cambio de URL detectado. Verificando login exitoso...")
                    try:
                        dashboard_element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Prior Notice System Interface')]"))
                        )
                        print("✅ Login exitoso detectado. Continuando...")
                        break
                    except TimeoutException:
                        logger.fda_logger.error("No se detectó el dashboard tras el 2FA. Login fallido o token incorrecto.")
                        print("❌ No se detectó el dashboard tras el 2FA. Login fallido o token incorrecto. Deteniendo proceso.")
                        raise Exception("Login fallido tras 2FA")
                # Verificar si aparece el mensaje de error de código inválido
                try:
                    error_box = driver.find_element(By.ID, "serverMsageBox")
                    if "Please enter a valid Verification Code." in error_box.text:
                        if not error_logged:
                            logger.fda_logger.error("❌ Token de verificación inválido detectado. Esperando nuevo intento del usuario.")
                            print("❌ Token de verificación inválido. Esperando que ingreses un nuevo código en Chrome...")
                            error_logged = True
                    else:
                        error_logged = False
                except Exception:
                    error_logged = False
                # Log activo cada 10 segundos
                now = time.time()
                if now - last_log_time > 10:
                    logger.fda_logger.info("⏳ Esperando que completes el 2FA en la ventana de Chrome...")
                    print("⏳ Esperando que completes el 2FA en la ventana de Chrome...")
                    last_log_time = now
                # Timeout
                if now - start_time > max_wait:
                    logger.fda_logger.warning("Timeout esperando que el usuario complete el 2FA (30 minutos)")
                    print("⚠️ Tiempo máximo de espera alcanzado para el 2FA. El proceso continuará, pero puede fallar si no se completó el token.")
                    break
                time.sleep(2)
        else:
            # Solicitar token al usuario
            logger.fda_logger.info("Solicitando token de verificación al usuario")
            verification_token = input("Ingresa el token de verificación: ")
            # Completar campo del token
            token_field.clear()
            token_field.send_keys(verification_token)
            logger.fda_logger.debug("Token de verificación ingresado")
            # Hacer clic en botón de confirmación
            confirm_button = wait.until(EC.element_to_be_clickable((By.ID, "confirmLogin")))
            confirm_button.click()
        logger.fda_logger.info("Autenticación de dos factores completada exitosamente")
    except Exception as e:
        logger.fda_logger.error("Error durante autenticación de dos factores", extra={"error": str(e)})
        raise

def complete_fda_login(driver, wait, no_input=False):
    """
    Ejecuta el proceso completo de login de FDA
    """
    logger.fda_logger.info("=== INICIANDO PROCESO COMPLETO DE LOGIN FDA ===")
    try:
        navigate_to_login(driver)
        fill_login_form(driver, wait)
        submit_login_form(driver, wait)
        handle_two_factor_auth(driver, wait, no_input=no_input)
        logger.fda_logger.info("=== LOGIN FDA COMPLETADO EXITOSAMENTE ===")
        return True
    except Exception as e:
        logger.fda_logger.error("=== ERROR DURANTE LOGIN FDA ===", extra={"error": str(e)})
        logger.error_logger.error("FDA Login failed", extra={
            "source_module": "fda_authentication",
            "function": "complete_fda_login",
            "error": str(e),
            "error_type": type(e).__name__
        })
        return False 