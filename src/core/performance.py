"""
Sistema de Métricas de Performance para Automatización FDA/Shopify
Tracks timing, success rates, and other performance indicators
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from contextlib import contextmanager
import json

@dataclass
class PerformanceMetric:
    """Métrica individual de performance"""
    name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    success: bool = True
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def finish(self, success: bool = True, error_message: Optional[str] = None):
        """Marca la métrica como completada"""
        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
        self.success = success
        self.error_message = error_message
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la métrica a diccionario"""
        return {
            'name': self.name,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration': self.duration,
            'success': self.success,
            'error_message': self.error_message,
            'metadata': self.metadata
        }

class PerformanceTracker:
    """
    Tracker de performance para medir y analizar el rendimiento de la automatización
    """
    
    def __init__(self, logger=None):
        """
        Inicializa el tracker de performance
        
        Args:
            logger: Instancia del AutomationLogger
        """
        self.logger = logger
        self.metrics: List[PerformanceMetric] = []
        self.session_start = datetime.now()
        self.active_metrics: Dict[str, PerformanceMetric] = {}
        
        # Métricas agregadas
        self.step_times: Dict[str, List[float]] = {}
        self.success_rates: Dict[str, Dict[str, int]] = {}
        
        if self.logger:
            self.logger.info("🎯 Performance tracking iniciado", module='performance')
    
    def start_metric(self, name: str, metadata: Optional[Dict[str, Any]] = None) -> PerformanceMetric:
        """
        Inicia el tracking de una métrica
        
        Args:
            name: Nombre de la métrica
            metadata: Metadatos adicionales
            
        Returns:
            Instancia de la métrica iniciada
        """
        metric = PerformanceMetric(
            name=name,
            start_time=datetime.now(),
            metadata=metadata or {}
        )
        
        self.active_metrics[name] = metric
        
        if self.logger:
            self.logger.debug(f"⏱️ Iniciando tracking: {name}", module='performance')
        
        return metric
    
    def finish_metric(self, name: str, success: bool = True, error_message: Optional[str] = None):
        """
        Finaliza el tracking de una métrica
        
        Args:
            name: Nombre de la métrica
            success: Si la operación fue exitosa
            error_message: Mensaje de error si aplica
        """
        if name not in self.active_metrics:
            if self.logger:
                self.logger.warning(f"⚠️ Métrica no encontrada para finalizar: {name}", module='performance')
            return
        
        metric = self.active_metrics[name]
        metric.finish(success=success, error_message=error_message)
        
        # Agregar a la lista de métricas completadas
        self.metrics.append(metric)
        
        # Actualizar estadísticas agregadas
        self._update_aggregated_stats(metric)
        
        # Remover de métricas activas
        del self.active_metrics[name]
        
        # Log de la métrica completada
        if self.logger:
            status = "✅" if success else "❌"
            self.logger.info(
                f"{status} {name}: {metric.duration:.2f}s", 
                module='performance'
            )
            
            # Log en archivo de performance
            perf_data = {
                'metric': metric.to_dict(),
                'timestamp': datetime.now().isoformat()
            }
            self.logger.debug(
                f"Performance data: {json.dumps(perf_data, indent=2)}", 
                module='performance'
            )
    
    def _update_aggregated_stats(self, metric: PerformanceMetric):
        """Actualiza estadísticas agregadas"""
        name = metric.name
        
        # Tiempos por paso
        if name not in self.step_times:
            self.step_times[name] = []
        if metric.duration:
            self.step_times[name].append(metric.duration)
        
        # Tasas de éxito
        if name not in self.success_rates:
            self.success_rates[name] = {'success': 0, 'failure': 0}
        
        if metric.success:
            self.success_rates[name]['success'] += 1
        else:
            self.success_rates[name]['failure'] += 1
    
    @contextmanager
    def track(self, name: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Context manager para tracking automático
        
        Args:
            name: Nombre de la métrica
            metadata: Metadatos adicionales
        """
        metric = self.start_metric(name, metadata)
        try:
            yield metric
            self.finish_metric(name, success=True)
        except Exception as e:
            self.finish_metric(name, success=False, error_message=str(e))
            raise
    
    def get_step_statistics(self, step_name: str) -> Dict[str, Any]:
        """
        Obtiene estadísticas de un paso específico
        
        Args:
            step_name: Nombre del paso
            
        Returns:
            Diccionario con estadísticas del paso
        """
        if step_name not in self.step_times:
            return {'error': f'No data for step: {step_name}'}
        
        times = self.step_times[step_name]
        success_data = self.success_rates.get(step_name, {'success': 0, 'failure': 0})
        
        total_executions = success_data['success'] + success_data['failure']
        success_rate = (success_data['success'] / total_executions * 100) if total_executions > 0 else 0
        
        return {
            'step_name': step_name,
            'total_executions': total_executions,
            'success_rate': f"{success_rate:.1f}%",
            'successful_executions': success_data['success'],
            'failed_executions': success_data['failure'],
            'timing_stats': {
                'min_time': min(times),
                'max_time': max(times),
                'avg_time': sum(times) / len(times),
                'total_time': sum(times)
            },
            'last_execution': times[-1] if times else None
        }
    
    def get_session_summary(self) -> Dict[str, Any]:
        """
        Obtiene un resumen completo de la sesión
        
        Returns:
            Diccionario con resumen de performance
        """
        session_duration = (datetime.now() - self.session_start).total_seconds()
        total_metrics = len(self.metrics)
        successful_metrics = len([m for m in self.metrics if m.success])
        
        # Top pasos más lentos
        avg_times = {}
        for step, times in self.step_times.items():
            avg_times[step] = sum(times) / len(times)
        
        slowest_steps = sorted(avg_times.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Pasos con más fallos
        failure_rates = {}
        for step, rates in self.success_rates.items():
            total = rates['success'] + rates['failure']
            if total > 0:
                failure_rates[step] = rates['failure'] / total * 100
        
        most_failures = sorted(failure_rates.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'session_info': {
                'start_time': self.session_start.isoformat(),
                'duration': f"{session_duration:.2f}s",
                'total_metrics': total_metrics,
                'successful_metrics': successful_metrics,
                'success_rate': f"{(successful_metrics/total_metrics*100):.1f}%" if total_metrics > 0 else "0%"
            },
            'performance_insights': {
                'slowest_steps': [{'step': step, 'avg_time': f"{time:.2f}s"} for step, time in slowest_steps],
                'steps_with_most_failures': [{'step': step, 'failure_rate': f"{rate:.1f}%"} for step, rate in most_failures],
                'total_execution_time': f"{sum([sum(times) for times in self.step_times.values()]):.2f}s"
            },
            'step_breakdown': [self.get_step_statistics(step) for step in self.step_times.keys()]
        }
    
    def log_session_summary(self):
        """Loguea el resumen de la sesión"""
        summary = self.get_session_summary()
        
        if self.logger:
            self.logger.info("📊 RESUMEN DE PERFORMANCE DE LA SESIÓN", module='performance')
            self.logger.info(f"   Duración total: {summary['session_info']['duration']}", module='performance')
            self.logger.info(f"   Métricas totales: {summary['session_info']['total_metrics']}", module='performance')
            self.logger.info(f"   Tasa de éxito: {summary['session_info']['success_rate']}", module='performance')
            
            # Pasos más lentos
            if summary['performance_insights']['slowest_steps']:
                self.logger.info("🐌 Pasos más lentos:", module='performance')
                for step_info in summary['performance_insights']['slowest_steps'][:3]:
                    self.logger.info(f"   • {step_info['step']}: {step_info['avg_time']}", module='performance')
            
            # Pasos con más fallos
            if summary['performance_insights']['steps_with_most_failures']:
                self.logger.warning("⚠️ Pasos con más fallos:", module='performance')
                for step_info in summary['performance_insights']['steps_with_most_failures'][:3]:
                    if float(step_info['failure_rate'].replace('%', '')) > 0:
                        self.logger.warning(f"   • {step_info['step']}: {step_info['failure_rate']}", module='performance')

# Decorador para tracking automático de funciones
def track_performance(tracker: PerformanceTracker, metric_name: Optional[str] = None):
    """
    Decorador que trackea automáticamente el performance de una función
    
    Args:
        tracker: Instancia del PerformanceTracker
        metric_name: Nombre personalizado para la métrica
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            name = metric_name or f"{func.__module__}.{func.__name__}" if hasattr(func, '__module__') else func.__name__
            
            with tracker.track(name):
                return func(*args, **kwargs)
        
        return wrapper
    return decorator

# Función de conveniencia
def create_performance_tracker(logger=None) -> PerformanceTracker:
    """
    Crea una instancia del tracker de performance
    
    Args:
        logger: Instancia del AutomationLogger
        
    Returns:
        PerformanceTracker configurado
    """
    return PerformanceTracker(logger) 