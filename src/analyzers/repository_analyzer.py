import os
import tempfile
import shutil
from pathlib import Path
from typing import Optional, List
import git
from .models import ProjectAnalysis
from .detectors.java_detector import JavaDetector
from .detectors.go_detector import GoDetector
from .detectors.js_detector import JSDetector
from .detectors.python_detector import PythonDetector


class RepositoryAnalyzer:
    """Анализатор Git-репозитория для определения стека технологий"""
    
    def __init__(self):
        self.detectors = [
            PythonDetector(),  # Python первый для приоритета над JS в смешанных проектах
            JavaDetector(),
            GoDetector(),
            JSDetector()
        ]
        self.temp_dirs = []
    
    def clone_repository(self, repo_url: str) -> str:
        """Клонирует репозиторий во временную директорию"""
        try:
            temp_dir = tempfile.mkdtemp(prefix="self_deploy_")
            self.temp_dirs.append(temp_dir)
            
            print(f"Клонирование репозитория: {repo_url}")
            # Используем shallow clone для экономии места (только последний коммит)
            # Добавляем single-branch для еще большей экономии места
            git.Repo.clone_from(repo_url, temp_dir, depth=1, single_branch=True)
            print(f"Репо клонирован в: {temp_dir}")
            
            return temp_dir
        except git.GitCommandError as e:
            # Очистка при ошибке клонирования
            self.cleanup_temp_dirs()
            raise Exception(f"Ошибка клонирования репозитория: {e}")
        except Exception as e:
            # Очистка при любой другой ошибке
            self.cleanup_temp_dirs()
            raise Exception(f"Неожиданная ошибка при клонировании: {e}")
    
    def analyze_project(self, repo_url: str) -> ProjectAnalysis:
        """Анализирует проект и возвращает результат анализа"""
        repo_path_str = self.clone_repository(repo_url)
        repo_path = Path(repo_path_str)
        
        try:
            # Определяем основной язык и технологии
            detected_language = self.detect_technology(repo_path)
            
            # Запускаем соответствующий детектор для детального анализа
            analysis = None
            for detector in self.detectors:
                if detector.detect(repo_path):
                    analysis = detector.analyze(repo_path)
                    break
            
            if analysis is None:
                raise Exception("Не удалось определить стек технологий проекта")
            
            # Добавляем информацию о репозитории
            analysis.repo_url = repo_url
            analysis.repo_name = self._get_repo_name_from_url(repo_url)
            
            return analysis
            
        finally:
            # Очищаем временные файлы
            self.cleanup_temp_dirs()
    
    def detect_technology(self, repo_path: Path) -> str:
        """Определяет основной язык программирования проекта"""
        for detector in self.detectors:
            if detector.detect(repo_path):
                return detector.language_name
        
        raise Exception("Не удалось определить язык программирования проекта")
    
    def analyze_local_project(self, local_path: str) -> ProjectAnalysis:
        """Анализирует локальный проект без клонирования"""
        repo_path = Path(local_path)
        
        # Определяем основной язык и технологии
        detected_language = self.detect_technology(repo_path)
        
        # Запускаем соответствующий детектор для детального анализа
        analysis = None
        for detector in self.detectors:
            if detector.detect(repo_path):
                analysis = detector.analyze(repo_path)
                break
        
        if analysis is None:
            raise Exception("Не удалось определить стек технологий проекта")
        
        # Добавляем информацию о проекте
        analysis.repo_url = f"file://{local_path}"
        analysis.repo_name = repo_path.name
        
        return analysis
    
    def _get_repo_name_from_url(self, repo_url: str) -> str:
        """Извлекает имя репозитория из URL"""
        # Убираем .git в конце если есть
        if repo_url.endswith('.git'):
            repo_url = repo_url[:-4]
        
        # Извлекаем последнюю часть пути
        return repo_url.split('/')[-1]
    
    def cleanup_temp_dirs(self):
        """Очищает все временные директории"""
        for temp_dir in self.temp_dirs:
            try:
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
            except Exception as e:
                print(f"Предупреждение: не удалось удалить временную директорию {temp_dir}: {e}")
        
        self.temp_dirs = []
    
    def __del__(self):
        """Деструктор для очистки временных файлов"""
        self.cleanup_temp_dirs()