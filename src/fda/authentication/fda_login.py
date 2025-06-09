from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config.config import FDA_LOGIN_URL, USERNAME, PASSWORD

def navigate_to_login(driver):
    """
    Navega a la página de login de FDA
    """
    driver.get(FDA_LOGIN_URL)
    print("Navegando a página de login de FDA...")

def fill_login_form(driver, wait):
    """
    Completa el formulario de login con usuario, contraseña y checkbox
    """
    # Completar campo de usuario
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "userName")))
    username_field.clear()
    username_field.send_keys(USERNAME)
    
    # Completar campo de contraseña
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_field.clear()
    password_field.send_keys(PASSWORD)
    
    # Marcar checkbox "understand"
    understand_checkbox = wait.until(EC.element_to_be_clickable((By.NAME, "understand")))
    if not understand_checkbox.is_selected():
        understand_checkbox.click()
    
    print("Formulario de login completado")

def submit_login_form(driver, wait):
    """
    Envía el formulario de login
    """
    login_link = wait.until(EC.element_to_be_clickable((By.ID, "login")))
    login_link.click()
    print("Formulario enviado exitosamente")

def handle_two_factor_auth(driver, wait):
    """
    Maneja la autenticación de dos factores
    """
    print("Esperando página de verificación...")
    token_field = wait.until(EC.presence_of_element_located((By.ID, "oneTimePassword")))
    
    # Solicitar token al usuario
    verification_token = input("Ingresa el token de verificación: ")
    
    # Completar campo del token
    token_field.clear()
    token_field.send_keys(verification_token)
    
    # Hacer clic en botón de confirmación
    confirm_button = wait.until(EC.element_to_be_clickable((By.ID, "confirmLogin")))
    confirm_button.click()
    
    print("Token de verificación enviado exitosamente")

def complete_fda_login(driver, wait):
    """
    Ejecuta el proceso completo de login de FDA
    """
    try:
        navigate_to_login(driver)
        fill_login_form(driver, wait)
        submit_login_form(driver, wait)
        handle_two_factor_auth(driver, wait)
        return True
    except Exception as e:
        print(f"Error durante el login: {e}")
        return False 