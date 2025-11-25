# Детекторы технологий для анализа репозиториев
from .base_detector import BaseDetector
from .java_detector import JavaDetector
from .go_detector import GoDetector
from .js_detector import JSDetector
from .python_detector import PythonDetector

__all__ = ['BaseDetector', 'JavaDetector', 'GoDetector', 'JSDetector', 'PythonDetector']