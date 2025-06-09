#!/usr/bin/env python3
"""
Log Cleaner Utility - Limpieza automática de logs
"""

import os
import gzip
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict

class LogCleaner:
    """Utilidad de limpieza automática de logs"""
    
    def __init__(self, logs_dir: str = "logs"):
        self.logs_dir = Path(logs_dir)
        self.stats = {
            "files_compressed": 0,
            "files_deleted": 0,
            "space_saved_mb": 0,
            "errors": []
        }
    
    def get_directory_stats(self) -> Dict:
        """Obtiene estadísticas del directorio de logs"""
        if not self.logs_dir.exists():
            return {"error": "Directorio de logs no existe"}
        
        total_files = 0
        total_size = 0
        file_types = {}
        
        for file_path in self.logs_dir.rglob("*"):
            if file_path.is_file():
                total_files += 1
                total_size += file_path.stat().st_size
                
                ext = file_path.suffix or "sin_extension"
                file_types[ext] = file_types.get(ext, 0) + 1
        
        return {
            "total_files": total_files,
            "total_size_mb": round(total_size / (1024*1024), 2),
            "file_types": file_types,
            "directory": str(self.logs_dir)
        }
    
    def compress_old_logs(self, days_old: int = 1) -> Dict:
        """Comprime logs antiguos"""
        cutoff_time = datetime.now() - timedelta(days=days_old)
        compressed_count = 0
        space_saved = 0
        
        for log_file in self.logs_dir.rglob("*.log"):
            if log_file.suffix == '.gz':
                continue
                
            try:
                file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
                if file_time < cutoff_time:
                    original_size = log_file.stat().st_size
                    
                    if original_size > 1024:  # Solo comprimir si >1KB
                        compressed_file = log_file.with_suffix(log_file.suffix + '.gz')
                        
                        with open(log_file, 'rb') as f_in:
                            with gzip.open(compressed_file, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                        
                        compressed_size = compressed_file.stat().st_size
                        space_saved += (original_size - compressed_size)
                        
                        log_file.unlink()
                        compressed_count += 1
                        
            except Exception as e:
                self.stats["errors"].append(f"Error: {e}")
        
        self.stats["files_compressed"] = compressed_count
        self.stats["space_saved_mb"] = round(space_saved / (1024*1024), 2)
        
        return {
            "compressed": compressed_count,
            "space_saved_mb": round(space_saved / (1024*1024), 2)
        }


def main():
    """Función principal"""
    cleaner = LogCleaner()
    stats = cleaner.get_directory_stats()
    
    print("📊 Estadísticas del directorio de logs:")
    print(f"   📁 Directorio: {stats.get('directory', 'N/A')}")
    print(f"   📄 Total archivos: {stats.get('total_files', 0)}")
    print(f"   💾 Tamaño total: {stats.get('total_size_mb', 0)} MB")
    print(f"   📋 Tipos de archivo: {stats.get('file_types', {})}")


if __name__ == "__main__":
    main() 