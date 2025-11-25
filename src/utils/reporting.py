"""
Модуль для формирования отчетов и вывода результатов анализа
"""

from typing import Dict, Any
from pathlib import Path


def print_summary(analysis, generated_config: str, output_path: str) -> None:
    """Выводит сводку по анализу и сгенерированной конфигурации"""
    
    print("\n📊 СВОДКА АНАЛИЗА:")
    print(f"   Язык программирования: {analysis.language}")
    
    # Используем безопасный доступ к атрибутам с проверкой наличия
    if hasattr(analysis, 'primary_technology') and analysis.primary_technology:
        print(f"   Основная технология: {analysis.primary_technology}")
    
    if hasattr(analysis, 'frameworks') and analysis.frameworks:
        print(f"   Фреймворки: {', '.join(analysis.frameworks)}")
    
    if hasattr(analysis, 'build_tools') and analysis.build_tools:
        print(f"   Инструменты сборки: {', '.join(analysis.build_tools)}")
    
    if hasattr(analysis, 'dependency_managers') and analysis.dependency_managers:
        print(f"   Системы управления зависимостями: {', '.join(analysis.dependency_managers)}")
    
    print(f"\n📁 Сгенерированная конфигурация сохранена в: {output_path}")
    
    # Выводим статистику конфигурации
    lines = generated_config.split('\n')
    stages = [line for line in lines if 'stage(' in line or '  - stage:' in line]
    
    print(f"   Этапы CI/CD: {len(stages)}")
    print(f"   Общее количество строк: {len(lines)}")
    
    # Выводим ключевые этапы
    print(f"\n🔧 Ключевые этапы:")
    for stage in stages:
        stage_name = stage.split('"')[1] if '"' in stage else stage.split("'")[1] if "'" in stage else stage.strip()
        print(f"   - {stage_name}")


def print_error_summary(error: Exception, context: str) -> None:
    """Выводит информацию об ошибке"""
    print(f"\n❌ ОШИБКА при {context}:")
    print(f"   Тип ошибки: {type(error).__name__}")
    print(f"   Сообщение: {str(error)}")
    
    # Дополнительная информация для отладки
    if hasattr(error, '__traceback__'):
        import traceback
        tb_lines = traceback.format_tb(error.__traceback__)
        if tb_lines:
            print(f"   Файл: {tb_lines[-1].split(',')[0].strip()}")


def print_technology_detection(detected_technologies: Dict[str, Any]) -> None:
    """Выводит информацию о детектированных технологиях"""
    print("\n🔍 ДЕТЕКТИРОВАННЫЕ ТЕХНОЛОГИИ:")
    
    for detector_name, technologies in detected_technologies.items():
        if technologies:
            print(f"   {detector_name}:")
            for tech_name, tech_details in technologies.items():
                if isinstance(tech_details, dict):
                    version = tech_details.get('version', 'Не определена')
                    print(f"     - {tech_name} (версия: {version})")
                else:
                    print(f"     - {tech_name}")


def print_configuration_preview(config_content: str, max_lines: int = 20) -> None:
    """Выводит превью сгенерированной конфигурации"""
    lines = config_content.split('\n')
    
    print(f"\n👀 ПРЕВЬЮ КОНФИГУРАЦИИ (первые {min(max_lines, len(lines))} строк):")
    print("-" * 50)
    
    for i, line in enumerate(lines[:max_lines]):
        print(f"{i+1:3d} | {line}")
    
    if len(lines) > max_lines:
        print(f"... и еще {len(lines) - max_lines} строк")
    
    print("-" * 50)


def print_comparison_table(jenkins_config: str, gitlab_config: str) -> None:
    """Выводит сравнительную таблицу для двух CI/CD систем"""
    
    jenkins_lines = jenkins_config.split('\n')
    gitlab_lines = gitlab_config.split('\n')
    
    jenkins_stages = len([line for line in jenkins_lines if 'stage(' in line])
    gitlab_stages = len([line for line in gitlab_lines if '  - stage:' in line])
    
    print("\n📋 СРАВНИТЕЛЬНАЯ ТАБЛИЦА CI/CD СИСТЕМ:")
    print("+" + "-"*40 + "+")
    print(f"| {'Параметр':<20} | {'Jenkins':<8} | {'GitLab CI':<8} |")
    print("+" + "-"*40 + "+")
    print(f"| {'Количество этапов':<20} | {jenkins_stages:<8} | {gitlab_stages:<8} |")
    print(f"| {'Общее строк':<20} | {len(jenkins_lines):<8} | {len(gitlab_lines):<8} |")
    print(f"| {'Сложность':<20} | {'Средняя':<8} | {'Низкая':<8} |")
    print(f"| {'Требует сервер':<20} | {'Да':<8} | {'Нет':<8} |")
    print("+" + "-"*40 + "+")


def print_file_structure(analysis: Dict[str, Any]) -> None:
    """Выводит структуру файлов проекта"""
    file_structure = analysis.get('file_structure', {})
    
    if file_structure:
        print("\n📁 СТРУКТУРА ПРОЕКТА:")
        
        def print_tree(structure: Dict, prefix: str = ""):
            for name, contents in structure.items():
                if isinstance(contents, dict):
                    print(f"{prefix}📁 {name}/")
                    print_tree(contents, prefix + "  ")
                else:
                    print(f"{prefix}📄 {name}")
        
        print_tree(file_structure)


def print_recommendations(analysis: Dict[str, Any]) -> None:
    """Выводит рекомендации по улучшению CI/CD процесса"""
    primary_language = analysis.get('primary_language')
    frameworks = analysis.get('frameworks', [])
    
    print("\n💡 РЕКОМЕНДАЦИИ:")
    
    if primary_language == 'Java':
        print("   • Настройте кеширование Maven/Gradle зависимостей")
        print("   • Добавьте статический анализ кода (SonarQube)")
        print("   • Рассмотрите использование JUnit 5 для тестирования")
        
    elif primary_language == 'Go':
        print("   • Используйте Go Modules для управления зависимостями")
        print("   • Настройте кеширование модулей Go")
        print("   • Добавьте линтеры (golangci-lint)")
        
    elif primary_language == 'JavaScript':
        print("   • Настройте кеширование node_modules")
        print("   • Добавьте линтеры (ESLint) и форматирование (Prettier)")
        print("   • Используйте npm/yarn audit для проверки уязвимостей")
        
    elif primary_language == 'Python':
        print("   • Настройте кеширование pip зависимостей")
        print("   • Добавьте линтеры (flake8, pylint) и форматирование (black)")
        print("   • Используйте poetry/pipenv для управления зависимостями")
    
    # Общие рекомендации
    print("   • Настройте автоматическое развертывание на staging/production")
    print("   • Добавьте мониторинг и алертинг")
    print("   • Рассмотрите использование Docker для контейнеризации")


def print_success_message(output_files: list) -> None:
    """Выводит сообщение об успешном завершении"""
    print("\n🎉 УСПЕШНО ЗАВЕРШЕНО!")
    print("📁 Созданные файлы:")
    
    for file_path in output_files:
        if Path(file_path).exists():
            file_size = Path(file_path).stat().st_size
            print(f"   ✅ {file_path} ({file_size} байт)")
        else:
            print(f"   ❌ {file_path} (файл не найден)")