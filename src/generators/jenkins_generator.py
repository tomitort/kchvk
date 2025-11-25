import os
from pathlib import Path
from typing import Dict, Any
import re
from .base_generator import BaseGenerator
from ..analyzers.models import ProjectAnalysis, CICDConfig


class JenkinsGenerator(BaseGenerator):
    """Генератор конфигураций для Jenkins"""
    
    def __init__(self):
        template_dir = str(Path(__file__).parent.parent / "templates" / "jenkins")
        super().__init__(template_dir)
    
    def generate(self, analysis: ProjectAnalysis, output_path: str) -> CICDConfig:
        """Генерирует Jenkinsfile на основе анализа проекта"""
        # Определяем имя шаблона на основе языка
        template_name = self._get_template_name(analysis)
        
        # Получаем переменные для шаблона
        variables = self.get_template_variables(analysis)
        
        # Рендерим шаблон
        config_content = self.render_template(template_name, variables)
        
        # Сохраняем конфигурационный файл
        final_output_path = self.save_config(config_content, output_path)
        
        # Создаем объект конфигурации
        config = CICDConfig(
            system="jenkins",
            template_name=template_name,
            variables=variables,
            stages=["build", "test", "code_analysis", "docker_build", "publish", "deploy_staging", "deploy_production"],
            config_content=config_content
        )
        
        return config
    
    def validate(self, config_content: str) -> bool:
        """Валидирует синтаксис Jenkinsfile"""
        # Базовая проверка структуры Jenkinsfile
        required_patterns = [
            r"pipeline\s*{",
            r"agent\s+\w+",
            r"stages\s*{",
            r"stage\s*\(['\"]\w+['\"]\)"
        ]
        
        for pattern in required_patterns:
            if not re.search(pattern, config_content, re.MULTILINE | re.DOTALL):
                return False
        
        return True
    
    def get_output_filename(self, analysis: ProjectAnalysis) -> str:
        """Возвращает имя выходного файла для Jenkins"""
        return "Jenkinsfile"
    
    def _get_template_name(self, analysis: ProjectAnalysis) -> str:
        """Определяет имя шаблона на основе языка проекта"""
        language_to_template = {
            "java": "java.j2",
            "go": "go.j2", 
            "javascript": "javascript.j2",
            "python": "python.j2"
        }
        
        template_name = language_to_template.get(analysis.language)
        if not template_name:
            raise ValueError(f"Нет шаблона Jenkins для языка: {analysis.language}")
        
        return template_name
    
    def get_template_variables(self, analysis: ProjectAnalysis) -> Dict[str, Any]:
        """Расширяет базовые переменные для Jenkins"""
        variables = super().get_template_variables(analysis)
        
        # Добавляем специфичные для Jenkins переменные
        jenkins_variables = {
            "docker_registry": os.getenv("DOCKER_REGISTRY", "registry.example.com"),
            "nexus_url": os.getenv("NEXUS_URL", "http://nexus:8081"),
            "sonar_url": os.getenv("SONAR_URL", "http://sonarqube:9000"),
            "k8s_namespace": os.getenv("K8S_NAMESPACE", "default")
        }
        
        variables.update(jenkins_variables)
        return variables