from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class ProjectAnalysis:
    """Результат анализа проекта"""
    language: str
    framework: Optional[str]
    version: Optional[str]
    build_tool: Optional[str]
    dependencies: List[str]
    config_files: List[str]
    project_structure: Dict[str, List[str]]
    repo_name: str
    repo_url: str

    def __str__(self) -> str:
        return f"ProjectAnalysis(language={self.language}, framework={self.framework}, version={self.version}, build_tool={self.build_tool})"


@dataclass
class CICDConfig:
    """Конфигурация CI/CD системы"""
    system: str  # 'jenkins' или 'gitlab'
    template_name: str
    variables: Dict[str, str]
    stages: List[str]
    config_content: str

    def __str__(self) -> str:
        return f"CICDConfig(system={self.system}, template={self.template_name}, stages={len(self.stages)})"