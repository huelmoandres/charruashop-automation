"""
Import Optimizer - Centraliza y optimiza importaciones comunes
Evita duplicación de imports y mejora la organización del código
"""

# Standard Library Imports
import os
import sys
import time
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from contextlib import contextmanager
from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor, as_completed

# Third-party imports
try:
    import selenium
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.common.exceptions import (
        TimeoutException, NoSuchElementException, WebDriverException,
        ElementNotInteractableException, StaleElementReferenceException
    )
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

# Local imports - Constants
from ..constants.paths import (
    BASE_DIR, DATA_DIR, LOGS_DIR, SCREENSHOTS_DIR, 
    ORDER_SAMPLE_FILE, ensure_directories
)
from ..constants.timings import SleepTimes, ElementTimeouts
from ..constants.messages import ProcessMessages, LogMessages, UserMessages
from ..constants.selectors import FDASelectors, ShopifySelectors
from ..constants.enums import (
    ProcessStep, ProcessResult, SystemConfiguration, 
    UserResponse, SystemModule, OperationType, ScreenshotType
)

# Local imports - Core
from ..core.logging_config import init_logging
from ..core.selenium_manager import SeleniumManager
from ..core.wait_helper import WaitHelper
from ..core.screenshot_manager import ScreenshotManager
from ..core.performance_tracker import PerformanceTracker

# Local imports - Optimizations
from ..optimizations.element_cache import ElementCache
from ..optimizations.screenshot_manager import OptimizedScreenshotManager
from ..optimizations.adaptive_timeouts import AdaptiveTimeouts
from ..optimizations.performance_tracker import OptimizedPerformanceTracker

# Local imports - FDA
from ..fda.login import complete_fda_login
from ..fda.automation.step_01_copy_selection import execute_step_01
from ..fda.automation.step_02_edit_information import execute_step_02_edit_information
from ..fda.automation.step_03_final_save import execute_step_03

# Local imports - Utilities
from ..utils.helpers import show_paths, validate_files


class ImportStatus:
    """Clase para verificar disponibilidad de dependencias"""
    
    @staticmethod
    def check_selenium() -> bool:
        """Verifica si Selenium está disponible"""
        return SELENIUM_AVAILABLE
    
    @staticmethod
    def check_pil() -> bool:
        """Verifica si PIL/Pillow está disponible"""
        return PIL_AVAILABLE
    
    @staticmethod
    def check_pandas() -> bool:
        """Verifica si Pandas está disponible"""
        return PANDAS_AVAILABLE
    
    @staticmethod
    def get_status_report() -> Dict[str, bool]:
        """Retorna reporte de estado de todas las dependencias"""
        return {
            'selenium': SELENIUM_AVAILABLE,
            'pil': PIL_AVAILABLE, 
            'pandas': PANDAS_AVAILABLE
        }
    
    @staticmethod
    def validate_required_dependencies(required: List[str]) -> bool:
        """Valida que las dependencias requeridas están disponibles"""
        status = ImportStatus.get_status_report()
        
        for dep in required:
            if dep not in status or not status[dep]:
                print(f"❌ Dependencia requerida no disponible: {dep}")
                return False
        
        return True


class DependencyError(Exception):
    """Error cuando una dependencia requerida no está disponible"""
    def __init__(self, dependency: str, suggestion: str = ""):
        message = f"Dependencia '{dependency}' no está disponible"
        if suggestion:
            message += f". {suggestion}"
        super().__init__(message)
        self.dependency = dependency


def require_selenium():
    """Decorador que requiere Selenium"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not SELENIUM_AVAILABLE:
                raise DependencyError(
                    "selenium", 
                    "Instala con: pip install selenium"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_pil():
    """Decorador que requiere PIL/Pillow"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not PIL_AVAILABLE:
                raise DependencyError(
                    "PIL/Pillow", 
                    "Instala con: pip install Pillow"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_pandas():
    """Decorador que requiere Pandas"""  
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not PANDAS_AVAILABLE:
                raise DependencyError(
                    "pandas", 
                    "Instala con: pip install pandas"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Importaciones consolidadas por contexto
class CoreImports:
    """Importaciones para funcionalidad core"""
    
    @staticmethod
    def get_selenium_imports():
        """Retorna imports de Selenium si están disponibles"""
        if not SELENIUM_AVAILABLE:
            return None
        
        return {
            'webdriver': webdriver,
            'WebDriver': WebDriver,
            'WebDriverWait': WebDriverWait,
            'EC': EC,
            'By': By,
            'Keys': Keys,
            'ActionChains': ActionChains,
            'ChromeService': ChromeService,
            'ChromeOptions': ChromeOptions,
            'exceptions': {
                'TimeoutException': TimeoutException,
                'NoSuchElementException': NoSuchElementException,
                'WebDriverException': WebDriverException,
                'ElementNotInteractableException': ElementNotInteractableException,
                'StaleElementReferenceException': StaleElementReferenceException
            }
        }
    
    @staticmethod
    def get_logging_imports():
        """Retorna imports para logging"""
        return {
            'logging': logging,
            'init_logging': init_logging
        }
    
    @staticmethod
    def get_performance_imports():
        """Retorna imports para performance tracking"""
        return {
            'PerformanceTracker': PerformanceTracker,
            'OptimizedPerformanceTracker': OptimizedPerformanceTracker,
            'AdaptiveTimeouts': AdaptiveTimeouts
        }


class UtilityImports:
    """Importaciones para utilidades"""
    
    @staticmethod
    def get_path_imports():
        """Retorna imports relacionados con paths"""
        return {
            'BASE_DIR': BASE_DIR,
            'DATA_DIR': DATA_DIR,
            'LOGS_DIR': LOGS_DIR,
            'SCREENSHOTS_DIR': SCREENSHOTS_DIR,
            'ORDER_SAMPLE_FILE': ORDER_SAMPLE_FILE,
            'ensure_directories': ensure_directories,
            'show_paths': show_paths
        }
    
    @staticmethod
    def get_timing_imports():
        """Retorna imports relacionados con timings"""
        return {
            'SleepTimes': SleepTimes,
            'ElementTimeouts': ElementTimeouts
        }
    
    @staticmethod
    def get_message_imports():
        """Retorna imports relacionados con mensajes"""
        return {
            'ProcessMessages': ProcessMessages,
            'LogMessages': LogMessages,
            'UserMessages': UserMessages
        }


class OptimizationImports:
    """Importaciones para optimizaciones avanzadas"""
    
    @staticmethod
    def get_cache_imports():
        """Retorna imports para caching"""
        return {
            'ElementCache': ElementCache
        }
    
    @staticmethod
    def get_screenshot_imports():
        """Retorna imports para screenshots optimizados"""
        return {
            'ScreenshotManager': ScreenshotManager,
            'OptimizedScreenshotManager': OptimizedScreenshotManager
        }


def create_optimized_imports_context():
    """Crea contexto con todas las importaciones optimizadas disponibles"""
    context = {}
    
    # Core imports
    if SELENIUM_AVAILABLE:
        context.update(CoreImports.get_selenium_imports() or {})
    
    context.update(CoreImports.get_logging_imports())
    context.update(CoreImports.get_performance_imports())
    
    # Utility imports
    context.update(UtilityImports.get_path_imports())
    context.update(UtilityImports.get_timing_imports())
    context.update(UtilityImports.get_message_imports())
    
    # Optimization imports
    context.update(OptimizationImports.get_cache_imports())
    context.update(OptimizationImports.get_screenshot_imports())
    
    return context


# Función de conveniencia para setup común
def setup_common_environment():
    """Setup común para todos los módulos"""
    # Asegurar directorios
    ensure_directories()
    
    # Verificar dependencias críticas
    status = ImportStatus.get_status_report()
    
    if not status['selenium']:
        print("⚠️ Selenium no disponible - funcionalidad web limitada")
    
    if not status['pil']:
        print("⚠️ PIL/Pillow no disponible - optimización de screenshots deshabilitada")
    
    return status 