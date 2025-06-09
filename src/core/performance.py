"""
Sistema de métricas de performance optimizado - Anti-spam
Tracking esencial sin verbosidad excesiva
"""

import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from contextlib import contextmanager
from dataclasses import dataclass, field

try:
    from .optimized_logger import get_optimized_logger
except ImportError:
    # Fallback para compatibilidad
    import logging
    get_optimized_logger = lambda: logging.getLogger("performance")


@dataclass
class PerformanceMetric:
    """Métrica optimizada de performance"""
    name: str
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    status: str = "running"
    
    def complete(self, metadata: Optional[Dict] = None):
        """Completa métrica sin spam de logs"""
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        self.status = "completed"
        if metadata:
            self.metadata.update(metadata)
    
    def fail(self, error: str, metadata: Optional[Dict] = None):
        """Marca métrica como fallida"""
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        self.status = "failed"
        self.metadata["error"] = error
        if metadata:
            self.metadata.update(metadata)


class OptimizedPerformanceTracker:
    """Tracker de performance sin spam - Solo métricas esenciales"""
    
    def __init__(self, logger=None, session_id: str = None):
        self.logger = logger or get_optimized_logger()
        self.session_id = session_id or f"perf_{datetime.now().strftime('%H%M%S')}"
        self.metrics: List[PerformanceMetric] = []
        self.active_metrics: Dict[str, PerformanceMetric] = {}
        self.session_start = time.time()
        
        # Configuración anti-spam
        self.log_threshold = 2.0  # Solo loggear operaciones >2s
        self.critical_operations = {'selenium', 'fda', 'step', 'process', 'screenshot'}
        
        # Log inicial silencioso
        self.logger.info("Tracker iniciado", module="perf")
    
    @contextmanager
    def track(self, operation_name: str, metadata: Optional[Dict] = None):
        """Context manager silencioso para tracking"""
        metric = PerformanceMetric(
            name=operation_name,
            start_time=time.time(),
            metadata=metadata or {}
        )
        
        self.active_metrics[operation_name] = metric
        
        try:
            yield metric
            metric.complete()
            
            # Log inteligente - solo si es relevante
            self._smart_log(metric)
            
        except Exception as e:
            metric.fail(str(e))
            # Errores siempre se loggean
            self.logger.error(f"{operation_name} falló: {e}", module="perf")
            raise
        finally:
            self.metrics.append(metric)
            if operation_name in self.active_metrics:
                del self.active_metrics[operation_name]
    
    def _smart_log(self, metric: PerformanceMetric):
        """Logging inteligente - reduce spam significativamente"""
        # Solo loggear si:
        # 1. Es una operación crítica Y dura >1s
        # 2. Cualquier operación que dure >2s
        # 3. Operaciones que fallan
        
        is_critical = any(keyword in metric.name.lower() 
                         for keyword in self.critical_operations)
        
        if metric.status == "failed":
            self.logger.error(f"❌ {metric.name}: {metric.duration:.1f}s", module="perf")
        elif (is_critical and metric.duration > 1.0) or metric.duration > self.log_threshold:
            if metric.duration > 10.0:
                self.logger.warning(f"🐌 {metric.name}: {metric.duration:.1f}s", module="perf")
            else:
                self.logger.info(f"⏱️ {metric.name}: {metric.duration:.1f}s", module="perf")
    
    def track_step(self, step_name: str, metadata: Optional[Dict] = None):
        """Tracking específico para pasos (siempre relevante)"""
        return self.track(f"step_{step_name}", metadata)
    
    def log_milestone(self, milestone_name: str, details: str = None):
        """Milestone importante - siempre se loggea"""
        elapsed = time.time() - self.session_start
        detail_str = f" - {details}" if details else ""
        self.logger.info(f"🎯 {milestone_name} ({elapsed:.1f}s){detail_str}", module="milestone")
    
    def get_performance_summary(self) -> Dict:
        """Resumen compacto de performance"""
        completed = [m for m in self.metrics if m.status == "completed"]
        failed = [m for m in self.metrics if m.status == "failed"]
        
        if not completed and not failed:
            return {"status": "no_data"}
        
        total_ops = len(completed) + len(failed)
        total_time = sum(m.duration for m in completed if m.duration)
        session_time = time.time() - self.session_start
        
        # Solo operaciones lentas para el resumen
        slow_ops = [m for m in completed if m.duration and m.duration > 1.0]
        
        return {
            "session_duration": round(session_time, 1),
            "total_operations": total_ops,
            "slow_operations": len(slow_ops),
            "failed_operations": len(failed),
            "total_processing_time": round(total_time, 1),
            "efficiency": round((total_time / session_time * 100), 1) if session_time > 0 else 0
        }
    
    def log_session_summary(self):
        """Resumen final compacto"""
        try:
            summary = self.get_performance_summary()
            
            if summary.get("status") == "no_data":
                return
            
            # Solo mostrar resumen si hay datos significativos
            if (summary["session_duration"] > 30 or 
                summary["slow_operations"] > 2 or 
                summary["failed_operations"] > 0):
                
                self.logger.info(
                    f"Sesión: {summary['session_duration']}s, "
                    f"{summary['slow_operations']} ops lentas, "
                    f"{summary['failed_operations']} fallos",
                    module="summary"
                )
                
                if summary["efficiency"] < 50 and summary["session_duration"] > 60:
                    self.logger.warning(f"Eficiencia baja: {summary['efficiency']}%", module="summary")
            
        except Exception:
            pass  # Silenciar errores de resumen
    
    def get_critical_metrics(self) -> List[Dict]:
        """Solo métricas críticas para debugging"""
        critical_metrics = []
        
        for metric in self.metrics:
            if (metric.duration and metric.duration > 5.0) or metric.status == "failed":
                critical_metrics.append({
                    "name": metric.name,
                    "duration": metric.duration,
                    "status": metric.status,
                    "metadata": metric.metadata
                })
        
        return critical_metrics
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.log_session_summary()


def create_performance_tracker(logger=None, session_id: str = None) -> OptimizedPerformanceTracker:
    """Factory function para crear tracker optimizado"""
    return OptimizedPerformanceTracker(logger, session_id)


# Singleton para uso global
_global_tracker = None

def get_global_performance_tracker() -> OptimizedPerformanceTracker:
    """Obtiene instancia global del tracker"""
    global _global_tracker
    if _global_tracker is None:
        _global_tracker = OptimizedPerformanceTracker()
    return _global_tracker 