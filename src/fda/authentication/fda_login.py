from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config.config import FDA_LOGIN_URL, USERNAME, PASSWORD
from src.core.logger import AutomationLogger

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

def handle_two_factor_auth(driver, wait):
    """
    Maneja la autenticación de dos factores
    """
    logger.fda_logger.info("Iniciando proceso de autenticación de dos factores")
    
    try:
        logger.fda_logger.debug("Esperando página de verificación")
        token_field = wait.until(EC.presence_of_element_located((By.ID, "oneTimePassword")))
        
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

def complete_fda_login(driver, wait):
    """
    Ejecuta el proceso completo de login de FDA
    """
    logger.fda_logger.info("=== INICIANDO PROCESO COMPLETO DE LOGIN FDA ===")
    
    try:
        navigate_to_login(driver)
        fill_login_form(driver, wait)
        submit_login_form(driver, wait)
        handle_two_factor_auth(driver, wait)
        
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