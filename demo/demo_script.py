#!/usr/bin/env python3
"""
Демонстрационный скрипт для Self-Deploy CI/CD
Демонстрирует работу системы на всех 4 поддерживаемых языках
"""

import os
import sys
import time
from pathlib import Path

# Добавляем путь к src для импорта модулей
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.analyzers import RepositoryAnalyzer
from src.generators import JenkinsGenerator, GitLabGenerator


def print_header(text):
    """Печатает заголовок раздела"""
    print(f"\n{'='*60}")
    print(f"🎬 {text}")
    print(f"{'='*60}")


def print_success(text):
    """Печатает успешное сообщение"""
    print(f"✅ {text}")


def print_info(text):
    """Печатает информационное сообщение"""
    print(f"ℹ️  {text}")


def demo_java_project():
    """Демонстрация для Java проекта"""
    print_header("ДЕМОНСТРАЦИЯ: Java проект (Spring Boot + Maven)")
    
    project_path = str(Path(__file__).parent.parent / "examples" / "test_java_project")
    
    if not os.path.exists(project_path):
        print("❌ Java проект не найден")
        return
    
    print_info(f"Анализ проекта: {project_path}")
    
    try:
        analyzer = RepositoryAnalyzer()
        
        # Анализ локального проекта
        start_time = time.time()
        analysis = analyzer.analyze_local_project(project_path)
        analysis_time = time.time() - start_time
        
        print_success(f"Анализ завершен за {analysis_time:.2f} секунд")
        print_info(f"Язык: {analysis.language}")
        print_info(f"Фреймворк: {analysis.framework}")
        print_info(f"Инструмент сборки: {analysis.build_tool}")
        print_info(f"Версия: {analysis.version}")
        print_info(f"Зависимости: {len(analysis.dependencies)}")
        
        # Генерация конфигураций
        jenkins_gen = JenkinsGenerator()
        gitlab_gen = GitLabGenerator()
        
        # Jenkins
        jenkins_config = jenkins_gen.generate(analysis, "./demo_output/java/Jenkinsfile")
        print_success(f"Jenkinsfile сгенерирован: {len(jenkins_config.config_content)} строк")
        
        # GitLab CI
        gitlab_config = gitlab_gen.generate(analysis, "./demo_output/java/.gitlab-ci.yml")
        print_success(f".gitlab-ci.yml сгенерирован: {len(gitlab_config.config_content)} строк")
        
        # Валидация
        if jenkins_gen.validate(jenkins_config.config_content):
            print_success("Jenkinsfile прошел валидацию")
        else:
            print("⚠️  Jenkinsfile содержит возможные ошибки")
            
        if gitlab_gen.validate(gitlab_config.config_content):
            print_success(".gitlab-ci.yml прошел валидацию")
        else:
            print("⚠️  .gitlab-ci.yml содержит возможные ошибки")
            
    except Exception as e:
        print(f"❌ Ошибка при анализе Java проекта: {e}")


def demo_go_project():
    """Демонстрация для Go проекта"""
    print_header("ДЕМОНСТРАЦИЯ: Go проект (Go Modules)")
    
    project_path = str(Path(__file__).parent.parent / "examples" / "test_go_project")
    
    if not os.path.exists(project_path):
        print("❌ Go проект не найден")
        return
    
    print_info(f"Анализ проекта: {project_path}")
    
    try:
        analyzer = RepositoryAnalyzer()
        
        # Анализ локального проекта
        start_time = time.time()
        analysis = analyzer.analyze_local_project(project_path)
        analysis_time = time.time() - start_time
        
        print_success(f"Анализ завершен за {analysis_time:.2f} секунд")
        print_info(f"Язык: {analysis.language}")
        print_info(f"Фреймворк: {analysis.framework}")
        print_info(f"Инструмент сборки: {analysis.build_tool}")
        print_info(f"Версия: {analysis.version}")
        print_info(f"Зависимости: {len(analysis.dependencies)}")
        
        # Генерация конфигураций
        jenkins_gen = JenkinsGenerator()
        gitlab_gen = GitLabGenerator()
        
        # Jenkins
        jenkins_config = jenkins_gen.generate(analysis, "./demo_output/go/Jenkinsfile")
        print_success(f"Jenkinsfile сгенерирован: {len(jenkins_config.config_content)} строк")
        
        # GitLab CI
        gitlab_config = gitlab_gen.generate(analysis, "./demo_output/go/.gitlab-ci.yml")
        print_success(f".gitlab-ci.yml сгенерирован: {len(gitlab_config.config_content)} строк")
        
        # Валидация
        if jenkins_gen.validate(jenkins_config.config_content):
            print_success("Jenkinsfile прошел валидацию")
        else:
            print("⚠️  Jenkinsfile содержит возможные ошибки")
            
        if gitlab_gen.validate(gitlab_config.config_content):
            print_success(".gitlab-ci.yml прошел валидацию")
        else:
            print("⚠️  .gitlab-ci.yml содержит возможные ошибки")
            
    except Exception as e:
        print(f"❌ Ошибка при анализе Go проекта: {e}")


def demo_javascript_project():
    """Демонстрация для JavaScript проекта"""
    print_header("ДЕМОНСТРАЦИЯ: JavaScript проект (Node.js + npm)")
    
    project_path = str(Path(__file__).parent.parent / "examples" / "test_js_project")
    
    if not os.path.exists(project_path):
        print("❌ JavaScript проект не найден")
        return
    
    print_info(f"Анализ проекта: {project_path}")
    
    try:
        analyzer = RepositoryAnalyzer()
        
        # Анализ локального проекта
        start_time = time.time()
        analysis = analyzer.analyze_local_project(project_path)
        analysis_time = time.time() - start_time
        
        print_success(f"Анализ завершен за {analysis_time:.2f} секунд")
        print_info(f"Язык: {analysis.language}")
        print_info(f"Фреймворк: {analysis.framework}")
        print_info(f"Инструмент сборки: {analysis.build_tool}")
        print_info(f"Версия: {analysis.version}")
        print_info(f"Зависимости: {len(analysis.dependencies)}")
        
        # Генерация конфигураций
        jenkins_gen = JenkinsGenerator()
        gitlab_gen = GitLabGenerator()
        
        # Jenkins
        jenkins_config = jenkins_gen.generate(analysis, "./demo_output/javascript/Jenkinsfile")
        print_success(f"Jenkinsfile сгенерирован: {len(jenkins_config.config_content)} строк")
        
        # GitLab CI
        gitlab_config = gitlab_gen.generate(analysis, "./demo_output/javascript/.gitlab-ci.yml")
        print_success(f".gitlab-ci.yml сгенерирован: {len(gitlab_config.config_content)} строк")
        
        # Валидация
        if jenkins_gen.validate(jenkins_config.config_content):
            print_success("Jenkinsfile прошел валидацию")
        else:
            print("⚠️  Jenkinsfile содержит возможные ошибки")
            
        if gitlab_gen.validate(gitlab_config.config_content):
            print_success(".gitlab-ci.yml прошел валидацию")
        else:
            print("⚠️  .gitlab-ci.yml содержит возможные ошибки")
            
    except Exception as e:
        print(f"❌ Ошибка при анализе JavaScript проекта: {e}")


def demo_python_project():
    """Демонстрация для Python проекта"""
    print_header("ДЕМОНСТРАЦИЯ: Python проект (Poetry)")
    
    project_path = str(Path(__file__).parent.parent / "examples" / "test_python_project")
    
    if not os.path.exists(project_path):
        print("❌ Python проект не найден")
        return
    
    print_info(f"Анализ проекта: {project_path}")
    
    try:
        analyzer = RepositoryAnalyzer()
        
        # Анализ локального проекта
        start_time = time.time()
        analysis = analyzer.analyze_local_project(project_path)
        analysis_time = time.time() - start_time
        
        print_success(f"Анализ завершен за {analysis_time:.2f} секунд")
        print_info(f"Язык: {analysis.language}")
        print_info(f"Фреймворк: {analysis.framework}")
        print_info(f"Инструмент сборки: {analysis.build_tool}")
        print_info(f"Версия: {analysis.version}")
        print_info(f"Зависимости: {len(analysis.dependencies)}")
        
        # Генерация конфигураций
        jenkins_gen = JenkinsGenerator()
        gitlab_gen = GitLabGenerator()
        
        # Jenkins
        jenkins_config = jenkins_gen.generate(analysis, "./demo_output/python/Jenkinsfile")
        print_success(f"Jenkinsfile сгенерирован: {len(jenkins_config.config_content)} строк")
        
        # GitLab CI
        gitlab_config = gitlab_gen.generate(analysis, "./demo_output/python/.gitlab-ci.yml")
        print_success(f".gitlab-ci.yml сгенерирован: {len(gitlab_config.config_content)} строк")
        
        # Валидация
        if jenkins_gen.validate(jenkins_config.config_content):
            print_success("Jenkinsfile прошел валидацию")
        else:
            print("⚠️  Jenkinsfile содержит возможные ошибки")
            
        if gitlab_gen.validate(gitlab_config.config_content):
            print_success(".gitlab-ci.yml прошел валидацию")
        else:
            print("⚠️  .gitlab-ci.yml содержит возможные ошибки")
            
    except Exception as e:
        print(f"❌ Ошибка при анализе Python проекта: {e}")


def generate_demo_report():
    """Генерирует итоговый отчет демонстрации"""
    print_header("📊 ИТОГОВЫЙ ОТЧЕТ ДЕМОНСТРАЦИИ")
    
    demo_output = Path("./demo_output")
    
    if not demo_output.exists():
        print("❌ Демонстрационные файлы не найдены")
        return
    
    total_configs = 0
    total_lines = 0
    
    for lang_dir in demo_output.iterdir():
        if lang_dir.is_dir():
            print(f"\n📁 {lang_dir.name.upper()}:")
            for config_file in lang_dir.iterdir():
                if config_file.is_file():
                    with open(config_file, 'r', encoding='utf-8') as f:
                        lines = len(f.readlines())
                    total_configs += 1
                    total_lines += lines
                    print(f"   📄 {config_file.name}: {lines} строк")
    
    print(f"\n📈 СВОДНАЯ СТАТИСТИКА:")
    print(f"   Всего сгенерировано конфигураций: {total_configs}")
    print(f"   Общее количество строк кода: {total_lines}")
    print(f"   Поддерживаемые языки: Java, Go, JavaScript, Python")
    print(f"   CI/CD системы: Jenkins, GitLab CI")
    
    print(f"\n🎯 КЛЮЧЕВЫЕ ВОЗМОЖНОСТИ:")
    print(f"   ✅ Автоматическое определение стека технологий")
    print(f"   ✅ Генерация полнофункциональных CI/CD пайплайнов")
    print(f"   ✅ Поддержка кеширования зависимостей")
    print(f"   ✅ Интеграция с SonarQube для анализа кода")
    print(f"   ✅ Многоэтапная сборка Docker образов")
    print(f"   ✅ Публикация артефактов в Nexus/Docker Registry")
    print(f"   ✅ Автоматическое развертывание на staging/production")


def main():
    """Основная функция демонстрационного скрипта"""
    print_header("🚀 Self-Deploy CI/CD - ДЕМОНСТРАЦИОННЫЙ СКРИПТ")
    print("Демонстрация работы системы на всех 4 поддерживаемых языках")
    
    # Создаем выходную директорию
    demo_output = Path("./demo_output")
    demo_output.mkdir(exist_ok=True)
    
    # Запускаем демонстрации для всех языков
    demo_java_project()
    demo_go_project()
    demo_javascript_project()
    demo_python_project()
    
    # Генерируем итоговый отчет
    generate_demo_report()
    
    print_header("🎉 ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("Все конфигурации сохранены в папке ./demo_output/")
    print("\n📋 СЛЕДУЮЩИЕ ШАГИ:")
    print("   1. Запустите локальную инфраструктуру: docker-compose up -d")
    print("   2. Настройте сгенерированные конфигурации в вашей CI/CD системе")
    print("   3. Запустите пайплайны для проверки их работы")
    print("\n📚 ДОКУМЕНТАЦИЯ:")
    print("   - README.md - Основная документация")
    print("   - DOCUMENTATION.md - Подробная документация по языкам")
    print("   - TEST_REPORT.md - Отчет о тестировании")
    print("   - PRESENTATION.md - Презентация проекта")


if __name__ == "__main__":
    main()