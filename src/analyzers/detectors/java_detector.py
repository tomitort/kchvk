from pathlib import Path
import xml.etree.ElementTree as ET
from typing import List, Optional
from .base_detector import BaseDetector
from ...analyzers.models import ProjectAnalysis


class JavaDetector(BaseDetector):
    """Детектор для Java/Kotlin проектов"""
    
    @property
    def language_name(self) -> str:
        return "java"
    
    def detect(self, repo_path: Path) -> bool:
        """Определяет, является ли проект Java/Kotlin проектом"""
        # Проверяем наличие конфигурационных файлов Maven или Gradle
        maven_files = self.find_files_by_pattern(repo_path, ["pom.xml"])
        gradle_files = self.find_files_by_pattern(repo_path, ["build.gradle", "build.gradle.kts"])
        java_src = self.find_files_by_pattern(repo_path, ["src/main/java/**/*.java", "src/main/kotlin/**/*.kt"])
        
        return len(maven_files) > 0 or len(gradle_files) > 0 or len(java_src) > 0
    
    def analyze(self, repo_path: Path) -> ProjectAnalysis:
        """Анализирует Java/Kotlin проект"""
        config_files = []
        build_tool = None
        framework = None
        version = None
        dependencies = []
        
        # Проверяем Maven
        pom_files = self.find_files_by_pattern(repo_path, ["pom.xml"])
        if pom_files:
            config_files.extend([str(p) for p in pom_files])
            build_tool = "maven"
            pom_analysis = self._analyze_pom_xml(pom_files[0])
            framework = pom_analysis.get("framework")
            version = pom_analysis.get("version")
            dependencies = pom_analysis.get("dependencies", [])
        
        # Проверяем Gradle
        gradle_files = self.find_files_by_pattern(repo_path, ["build.gradle", "build.gradle.kts"])
        if gradle_files and not build_tool:
            config_files.extend([str(p) for p in gradle_files])
            build_tool = "gradle"
            gradle_analysis = self._analyze_gradle_build(gradle_files[0])
            framework = gradle_analysis.get("framework")
            version = gradle_analysis.get("version")
            dependencies = gradle_analysis.get("dependencies", [])
        
        # Определяем фреймворк по исходному коду если не определили через конфигурацию
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
    
    def _analyze_pom_xml(self, pom_path: Path) -> dict:
        """Анализирует Maven pom.xml файл"""
        result = {
            "framework": None,
            "version": None,
            "dependencies": []
        }
        
        try:
            content = self.read_file_content(pom_path)
            root = ET.fromstring(content)
            
            # Получаем версию из parent или самого проекта
            version_elem = root.find(".//version")
            if version_elem is not None and version_elem.text:
                result["version"] = version_elem.text
            
            # Анализируем зависимости для определения фреймворка
            dependencies_elem = root.find(".//dependencies")
            if dependencies_elem is not None:
                for dep in dependencies_elem.findall(".//dependency"):
                    group_id = dep.find("groupId")
                    artifact_id = dep.find("artifactId")
                    
                    if group_id is not None and artifact_id is not None:
                        dep_name = f"{group_id.text}:{artifact_id.text}"
                        result["dependencies"].append(dep_name)
                        
                        # Определяем фреймворк по зависимостям
                        if not result["framework"]:
                            if "spring-boot" in artifact_id.text:
                                result["framework"] = "spring-boot"
                            elif "micronaut" in group_id.text:
                                result["framework"] = "micronaut"
                            elif "quarkus" in group_id.text:
                                result["framework"] = "quarkus"
            
        except Exception as e:
            print(f"Ошибка анализа pom.xml: {e}")
        
        return result
    
    def _analyze_gradle_build(self, gradle_path: Path) -> dict:
        """Анализирует Gradle build файл"""
        result = {
            "framework": None,
            "version": None,
            "dependencies": []
        }
        
        try:
            content = self.read_file_content(gradle_path)
            lines = content.split('\n')
            
            # Ищем зависимости и плагины
            for line in lines:
                line = line.strip()
                
                # Определяем фреймворк по плагинам
                if "org.springframework.boot" in line:
                    result["framework"] = "spring-boot"
                elif "io.micronaut" in line:
                    result["framework"] = "micronaut"
                elif "io.quarkus" in line:
                    result["framework"] = "quarkus"
                
                # Собираем зависимости
                if "implementation" in line or "compile" in line:
                    # Упрощенное извлечение имени зависимости
                    dep_parts = line.split("'")
                    if len(dep_parts) >= 2:
                        dep_name = dep_parts[1]
                        result["dependencies"].append(dep_name)
            
        except Exception as e:
            print(f"Ошибка анализа Gradle файла: {e}")
        
        return result
    
    def _detect_framework_from_source(self, repo_path: Path) -> Optional[str]:
        """Определяет фреймворк по исходному коду"""
        # Ищем характерные аннотации и импорты
        java_files = self.find_files_by_pattern(repo_path, ["**/*.java"])
        kotlin_files = self.find_files_by_pattern(repo_path, ["**/*.kt"])
        
        all_files = java_files + kotlin_files
        
        for file_path in all_files[:10]:  # Проверяем только первые 10 файлов для производительности
            content = self.read_file_content(file_path)
            
            if "@SpringBootApplication" in content:
                return "spring-boot"
            elif "@MicronautApplication" in content or "io.micronaut" in content:
                return "micronaut"
            elif "@QuarkusMain" in content or "io.quarkus" in content:
                return "quarkus"
            elif "@RestController" in content or "@Controller" in content:
                return "spring-mvc"  # Spring MVC без Boot
        
        return None