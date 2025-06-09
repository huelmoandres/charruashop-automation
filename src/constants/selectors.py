"""
Selectores centralizados para elementos web
Facilita mantenimiento y reutilización de selectores
"""

class FDASelectors:
    """Selectores específicos para el sistema FDA"""
    
    # Login
    USERNAME_INPUT = "userName"
    PASSWORD_INPUT = "password"
    UNDERSTAND_CHECKBOX = "understand"
    LOGIN_BUTTON = "login"
    CONFIRM_LOGIN_BUTTON = "confirmLogin"
    
    # Navegación principal
    PRIOR_NOTICE_LINK = "//a[contains(text(), 'Prior Notice')]"
    FOOD_FACILITY_LINK = "//a[contains(text(), 'Food Facility')]"
    SUBMISSIONS_BUTTON = "//button[@routerlink='/submissions']"
    
    # Tabla de Prior Notices
    PRIOR_NOTICE_TABLE = "//table[@role='presentation']"
    TABLE_ROWS = "//tbody//tr[@class='grid-view ng-star-inserted']"
    COPY_BUTTON = ".//button[@title='Copy']"
    COPY_BUTTON_ICON = ".//i"
    
    # Modal de confirmación
    CONFIRM_MODAL_BUTTON = "//button[contains(text(), 'CONFIRM')]"
    
    # Creación de Prior Notice
    COPY_NO_FOOD_BUTTON = "//button[@class='button button-stepper' and contains(text(), 'COPY WITH NO FOOD ARTICLES')]"
    COPY_NO_FOOD_ALT = "//button[contains(text(), 'COPY WITH NO FOOD') or contains(text(), 'NO FOOD ARTICLES')]"
    
    # Edición de información
    EDIT_BUTTON = "//button[@title='Edit Information']"
    TRACKING_NUMBER_INPUT = "trackingNumber"
    STATE_SELECT = "state"
    PORT_ARRIVAL_DATE_INPUT = "portOfArrivalDate"
    
    # Botones Save & Continue
    SAVE_CONTINUE_BUTTON = "//button[contains(text(), 'Save & Continue')]"
    SAVE_CONTINUE_CLASS = "button button-stepper mdc-button mat-mdc-button mat-unthemed mat-mdc-button-base"

class ModalSelectors:
    """Selectores para elementos de modales y dialogs"""
    
    # Botones principales de modal
    OK_BUTTON = "//button[contains(text(), 'OK')]"
    CONFIRM_BUTTON = "//button[contains(text(), 'Confirm')]"
    ACCEPT_BUTTON = "//button[contains(text(), 'Accept')]"
    CONTINUE_BUTTON = "//button[contains(text(), 'Continue')]"
    
    # Botones en español
    CONFIRMAR_BUTTON = "//button[contains(text(), 'Confirmar')]"
    ACEPTAR_BUTTON = "//button[contains(text(), 'Aceptar')]"
    CONTINUAR_BUTTON = "//button[contains(text(), 'Continuar')]"
    
    # Botones por clase
    PRIMARY_BUTTON = "//button[contains(@class, 'primary')]"
    CONFIRM_CLASS_BUTTON = "//button[contains(@class, 'confirm')]"
    
    # Contenedores de modal
    MODAL_CONTAINER = "//div[@class='modal']//button"
    DIALOG_CONTAINER = "//div[contains(@class, 'dialog')]//button"
    OVERLAY_CONTAINER = "//div[contains(@class, 'overlay')]//button"
    
    # Material Design modals
    MAT_DIALOG_BUTTON = "//mat-dialog-container//button"
    MDC_DIALOG_BUTTON = "//div[contains(@class, 'mdc-dialog')]//button"

class CommonSelectors:
    """Selectores comunes para diferentes elementos"""
    
    # Botones genéricos
    ALL_BUTTONS = "//button"
    ENABLED_BUTTONS = "//button[not(@disabled)]"
    
    # Inputs genéricos
    ALL_INPUTS = "//input"
    TEXT_INPUTS = "//input[@type='text']"
    
    # Elementos de carga
    LOADING_SPINNER = "//div[contains(@class, 'loading')]"
    PROGRESS_BAR = "//div[contains(@class, 'progress')]" 