#!/usr/bin/env python3
"""
Тестовый скрипт для проверки системы Self-Deploy CI/CD на примерах проектов
"""

import os
import sys
import shutil
from pathlib import Path

# Добавляем путь к src для импорта модулей
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzers import RepositoryAnalyzer
from src.generators import JenkinsGenerator, GitLabGenerator
from src.utils.reporting import print_summary, print_error_summary


def test_java_project():
    """Тестирование Java проекта"""
    print("\n" + "="*50)
    print("🧪 ТЕСТИРОВАНИЕ JAVA ПРОЕКТА")
    print("="*50)
    
    try:
        # Используем локальный путь к примеру проекта
        example_path = Path(__file__).parent / "test_java_project"
        
        # Анализируем проект напрямую без клонирования
        analyzer = RepositoryAnalyzer()
        analysis = analyzer.analyze_local_project(str(example_path))
        
        # Генерируем конфигурации
        jenkins_gen = JenkinsGenerator()
        gitlab_gen = GitLabGenerator()
        
        # Jenkins
        jenkins_output = Path("test_output/java/Jenkinsfile")
        jenkins_output.parent.mkdir(parents=True, exist_ok=True)
        jenkins_config = jenkins_gen.generate(analysis, str(jenkins_output))
        
        # GitLab CI
        gitlab_output = Path("test_output/java/.gitlab-ci.yml")
        gitlab_output.parent.mkdir(parents=True, exist_ok=True)
        gitlab_config = gitlab_gen.generate(analysis, str(gitlab_output))
        
        print("✅ Java проект успешно протестирован")
        print_summary(analysis, jenkins_config.config_content, str(jenkins_output))
        
        return True
        
    except Exception as e:
        print_error_summary(e, "тестирование Java проекта")
        return False


def test_go_project():
    """Тестирование Go проекта"""
    print("\n" + "="*50)
    print("🧪 ТЕСТИРОВАНИЕ GO ПРОЕКТА")
    print("="*50)
    
    try:
        # Используем локальный путь к примеру проекта
        example_path = Path(__file__).parent / "test_go_project"
        
        # Анализируем проект напрямую без клонирования
        analyzer = RepositoryAnalyzer()
        analysis = analyzer.analyze_local_project(str(example_path))
        
        # Генерируем конфигурации
        jenkins_gen = JenkinsGenerator()
        gitlab_gen = GitLabGenerator()
        
        # Jenkins
        jenkins_output = Path("test_output/go/Jenkinsfile")
        jenkins_output.parent.mkdir(parents=True, exist_ok=True)
        jenkins_config = jenkins_gen.generate(analysis, str(jenkins_output))
        
        # GitLab CI
        gitlab_output = Path("test_output/go/.gitlab-ci.yml")
        gitlab_output.parent.mkdir(parents=True, exist_ok=True)
        gitlab_config = gitlab_gen.generate(analysis, str(gitlab_output))
        
        print("✅ Go проект успешно протестирован")
        print_summary(analysis, jenkins_config.config_content, str(jenkins_output))
        
        return True
        
    except Exception as e:
        print_error_summary(e, "тестирование Go проекта")
        return False


def test_js_project():
    """Тестирование JavaScript проекта"""
    print("\n" + "="*50)
    print("🧪 ТЕСТИРОВАНИЕ JAVASCRIPT ПРОЕКТА")
    print("="*50)
    
    try:
        # Используем локальный путь к примеру проекта
        example_path = Path(__file__).parent / "test_js_project"
        
        # Анализируем проект напрямую без клонирования
        analyzer = RepositoryAnalyzer()
        analysis = analyzer.analyze_local_project(str(example_path))
        
        # Генерируем конфигурации
        jenkins_gen = JenkinsGenerator()
        gitlab_gen = GitLabGenerator()
        
        # Jenkins
        jenkins_output = Path("test_output/js/Jenkinsfile")
        jenkins_output.parent.mkdir(parents=True, exist_ok=True)
        jenkins_config = jenkins_gen.generate(analysis, str(jenkins_output))
        
        # GitLab CI
        gitlab_output = Path("test_output/js/.gitlab-ci.yml")
        gitlab_output.parent.mkdir(parents=True, exist_ok=True)
        gitlab_config = gitlab_gen.generate(analysis, str(gitlab_output))
        
        print("✅ JavaScript проект успешно протестирован")
        print_summary(analysis, jenkins_config.config_content, str(jenkins_output))
        
        return True
        
    except Exception as e:
        print_error_summary(e, "тестирование JavaScript проекта")
        return False


def test_python_project():
    """Тестирование Python проекта"""
    print("\n" + "="*50)
    print("🧪 ТЕСТИРОВАНИЕ PYTHON ПРОЕКТА")
    print("="*50)
    
    try:
        # Используем локальный путь к примеру проекта
        example_path = Path(__file__).parent / "test_python_project"
        
        # Анализируем проект напрямую без клонирования
        analyzer = RepositoryAnalyzer()
        analysis = analyzer.analyze_local_project(str(example_path))
        
        # Генерируем конфигурации
        jenkins_gen = JenkinsGenerator()
        gitlab_gen = GitLabGenerator()
        
        # Jenkins
        jenkins_output = Path("test_output/python/Jenkinsfile")
        jenkins_output.parent.mkdir(parents=True, exist_ok=True)
        jenkins_config = jenkins_gen.generate(analysis, str(jenkins_output))
        
        # GitLab CI
        gitlab_output = Path("test_output/python/.gitlab-ci.yml")
        gitlab_output.parent.mkdir(parents=True, exist_ok=True)
        gitlab_config = gitlab_gen.generate(analysis, str(gitlab_output))
        
        print("✅ Python проект успешно протестирован")
        print_summary(analysis, jenkins_config.config_content, str(jenkins_output))
        
        return True
        
    except Exception as e:
        print_error_summary(e, "тестирование Python проекта")
        return False


def run_all_tests():
    """Запускает все тесты"""
    print("🚀 ЗАПУСК ТЕСТИРОВАНИЯ SELF-DEPLOY CI/CD")
    print("="*60)
    
    # Создаем выходную директорию
    output_dir = Path("test_output")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    
    test_results = {}
    
    # Запускаем тесты для всех языков
    test_results["java"] = test_java_project()
    test_results["go"] = test_go_project()
    test_results["javascript"] = test_js_project()
    test_results["python"] = test_python_project()
    
    # Выводим сводку
    print("\n" + "="*60)
    print("📊 СВОДКА ТЕСТИРОВАНИЯ")
    print("="*60)
    
    passed = sum(test_results.values())
    total = len(test_results)
    
    for language, result in test_results.items():
        status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
        print(f"   {language.capitalize():<12} : {status}")
    
    print(f"\n   ИТОГО: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("\n🎉 ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ!")
        print("📁 Сгенерированные конфигурации сохранены в: test_output/")
        return True
    else:
        print(f"\n⚠️  {total - passed} тестов не пройдено")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)