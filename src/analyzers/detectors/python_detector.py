from pathlib import Path
import re
import tomllib
from typing import List, Optional
from .base_detector import BaseDetector
from ...analyzers.models import ProjectAnalysis


class PythonDetector(BaseDetector):
    """Детектор для Python проектов"""
    
    @property
    def language_name(self) -> str:
        return "python"
    
    def detect(self, repo_path: Path) -> bool:
        """Определяет, является ли проект Python проектом"""
        # Проверяем наличие конфигурационных файлов Python
        requirements_files = self.find_files_by_pattern(repo_path, ["requirements.txt"])
        pyproject_files = self.find_files_by_pattern(repo_path, ["pyproject.toml"])
        setup_files = self.find_files_by_pattern(repo_path, ["setup.py"])
        pipfile_files = self.find_files_by_pattern(repo_path, ["Pipfile"])
        python_files = self.find_files_by_pattern(repo_path, ["**/*.py"])
        
        return (len(requirements_files) > 0 or len(pyproject_files) > 0 or 
                len(setup_files) > 0 or len(pipfile_files) > 0 or len(python_files) > 0)
    
    def analyze(self, repo_path: Path) -> ProjectAnalysis:
        """Анализирует Python проект"""
        config_files = []
        build_tool = "pip"
        framework = None
        version = None
        dependencies = []
        
        # Анализируем pyproject.toml (современный стандарт)
        pyproject_files = self.find_files_by_pattern(repo_path, ["pyproject.toml"])
        if pyproject_files:
            config_files.extend([str(p) for p in pyproject_files])
            pyproject_analysis = self._analyze_pyproject_toml(pyproject_files[0])
            version = pyproject_analysis.get("version")
            dependencies = pyproject_analysis.get("dependencies", [])
            framework = pyproject_analysis.get("framework")
            build_tool = pyproject_analysis.get("build_tool", "pip")
        
        # Анализируем requirements.txt
        requirements_files = self.find_files_by_pattern(repo_path, ["requirements.txt"])
        if requirements_files and not dependencies:
            config_files.extend([str(p) for p in requirements_files])
            requirements_analysis = self._analyze_requirements_txt(requirements_files[0])
            dependencies = requirements_analysis.get("dependencies", [])
            if not framework:
                framework = requirements_analysis.get("framework")
        
        # Анализируем setup.py
        setup_files = self.find_files_by_pattern(repo_path, ["setup.py"])
        if setup_files and not version:
            config_files.extend([str(p) for p in setup_files])
            setup_analysis = self._analyze_setup_py(setup_files[0])
            if not version:
                version = setup_analysis.get("version")
            if not dependencies:
                dependencies = setup_analysis.get("dependencies", [])
            if not framework:
                framework = setup_analysis.get("framework")
        
        # Анализируем Pipfile
        pipfile_files = self.find_files_by_pattern(repo_path, ["Pipfile"])
        if pipfile_files and build_tool == "pip":
            config_files.extend([str(p) for p in pipfile_files])
            build_tool = "pipenv"
            pipfile_analysis = self._analyze_pipfile(pipfile_files[0])
            if not version:
                version = pipfile_analysis.get("version")
            if not dependencies:
                dependencies = pipfile_analysis.get("dependencies", [])
            if not framework:
                framework = pipfile_analysis.get("framework")
        
        # Если фреймворк не определен через конфигурационные файлы, определяем по исходному коду
        if not framework:
            framework = self._detect_framework_from_source(repo_path)
        
        # Получаем структуру проекта
        project_structure = self.get_project_structure(repo_path)
        
        return ProjectAnalysis(
            language=self.language_name,
            framework=framework,
            version=version,
            build_tool=build_tool,
            dependencies=dependencies,
            config_files=config_files,
            project_structure=project_structure,
            repo_name="",  # Будет заполнено в analyzer
            repo_url=""    # Будет заполнено в analyzer
        )
    
    def _analyze_pyproject_toml(self, pyproject_path: Path) -> dict:
        """Анализирует pyproject.toml файл"""
        result = {
            "framework": None,
            "version": None,
            "dependencies": [],
            "build_tool": "pip"
        }
        
        try:
            content = self.read_file_content(pyproject_path)
            data = tomllib.loads(content)
            
            # Получаем версию из проекта
            project_section = data.get("project", {})
            result["version"] = project_section.get("version")
            
            # Получаем зависимости
            dependencies = project_section.get("dependencies", [])
            result["dependencies"] = dependencies
            
            # Определяем фреймворк по зависимостям
            for dep in dependencies:
                if not result["framework"]:
                    if "django" in dep:
                        result["framework"] = "django"
                    elif "flask" in dep:
                        result["framework"] = "flask"
                    elif "fastapi" in dep:
                        result["framework"] = "fastapi"
                    elif "starlette" in dep:
                        result["framework"] = "starlette"
            
            # Проверяем build system
            build_system = data.get("build-system", {})
            if "poetry" in str(build_system):
                result["build_tool"] = "poetry"
            elif "flit" in str(build_system):
                result["build_tool"] = "flit"
            
        except Exception as e:
            print(f"Ошибка анализа pyproject.toml: {e}")
        
        return result
    
    def _analyze_requirements_txt(self, requirements_path: Path) -> dict:
        """Анализирует requirements.txt файл"""
        result = {
            "framework": None,
            "dependencies": []
        }
        
        try:
            content = self.read_file_content(requirements_path)
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                # Пропускаем комментарии и пустые строки
                if not line or line.startswith('#'):
                    continue
                
                # Извлекаем имя пакета (убираем версии и другие спецификаторы)
                package_name = line.split('==')[0].split('>=')[0].split('<=')[0].strip()
                if package_name:
                    result["dependencies"].append(package_name)
                    
                    # Определяем фреймворк по зависимостям
                    if not result["framework"]:
                        if package_name == "django":
                            result["framework"] = "django"
                        elif package_name == "flask":
                            result["framework"] = "flask"
                        elif package_name == "fastapi":
                            result["framework"] = "fastapi"
                        elif package_name == "starlette":
                            result["framework"] = "starlette"
            
        except Exception as e:
            print(f"Ошибка анализа requirements.txt: {e}")
        
        return result
    
    def _analyze_setup_py(self, setup_path: Path) -> dict:
        """Анализирует setup.py файл"""
        result = {
            "framework": None,
            "version": None,
            "dependencies": []
        }
        
        try:
            content = self.read_file_content(setup_path)
            
            # Ищем версию с помощью регулярных выражений
            version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
            if version_match:
                result["version"] = version_match.group(1)
            
            # Ищем install_requires
            requires_match = re.search(r'install_requires\s*=\s*\[([^\]]+)\]', content, re.DOTALL)
            if requires_match:
                requires_content = requires_match.group(1)
                # Извлекаем зависимости из списка
                dep_matches = re.findall(r'["\']([^"\']+)["\']', requires_content)
                result["dependencies"] = dep_matches
                
                # Определяем фреймворк по зависимостям
                for dep in dep_matches:
                    if not result["framework"]:
                        if "django" in dep:
                            result["framework"] = "django"
                        elif "flask" in dep:
                            result["framework"] = "flask"
                        elif "fastapi" in dep:
                            result["framework"] = "fastapi"
                        elif "starlette" in dep:
                            result["framework"] = "starlette"
            
        except Exception as e:
            print(f"Ошибка анализа setup.py: {e}")
        
        return result
    
    def _analyze_pipfile(self, pipfile_path: Path) -> dict:
        """Анализирует Pipfile"""
        result = {
            "framework": None,
            "version": None,
            "dependencies": []
        }
        
        try:
            content = self.read_file_content(pipfile_path)
            
            # Упрощенный анализ Pipfile (без полного парсера TOML)
            lines = content.split('\n')
            in_packages = False
            
            for line in lines:
                line = line.strip()
                
                if line.startswith('[packages]'):
                    in_packages = True
                    continue
                elif line.startswith('[') and in_packages:
                    break
                
                if in_packages and '=' in line and not line.startswith('#'):
                    package_name = line.split('=')[0].strip()
                    if package_name:
                        result["dependencies"].append(package_name)
                        
                        # Определяем фреймворк по зависимостям
                        if not result["framework"]:
                            if package_name == "django":
                                result["framework"] = "django"
                            elif package_name == "flask":
                                result["framework"] = "flask"
                            elif package_name == "fastapi":
                                result["framework"] = "fastapi"
                            elif package_name == "starlette":
                                result["framework"] = "starlette"
            
        except Exception as e:
            print(f"Ошибка анализа Pipfile: {e}")
        
        return result
    
    def _detect_framework_from_source(self, repo_path: Path) -> Optional[str]:
        """Определяет фреймворк по исходному коду"""
        python_files = self.find_files_by_pattern(repo_path, ["**/*.py"])
        
        for file_path in python_files[:15]:  # Проверяем только первые 15 файлов для производительности
            content = self.read_file_content(file_path)
            
            # Django - ищем характерные импорты и шаблоны
            if "from django." in content or "import django" in content:
                if "WSGI_APPLICATION" in content or "urlpatterns" in content:
                    return "django"
            
            # Flask - ищем создание приложения Flask
            elif "from flask import Flask" in content or "import Flask" in content:
                if "Flask(__name__)" in content:
                    return "flask"
            
            # FastAPI - ищем создание приложения FastAPI
            elif "from fastapi import FastAPI" in content:
                if "FastAPI()" in content:
                    return "fastapi"
            
            # Starlette - ищем создание приложения Starlette
            elif "from starlette.applications import Starlette" in content:
                if "Starlette()" in content:
                    return "starlette"
            
            # Pyramid - ищем характерные импорты
            elif "from pyramid.config import Configurator" in content:
                return "pyramid"
            
            # Bottle - ищем характерные импорты
            elif "import bottle" in content and "bottle.run(" in content:
                return "bottle"
        
        # Проверяем наличие framework-specific конфигурационных файлов
        if self.find_files_by_pattern(repo_path, ["manage.py"]):
            return "django"
        elif self.find_files_by_pattern(repo_path, ["wsgi.py", "asgi.py"]):
            # Может быть несколько фреймворков, но чаще всего Django или FastAPI
            wsgi_files = self.find_files_by_pattern(repo_path, ["wsgi.py", "asgi.py"])
            for wsgi_file in wsgi_files[:2]:
                wsgi_content = self.read_file_content(wsgi_file)
                if "django" in wsgi_content:
                    return "django"
                elif "fastapi" in wsgi_content:
                    return "fastapi"
        
        return None