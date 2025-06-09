"""
Optimized Logger - Sistema de logging inteligente sin spam
Reduce verbosidad, elimina duplicaciones y maneja limpieza automática
"""

import os
import gzip
import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Set, Optional
from logging.handlers import RotatingFileHandler
import threading


class SpamFilter:
    """Filtro inteligente para evitar spam de logs"""
    
    def __init__(self, time_window: int = 10, max_duplicates: int = 3):
        self.time_window = time_window  # Ventana de tiempo en segundos
        self.max_duplicates = max_duplicates  # Máximo de mensajes duplicados
        self.message_cache: Dict[str, list] = {}  # Cache de mensajes recientes
        self.lock = threading.Lock()
    
    def should_log(self, message: str, level: str) -> bool:
        """Determina si un mensaje debe ser loggeado o es spam"""
        current_time = time.time()
        message_key = f"{level}:{message}"
        
        with self.lock:
            # Limpiar mensajes antiguos
            if message_key in self.message_cache:
                self.message_cache[message_key] = [
                    t for t in self.message_cache[message_key] 
                    if current_time - t < self.time_window
                ]
            else:
                self.message_cache[message_key] = []
            
            # Verificar si excede el límite
            recent_count = len(self.message_cache[message_key])
            
            if recent_count >= self.max_duplicates:
                # Solo loggear cada 5 repeticiones adicionales
                if recent_count % 5 == 0:
                    self.message_cache[message_key].append(current_time)
                    return True, f"[REPETIDO {recent_count}x] {message}"
                return False, None
            else:
                self.message_cache[message_key].append(current_time)
                return True, message


class CompactFormatter(logging.Formatter):
    """Formatter compacto para logs menos verbosos"""
    
    def format(self, record):
        # Timestamp compacto
        timestamp = datetime.fromtimestamp(record.created).strftime('%H:%M:%S')
        
        # Level súper compacto
        level_map = {
            'DEBUG': '🔍',
            'INFO': '•', 
            'WARNING': '⚠',
            'ERROR': '❌',
            'CRITICAL': '🚨'
        }
        level_icon = level_map.get(record.levelname, record.levelname)
        
        # Módulo compacto (usar source_module para evitar conflicto)
        module = getattr(record, 'source_module', 'main')
        module_short = module[:8] if len(module) > 8 else module
        
        # Mensaje limpio
        message = record.getMessage()
        
        # Formato súper compacto: TIME ICON [MOD] MSG
        return f"{timestamp} {level_icon} [{module_short}] {message}"


class OptimizedLogger:
    """Logger optimizado con filtros anti-spam y limpieza automática"""
    
    def __init__(self, session_id: str = None, max_file_size: int = 5*1024*1024, backup_count: int = 3):
        self.session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.spam_filter = SpamFilter()
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
        
        # Logger principal
        self.logger = logging.getLogger(f"fda_automation_{self.session_id}")
        self.logger.setLevel(logging.INFO)  # Solo INFO+ por defecto
        
        # Evitar duplicar handlers
        if not self.logger.handlers:
            self._setup_handlers(max_file_size, backup_count)
        
        # Limpieza automática al inicializar
        self._auto_cleanup()
        
        # Log inicial limpio
        self.info("🚀 Sistema iniciado", module="system")
    
    def _setup_handlers(self, max_file_size: int, backup_count: int):
        """Configura handlers optimizados"""
        formatter = CompactFormatter()
        
        # Handler de archivo con rotación
        log_file = self.logs_dir / f"fda_automation.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Handler de consola solo para WARNINGS+
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(CompactFormatter())
        self.logger.addHandler(console_handler)
    
    def _auto_cleanup(self):
        """Limpieza automática de logs antiguos"""
        try:
            # Comprimir logs de más de 1 día
            self._compress_old_logs()
            
            # Eliminar logs comprimidos de más de 7 días
            self._cleanup_old_compressed_logs()
            
            # Limpiar screenshots antiguos
            self._cleanup_old_screenshots()
            
        except Exception as e:
            self.warning(f"Error en limpieza automática: {e}", module="cleanup")
    
    def _compress_old_logs(self):
        """Comprime logs de más de 1 día"""
        cutoff_time = datetime.now() - timedelta(days=1)
        
        for log_file in self.logs_dir.glob("*.log*"):
            if log_file.suffix == '.gz':
                continue
                
            try:
                file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
                if file_time < cutoff_time and log_file.stat().st_size > 1024:  # > 1KB
                    compressed_file = log_file.with_suffix(log_file.suffix + '.gz')
                    
                    with open(log_file, 'rb') as f_in:
                        with gzip.open(compressed_file, 'wb') as f_out:
                            f_out.writelines(f_in)
                    
                    log_file.unlink()  # Eliminar original
                    
            except Exception as e:
                pass  # Silenciar errores de compresión individual
    
    def _cleanup_old_compressed_logs(self):
        """Elimina logs comprimidos antiguos"""
        cutoff_time = datetime.now() - timedelta(days=7)
        
        for gz_file in self.logs_dir.glob("*.gz"):
            try:
                file_time = datetime.fromtimestamp(gz_file.stat().st_mtime)
                if file_time < cutoff_time:
                    gz_file.unlink()
            except:
                pass
    
    def _cleanup_old_screenshots(self):
        """Limpia screenshots antiguos"""
        screenshots_dir = self.logs_dir / "screenshots"
        if not screenshots_dir.exists():
            return
            
        cutoff_time = datetime.now() - timedelta(days=3)
        
        for screenshot in screenshots_dir.glob("*.png"):
            try:
                file_time = datetime.fromtimestamp(screenshot.stat().st_mtime)
                if file_time < cutoff_time:
                    screenshot.unlink()
            except:
                pass
    
    def _log_with_filter(self, level: str, message: str, module: str = "main", **kwargs):
        """Log con filtro anti-spam"""
        should_log, filtered_message = self.spam_filter.should_log(message, level)
        
        if should_log:
            # Agregar información de módulo extra (evitar conflicto con LogRecord)
            extra = {'source_module': module}
            extra.update(kwargs)
            
            getattr(self.logger, level.lower())(filtered_message, extra=extra)
    
    def debug(self, message: str, module: str = "main", **kwargs):
        """Debug log (deshabilitado por defecto)"""
        if self.logger.level <= logging.DEBUG:
            self._log_with_filter("DEBUG", message, module, **kwargs)
    
    def info(self, message: str, module: str = "main", **kwargs):
        """Info log con filtro anti-spam"""
        self._log_with_filter("INFO", message, module, **kwargs)
    
    def warning(self, message: str, module: str = "main", **kwargs):
        """Warning log"""
        self._log_with_filter("WARNING", message, module, **kwargs)
    
    def error(self, message: str, module: str = "main", exception: Exception = None, **kwargs):
        """Error log con excepción opcional"""
        if exception:
            message = f"{message}: {str(exception)}"
        self._log_with_filter("ERROR", message, module, **kwargs)
    
    def critical(self, message: str, module: str = "main", exception: Exception = None, **kwargs):
        """Critical log"""
        if exception:
            message = f"{message}: {str(exception)}"
        self._log_with_filter("CRITICAL", message, module, **kwargs)
    
    def step(self, step_name: str, status: str = "start", duration: float = None):
        """Log optimizado para pasos de proceso"""
        if status == "start":
            self.info(f"🚀 {step_name}", module="process")
        elif status == "success":
            duration_str = f" ({duration:.1f}s)" if duration else ""
            self.info(f"✅ {step_name}{duration_str}", module="process")
        elif status == "error":
            self.error(f"❌ {step_name} falló", module="process")
    
    def performance(self, operation: str, duration: float, metadata: Dict = None):
        """Log optimizado para métricas de performance"""
        if duration > 5.0:  # Solo loggear operaciones lentas
            meta_str = f" ({metadata})" if metadata else ""
            self.warning(f"🐌 {operation}: {duration:.1f}s{meta_str}", module="perf")
    
    def get_log_stats(self) -> Dict:
        """Estadísticas del sistema de logging"""
        log_files = list(self.logs_dir.glob("*.log*"))
        compressed_files = list(self.logs_dir.glob("*.gz"))
        
        total_size = sum(f.stat().st_size for f in log_files)
        compressed_size = sum(f.stat().st_size for f in compressed_files)
        
        return {
            "active_logs": len(log_files),
            "compressed_logs": len(compressed_files),
            "total_size_mb": round(total_size / (1024*1024), 2),
            "compressed_size_mb": round(compressed_size / (1024*1024), 2),
            "spam_filtered_messages": len(self.spam_filter.message_cache),
            "logs_directory": str(self.logs_dir)
        }


class QuietMode:
    """Context manager para modo silencioso temporal"""
    
    def __init__(self, logger: OptimizedLogger):
        self.logger = logger
        self.original_level = None
    
    def __enter__(self):
        self.original_level = self.logger.logger.level
        self.logger.logger.setLevel(logging.ERROR)  # Solo errores
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.logger.setLevel(self.original_level)


# Singleton global para evitar múltiples instancias
_optimized_logger_instance = None

def get_optimized_logger(session_id: str = None) -> OptimizedLogger:
    """Obtiene instancia singleton del logger optimizado"""
    global _optimized_logger_instance
    
    if _optimized_logger_instance is None:
        _optimized_logger_instance = OptimizedLogger(session_id)
    
    return _optimized_logger_instance


def init_optimized_logging(session_id: str = None) -> OptimizedLogger:
    """Inicializa sistema de logging optimizado"""
    logger = get_optimized_logger(session_id)
    
    # Log inicial con estadísticas
    stats = logger.get_log_stats()
    logger.info(f"📊 Logs: {stats['active_logs']} activos, {stats['compressed_logs']} comprimidos", module="system")
    
    return logger 