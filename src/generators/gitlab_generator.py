import os
from pathlib import Path
from typing import Dict, Any
import yaml
import re
from .base_generator import BaseGenerator
from ..analyzers.models import ProjectAnalysis, CICDConfig


class GitLabGenerator(BaseGenerator):
    """Генератор конфигураций для GitLab CI"""
    
    def __init__(self):
        template_dir = str(Path(__file__).parent.parent / "templates" / "gitlab")
        super().__init__(template_dir)
    
    def generate(self, analysis: ProjectAnalysis, output_path: str) -> CICDConfig:
        """Генерирует .gitlab-ci.yml на основе анализа проекта"""
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
            system="gitlab",
            template_name=template_name,
            variables=variables,
            stages=["build", "test", "code_analysis", "docker_build", "publish", "deploy_staging", "deploy_production"],
            config_content=config_content
        )
        
        return config
    
    def validate(self, config_content: str) -> bool:
        """Валидирует синтаксис .gitlab-ci.yml"""
        try:
            # Проверяем YAML синтаксис
            parsed_yaml = yaml.safe_load(config_content)
            
            # Проверяем обязательные секции
            if not parsed_yaml:
                return False
            
            # Проверяем наличие stages
            if "stages" not in parsed_yaml:
                return False
            
            # Проверяем, что stages - это список
            if not isinstance(parsed_yaml["stages"], list):
                return False
            
            # Проверяем наличие хотя бы одного job
            jobs = [key for key in parsed_yaml.keys() if not key.startswith('.') and key != 'stages' and key != 'variables']
            if len(jobs) == 0:
                return False
            
            # Проверяем, что каждый job имеет stage
            for job_name in jobs:
                job_config = parsed_yaml[job_name]
                if not isinstance(job_config, dict) or "stage" not in job_config:
                    return False
            
            return True
            
        except yaml.YAMLError:
            return False
        except Exception:
            return False
    
    def get_output_filename(self, analysis: ProjectAnalysis) -> str:
        """Возвращает имя выходного файла для GitLab CI"""
        return ".gitlab-ci.yml"
    
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
            raise ValueError(f"Нет шаблона GitLab CI для языка: {analysis.language}")
        
        return template_name
    
    def get_template_variables(self, analysis: ProjectAnalysis) -> Dict[str, Any]:
        """Расширяет базовые переменные для GitLab CI"""
        variables = super().get_template_variables(analysis)
        
        # Добавляем специфичные для GitLab CI переменные
        gitlab_variables = {
            "docker_registry": os.getenv("DOCKER_REGISTRY", "registry.example.com"),
            "nexus_url": os.getenv("NEXUS_URL", "http://nexus:8081"),
            "sonar_url": os.getenv("SONAR_URL", "http://sonarqube:9000"),
            "k8s_namespace": os.getenv("K8S_NAMESPACE", "default"),
            "ci_registry": os.getenv("CI_REGISTRY", "registry.gitlab.com")
        }
        
        variables.update(gitlab_variables)
        return variables