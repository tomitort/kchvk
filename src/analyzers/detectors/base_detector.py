from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List
from ...analyzers.models import ProjectAnalysis


class BaseDetector(ABC):
    """Базовый класс для детекторов технологий"""
    
    @property
    @abstractmethod
    def language_name(self) -> str:
        """Возвращает название языка программирования"""
        pass
    
    @abstractmethod
    def detect(self, repo_path: Path) -> bool:
        """Определяет, подходит ли детектор для проекта"""
        pass
    
    @abstractmethod
    def analyze(self, repo_path: Path) -> ProjectAnalysis:
        """Анализирует проект и возвращает данные"""
        pass
    
    def find_files_by_pattern(self, repo_path: Path, patterns: List[str]) -> List[Path]:
        """Находит файлы по шаблонам в репозитории"""
        found_files = []
        for pattern in patterns:
            for file_path in repo_path.rglob(pattern):
                if file_path.is_file():
                    found_files.append(file_path)
        return found_files
    
    def read_file_content(self, file_path: Path) -> str:
        """Читает содержимое файла безопасно"""
        try:
            return file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            try:
                return file_path.read_text(encoding='latin-1')
            except Exception:
                return ""
        except Exception:
            return ""
    
    def get_project_structure(self, repo_path: Path, max_depth: int = 3) -> Dict[str, List[str]]:
        """Получает структуру проекта до указанной глубины"""
        structure = {}
        
        def scan_directory(current_path: Path, current_depth: int, prefix: str = ""):
            if current_depth > max_depth:
                return
            
            items = []
            for item in current_path.iterdir():
                if item.is_dir():
                    items.append(f"{item.name}/")
                    if current_depth < max_depth:
                        scan_directory(item, current_depth + 1, f"{prefix}  ")
                else:
                    items.append(item.name)
            
            if items:
                structure[prefix + current_path.name] = sorted(items)
        
        scan_directory(repo_path, 0)
        return structure