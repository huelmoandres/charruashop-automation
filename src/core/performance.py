"""
Sistema de métricas de performance y profiling para FDA Automation
Incluye tracking optimizado de operaciones, caché de selectores y análisis de tiempos
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from contextlib import contextmanager
from dataclasses import dataclass, field
import json
from pathlib import Path
from ..constants.timeouts import adaptive_timeouts
from ..utils.selenium_helpers import ElementCache

@dataclass
class PerformanceMetric:
    """Métrica individual de performance"""
    name: str
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    status: str = "running"  # running, completed, failed
    
    def complete(self, metadata: Optional[Dict] = None):
        """Marca la métrica como completada"""
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        self.status = "completed"
        if metadata:
            self.metadata.update(metadata)
    
    def fail(self, error: str, metadata: Optional[Dict] = None):
        """Marca la métrica como fallida"""
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        self.status = "failed"
        self.metadata["error"] = error
        if metadata:
            self.metadata.update(metadata)

class OptimizedPerformanceTracker:
    """
    Tracker de performance optimizado con análisis en tiempo real
    """
    
    def __init__(self, logger=None, session_id: str = None):
        """
        Inicializa el tracker optimizado de performance
        
        Args:
            logger: Instancia del logger
            session_id: ID único de la sesión
        """
        self.logger = logger
        self.session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.metrics: List[PerformanceMetric] = []
        self.active_metrics: Dict[str, PerformanceMetric] = {}
        self.session_start = time.time()
        
        # Cache para análisis rápidos
        self._stats_cache = {}
        self._cache_timestamp = 0
        self._cache_ttl = 30  # segundos
        
        if self.logger:
            self.logger.info("🎯 Performance tracking optimizado iniciado", extra={
                "session_id": self.session_id
            })
    
    @contextmanager
    def track(self, operation_name: str, metadata: Optional[Dict] = None):
        """
        Context manager optimizado para tracking de operaciones
        """
        metric = PerformanceMetric(
            name=operation_name,
            start_time=time.time(),
            metadata=metadata or {}
        )
        
        self.active_metrics[operation_name] = metric
        
        try:
            yield metric
            metric.complete()
            
            # Registrar en sistema de timeouts adaptativos
            adaptive_timeouts.record_operation_time(operation_name, metric.duration)
            
            if self.logger:
                self.logger.info(f"✅ {operation_name}: {metric.duration:.2f}s", extra={
                    "operation": operation_name,
                    "duration": metric.duration,
                    "status": "completed"
                })
        except Exception as e:
            metric.fail(str(e))
            
            if self.logger:
                self.logger.error(f"❌ {operation_name}: {metric.duration:.2f}s - {e}", extra={
                    "operation": operation_name,
                    "duration": metric.duration,
                    "error": str(e),
                    "status": "failed"
                })
            raise
        finally:
            self.metrics.append(metric)
            if operation_name in self.active_metrics:
                del self.active_metrics[operation_name]
            
            # Invalidar cache de estadísticas
            self._invalidate_stats_cache()
    
    def track_async(self, operation_name: str, metadata: Optional[Dict] = None) -> PerformanceMetric:
        """
        Inicia tracking asíncrono de una operación (sin context manager)
        """
        metric = PerformanceMetric(
            name=operation_name,
            start_time=time.time(),
            metadata=metadata or {}
        )
        self.active_metrics[operation_name] = metric
        return metric
    
    def complete_async(self, operation_name: str, metadata: Optional[Dict] = None):
        """
        Completa tracking asíncrono de una operación
        """
        if operation_name in self.active_metrics:
            metric = self.active_metrics[operation_name]
            metric.complete(metadata)
            
            # Registrar en sistema adaptativo
            adaptive_timeouts.record_operation_time(operation_name, metric.duration)
            
            self.metrics.append(metric)
            del self.active_metrics[operation_name]
            self._invalidate_stats_cache()
            
            if self.logger:
                self.logger.info(f"✅ {operation_name}: {metric.duration:.2f}s (async)", extra={
                    "operation": operation_name,
                    "duration": metric.duration,
                    "status": "completed",
                    "async": True
                })
    
    def _invalidate_stats_cache(self):
        """Invalida el cache de estadísticas"""
        self._cache_timestamp = 0
    
    def _get_cached_stats(self) -> Optional[Dict]:
        """Obtiene estadísticas del cache si están vigentes"""
        current_time = time.time()
        if current_time - self._cache_timestamp < self._cache_ttl:
            return self._stats_cache
        return None
    
    def get_performance_summary(self, force_refresh: bool = False) -> Dict:
        """
        Obtiene resumen optimizado de performance con cache
        """
        if not force_refresh:
            cached = self._get_cached_stats()
            if cached:
                return cached
        
        completed_metrics = [m for m in self.metrics if m.status == "completed"]
        failed_metrics = [m for m in self.metrics if m.status == "failed"]
        
        if not completed_metrics and not failed_metrics:
            return {"error": "No hay métricas disponibles"}
        
        total_duration = sum(m.duration for m in completed_metrics if m.duration)
        session_duration = time.time() - self.session_start
        
        # Análisis de operaciones por tipo
        operation_stats = {}
        for metric in completed_metrics:
            if metric.name not in operation_stats:
                operation_stats[metric.name] = {
                    "count": 0,
                    "total_time": 0,
                    "min_time": float('inf'),
                    "max_time": 0,
                    "avg_time": 0,
                    "recent_trend": []
                }
            
            stats = operation_stats[metric.name]
            stats["count"] += 1
            stats["total_time"] += metric.duration
            stats["min_time"] = min(stats["min_time"], metric.duration)
            stats["max_time"] = max(stats["max_time"], metric.duration)
            stats["recent_trend"].append(metric.duration)
            
            # Mantener solo últimas 5 mediciones para trend
            if len(stats["recent_trend"]) > 5:
                stats["recent_trend"].pop(0)
        
        # Calcular promedios
        for stats in operation_stats.values():
            stats["avg_time"] = stats["total_time"] / stats["count"]
        
        # Identificar operaciones más lentas
        slowest_operations = sorted(
            operation_stats.items(),
            key=lambda x: x[1]["avg_time"],
            reverse=True
        )[:3]
        
        # Cache y system stats
        cache = ElementCache()
        cache_stats = cache.get_stats()
        
        summary = {
            "session_id": self.session_id,
            "session_duration": f"{session_duration:.2f}s",
            "total_operations": len(completed_metrics),
            "failed_operations": len(failed_metrics),
            "success_rate": f"{(len(completed_metrics) / (len(completed_metrics) + len(failed_metrics)) * 100):.1f}%" if (completed_metrics or failed_metrics) else "0%",
            "total_tracked_time": f"{total_duration:.2f}s",
            "efficiency": f"{(total_duration / session_duration * 100):.1f}%" if session_duration > 0 else "0%",
            "slowest_operations": [
                {
                    "name": name,
                    "avg_time": f"{stats['avg_time']:.2f}s",
                    "count": stats["count"]
                }
                for name, stats in slowest_operations
            ],
            "cache_performance": cache_stats,
            "adaptive_timeouts": adaptive_timeouts.get_performance_stats(),
            "operation_details": operation_stats
        }
        
        # Cache del resultado
        self._stats_cache = summary
        self._cache_timestamp = time.time()
        
        return summary
    
    def log_session_summary(self):
        """
        Log optimizado del resumen de la sesión
        """
        summary = self.get_performance_summary()
        
        if self.logger:
            self.logger.info("📊 RESUMEN DE PERFORMANCE DE LA SESIÓN", extra=summary)
            self.logger.info(f"   Duración total: {summary['session_duration']}")
            self.logger.info(f"   Métricas totales: {summary['total_operations']}")
            self.logger.info(f"   Tasa de éxito: {summary['success_rate']}")
            
            if summary["slowest_operations"]:
                self.logger.info("🐌 Pasos más lentos:")
                for op in summary["slowest_operations"]:
                    self.logger.info(f"   • {op['name']}: {op['avg_time']}")
            
            if summary["failed_operations"] > 0:
                self.logger.warning("⚠️ Pasos con más fallos:")
                # Análisis de fallos podría agregarse aquí
        
        # Guardar resumen detallado en archivo
        self._save_session_report(summary)
    
    def _save_session_report(self, summary: Dict):
        """
        Guarda reporte detallado de la sesión en archivo
        """
        try:
            reports_dir = Path("logs/performance")
            reports_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = reports_dir / f"performance_report_{timestamp}.json"
            
            # Preparar datos para JSON
            json_summary = summary.copy()
            json_summary["metrics_detail"] = [
                {
                    "name": m.name,
                    "duration": m.duration,
                    "status": m.status,
                    "metadata": m.metadata
                }
                for m in self.metrics
            ]
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(json_summary, f, indent=2, ensure_ascii=False)
            
            if self.logger:
                self.logger.info("📋 Reporte de performance guardado", extra={
                    "report_file": str(report_file)
                })
        
        except Exception as e:
            if self.logger:
                self.logger.warning("Error guardando reporte de performance", extra={
                    "error": str(e)
                })

def create_performance_tracker(logger=None, session_id: str = None) -> OptimizedPerformanceTracker:
    """
    Crea una instancia optimizada del PerformanceTracker
    
    Args:
        logger: Instancia del logger
        session_id: ID único de la sesión
        
    Returns:
        Instancia de OptimizedPerformanceTracker
    """
    if logger:
        logger.info("🎯 Performance tracking optimizado iniciado")
    
    return OptimizedPerformanceTracker(logger, session_id) 