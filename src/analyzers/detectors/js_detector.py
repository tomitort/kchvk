from pathlib import Path
import json
import re
from typing import List, Optional
from .base_detector import BaseDetector
from ...analyzers.models import ProjectAnalysis


class JSDetector(BaseDetector):
    """Детектор для JavaScript/TypeScript проектов"""
    
    @property
    def language_name(self) -> str:
        return "javascript"
    
    def detect(self, repo_path: Path) -> bool:
        """Определяет, является ли проект JavaScript/TypeScript проектом"""
        # Проверяем наличие package.json
        package_json_files = self.find_files_by_pattern(repo_path, ["package.json"])
        js_files = self.find_files_by_pattern(repo_path, ["**/*.js", "**/*.jsx", "**/*.ts", "**/*.tsx"])
        
        return len(package_json_files) > 0 or len(js_files) > 0
    
    def analyze(self, repo_path: Path) -> ProjectAnalysis:
        """Анализирует JavaScript/TypeScript проект"""
        config_files = []
        build_tool = "npm"
        framework = None
        version = None
        dependencies = []
        
        # Анализируем package.json
        package_json_files = self.find_files_by_pattern(repo_path, ["package.json"])
        if package_json_files:
            config_files.extend([str(p) for p in package_json_files])
            package_analysis = self._analyze_package_json(package_json_files[0])
            version = package_analysis.get("version")
            dependencies = package_analysis.get("dependencies", [])
            framework = package_analysis.get("framework")
            build_tool = package_analysis.get("build_tool", "npm")
        
        # Проверяем TypeScript
        tsconfig_files = self.find_files_by_pattern(repo_path, ["tsconfig.json"])
        if tsconfig_files:
            config_files.extend([str(p) for p in tsconfig_files])
        
        # Проверяем конфигурации сборщиков
        webpack_files = self.find_files_by_pattern(repo_path, ["webpack.config.js", "webpack.config.ts"])
        vite_files = self.find_files_by_pattern(repo_path, ["vite.config.js", "vite.config.ts"])
        if webpack_files:
            config_files.extend([str(p) for p in webpack_files])
        if vite_files:
            config_files.extend([str(p) for p in vite_files])
        
        # Если фреймворк не определен через package.json, определяем по исходному коду
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
    
    def _analyze_package_json(self, package_json_path: Path) -> dict:
        """Анализирует package.json файл"""
        result = {
            "framework": None,
            "version": None,
            "dependencies": [],
            "build_tool": "npm"
        }
        
        try:
            content = self.read_file_content(package_json_path)
            package_data = json.loads(content)
            
            # Получаем версию проекта
            result["version"] = package_data.get("version")
            
            # Собираем все зависимости
            all_deps = {}
            all_deps.update(package_data.get("dependencies", {}))
            all_deps.update(package_data.get("devDependencies", {}))
            all_deps.update(package_data.get("peerDependencies", {}))
            
            result["dependencies"] = list(all_deps.keys())
            
            # Определяем фреймворк по зависимостям
            dependencies_list = list(all_deps.keys())
            for dep in dependencies_list:
                if not result["framework"]:
                    if dep == "react":
                        result["framework"] = "react"
                    elif dep == "vue":
                        result["framework"] = "vue"
                    elif dep == "@angular/core":
                        result["framework"] = "angular"
                    elif dep == "express":
                        result["framework"] = "express"
                    elif dep == "koa":
                        result["framework"] = "koa"
                    elif dep == "next":
                        result["framework"] = "nextjs"
                    elif dep == "nuxt":
                        result["framework"] = "nuxtjs"
                    elif dep == "svelte":
                        result["framework"] = "svelte"
            
            # Определяем сборщик по скриптам и зависимостям
            scripts = package_data.get("scripts", {})
            if "yarn" in scripts.get("start", "") or "yarn" in scripts.get("build", ""):
                result["build_tool"] = "yarn"
            elif "pnpm" in scripts.get("start", "") or "pnpm" in scripts.get("build", ""):
                result["build_tool"] = "pnpm"
            elif "yarn" in dependencies_list:
                result["build_tool"] = "yarn"
            elif "pnpm" in dependencies_list:
                result["build_tool"] = "pnpm"
            
        except Exception as e:
            print(f"Ошибка анализа package.json: {e}")
        
        return result
    
    def _detect_framework_from_source(self, repo_path: Path) -> Optional[str]:
        """Определяет фреймворк по исходному коду"""
        # Ищем файлы с характерными импортами и шаблонами
        js_files = self.find_files_by_pattern(repo_path, ["**/*.js", "**/*.jsx", "**/*.ts", "**/*.tsx"])
        
        for file_path in js_files[:15]:  # Проверяем только первые 15 файлов для производительности
            content = self.read_file_content(file_path)
            
            # React - ищем JSX и импорты React
            if ("import React" in content or "from 'react'" in content) and ("<div>" in content or "React.createElement" in content):
                return "react"
            
            # Vue - ищем Vue импорты и шаблоны
            elif "import Vue" in content or "from 'vue'" in content or "Vue.component" in content:
                return "vue"
            
            # Angular - ищем декораторы Angular
            elif "@Component" in content or "@NgModule" in content or "from '@angular/core'" in content:
                return "angular"
            
            # Express - ищем использование express()
            elif "const express = require('express')" in content or "import express from 'express'" in content:
                if "express()" in content or "app.get" in content or "app.post" in content:
                    return "express"
            
            # Koa - ищем использование Koa
            elif "const Koa = require('koa')" in content or "import Koa from 'koa'" in content:
                if "new Koa()" in content:
                    return "koa"
            
            # Next.js - ищем характерные функции
            elif "getServerSideProps" in content or "getStaticProps" in content or "next/head" in content:
                return "nextjs"
            
            # Nuxt.js - ищем характерные функции
            elif "asyncData" in content or "fetch" in content or "nuxt/" in content:
                return "nuxtjs"
            
            # Svelte - ищем характерные шаблоны
            elif "<script context=" in content or "svelte" in file_path.name:
                return "svelte"
        
        # Проверяем наличие framework-specific конфигурационных файлов
        if self.find_files_by_pattern(repo_path, ["next.config.js", "next.config.ts"]):
            return "nextjs"
        elif self.find_files_by_pattern(repo_path, ["nuxt.config.js", "nuxt.config.ts"]):
            return "nuxtjs"
        elif self.find_files_by_pattern(repo_path, ["svelte.config.js"]):
            return "svelte"
        elif self.find_files_by_pattern(repo_path, ["angular.json"]):
            return "angular"
        elif self.find_files_by_pattern(repo_path, ["vue.config.js"]):
            return "vue"
        
        return None