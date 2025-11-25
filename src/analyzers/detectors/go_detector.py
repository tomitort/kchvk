from pathlib import Path
import re
from typing import List, Optional
from .base_detector import BaseDetector
from ...analyzers.models import ProjectAnalysis


class GoDetector(BaseDetector):
    """Детектор для Go проектов"""
    
    @property
    def language_name(self) -> str:
        return "go"
    
    def detect(self, repo_path: Path) -> bool:
        """Определяет, является ли проект Go проектом"""
        # Проверяем наличие go.mod или go.sum
        go_mod_files = self.find_files_by_pattern(repo_path, ["go.mod"])
        go_sum_files = self.find_files_by_pattern(repo_path, ["go.sum"])
        go_src = self.find_files_by_pattern(repo_path, ["**/*.go"])
        
        return len(go_mod_files) > 0 or len(go_sum_files) > 0 or len(go_src) > 0
    
    def analyze(self, repo_path: Path) -> ProjectAnalysis:
        """Анализирует Go проект"""
        config_files = []
        build_tool = "go"
        framework = None
        version = None
        dependencies = []
        
        # Анализируем go.mod
        go_mod_files = self.find_files_by_pattern(repo_path, ["go.mod"])
        if go_mod_files:
            config_files.extend([str(p) for p in go_mod_files])
            go_mod_analysis = self._analyze_go_mod(go_mod_files[0])
            version = go_mod_analysis.get("version")
            dependencies = go_mod_analysis.get("dependencies", [])
            framework = go_mod_analysis.get("framework")
        
        # Анализируем go.sum
        go_sum_files = self.find_files_by_pattern(repo_path, ["go.sum"])
        if go_sum_files:
            config_files.extend([str(p) for p in go_sum_files])
        
        # Если фреймворк не определен через go.mod, определяем по исходному коду
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
    
    def _analyze_go_mod(self, go_mod_path: Path) -> dict:
        """Анализирует go.mod файл"""
        result = {
            "framework": None,
            "version": None,
            "dependencies": []
        }
        
        try:
            content = self.read_file_content(go_mod_path)
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                
                # Ищем версию Go
                if line.startswith('go '):
                    result["version"] = line[3:].strip()
                
                # Ищем require блоки для зависимостей
                elif line.startswith('require ('):
                    # Многострочный require
                    in_require = True
                    continue
                elif line.startswith('require') and not line.startswith('require ('):
                    # Однострочный require
                    parts = line.split()
                    if len(parts) >= 2:
                        dep = parts[1]
                        result["dependencies"].append(dep)
                        # Проверяем фреймворки по зависимостям
                        if not result["framework"]:
                            if "github.com/gin-gonic/gin" in dep:
                                result["framework"] = "gin"
                            elif "github.com/labstack/echo" in dep:
                                result["framework"] = "echo"
                            elif "github.com/gofiber/fiber" in dep:
                                result["framework"] = "fiber"
                            elif "github.com/gorilla/mux" in dep:
                                result["framework"] = "gorilla-mux"
                
                # Обрабатываем многострочный require
                elif line.startswith(')') and 'in_require' in locals():
                    in_require = False
                elif 'in_require' in locals() and in_require and line:
                    parts = line.split()
                    if parts:
                        dep = parts[0]
                        result["dependencies"].append(dep)
                        # Проверяем фреймворки по зависимостям
                        if not result["framework"]:
                            if "github.com/gin-gonic/gin" in dep:
                                result["framework"] = "gin"
                            elif "github.com/labstack/echo" in dep:
                                result["framework"] = "echo"
                            elif "github.com/gofiber/fiber" in dep:
                                result["framework"] = "fiber"
                            elif "github.com/gorilla/mux" in dep:
                                result["framework"] = "gorilla-mux"
            
        except Exception as e:
            print(f"Ошибка анализа go.mod: {e}")
        
        return result
    
    def _detect_framework_from_source(self, repo_path: Path) -> Optional[str]:
        """Определяет фреймворк по исходному коду"""
        go_files = self.find_files_by_pattern(repo_path, ["**/*.go"])
        
        for file_path in go_files[:10]:  # Проверяем только первые 10 файлов для производительности
            content = self.read_file_content(file_path)
            
            # Ищем импорты и использование фреймворков
            if "github.com/gin-gonic/gin" in content and "gin.Default()" in content:
                return "gin"
            elif "github.com/labstack/echo" in content and "echo.New()" in content:
                return "echo"
            elif "github.com/gofiber/fiber" in content and "fiber.New()" in content:
                return "fiber"
            elif "github.com/gorilla/mux" in content and "mux.NewRouter()" in content:
                return "gorilla-mux"
            elif "net/http" in content and "http.HandleFunc" in content:
                return "net-http"  # Стандартная библиотека
        
        return None