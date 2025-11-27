from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any
import os
from ..analyzers.models import ProjectAnalysis, CICDConfig


class BaseGenerator(ABC):
    """Базовый класс для генераторов CI/CD конфигураций"""
    
    def __init__(self, template_dir: str, system_name: str):
        self.template_dir = template_dir
        self.system_name = system_name
        self.template_engine = None
        self._setup_template_engine()
    
    def _setup_template_engine(self):
        """Настраивает шаблонизатор Jinja2"""
        try:
            from jinja2 import Environment, FileSystemLoader, TemplateNotFound
            self.template_env = Environment(
                loader=FileSystemLoader(self.template_dir),
                trim_blocks=True,
                lstrip_blocks=True
            )
            self.template_engine = self.template_env
        except ImportError:
            raise ImportError("Jinja2 не установлен. Установите его с помощью: pip install jinja2")
    
    @abstractmethod
    def generate(self, analysis: ProjectAnalysis, output_path: str) -> CICDConfig:
        """Генерирует конфигурационный файл"""
        pass
    
    @abstractmethod
    def validate(self, config_content: str) -> bool:
        """Валидирует сгенерированную конфигурацию"""
        pass
    
    def get_template_variables(self, analysis: ProjectAnalysis) -> Dict[str, Any]:
        """Возвращает переменные для шаблона на основе анализа проекта"""
        return {
            "project_name": analysis.repo_name,
            "language": analysis.language,
            "framework": analysis.framework or "unknown",
            "version": analysis.version or "1.0.0",
            "build_tool": analysis.build_tool or "default",
            "dependencies": analysis.dependencies,
            "docker_registry": "registry.example.com",  # Можно настроить через переменные окружения
            "sonar_project_key": analysis.repo_name.replace("/", "_")
        }
    
    def render_template(self, template_name: str, variables: Dict[str, Any]) -> str:
        """Рендерит шаблон с указанными переменными"""
        if not self.template_engine:
            raise RuntimeError("Шаблонизатор не инициализирован")
        
        try:
            template = self.template_engine.get_template(template_name)
            return template.render(**variables)
        except TemplateNotFound:
            raise FileNotFoundError(f"Шаблон {template_name} не найден в {self.template_dir}")
        except Exception as e:
            raise RuntimeError(f"Ошибка рендеринга шаблона {template_name}: {e}")
    
    def save_config(self, config_content: str, output_path: str) -> str:
        """Сохраняет конфигурационный файл"""
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        return output_path
    
    def get_output_filename(self, analysis: ProjectAnalysis) -> str:
        """Возвращает имя выходного файла на основе анализа и системы CI/CD"""
        raise NotImplementedError("Должен быть реализован в подклассах")