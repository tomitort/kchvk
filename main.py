#!/usr/bin/env python3
"""
Self-Deploy CI/CD - Автоматическая генерация CI/CD конфигураций
Система анализирует Git-репозиторий и генерирует готовые конфигурации для Jenkins или GitLab CI
"""

import argparse
import sys
import os
from pathlib import Path

# Добавляем путь к src для импорта модулей
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.analyzers import RepositoryAnalyzer
from src.generators import JenkinsGenerator, GitLabGenerator
from src.utils.reporting import (
    print_summary,
    print_error_summary,
    print_success_message,
    print_technology_detection,
    print_configuration_preview
)


def parse_arguments():
    """Парсит аргументы командной строки"""
    parser = argparse.ArgumentParser(
        description="Self-Deploy CI/CD - Автоматическая генерация CI/CD конфигураций",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python main.py --repo https://github.com/user/java-project --system jenkins
  python main.py --repo https://gitlab.com/user/python-app --system gitlab --output ./ci-config
  python main.py --repo git@github.com:user/go-service.git --system jenkins --verbose
        """
    )
    
    parser.add_argument(
        '--repo', 
        required=True,
        help='URL Git-репозитория для анализа'
    )
    
    parser.add_argument(
        '--system',
        choices=['jenkins', 'gitlab', 'both'],
        default='jenkins',
        help='CI/CD система (по умолчанию: jenkins)'
    )
    
    parser.add_argument(
        '--output', 
        default='./output',
        help='Директория для сохранения конфигурации (по умолчанию: ./output)'
    )
    
    parser.add_argument(
        '--verbose', 
        action='store_true',
        help='Подробный вывод'
    )
    
    return parser.parse_args()


def validate_arguments(args):
    """Валидирует аргументы командной строки"""
    from src.utils.git_utils import validate_git_url
    
    if not validate_git_url(args.repo):
        raise ValueError(f"Некорректный URL Git-репозитория: {args.repo}")
    
    # Создаем выходную директорию если не существует
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    return True


def get_generators(system: str):
    """Возвращает соответствующие генераторы для выбранной CI/CD системы"""
    if system == 'jenkins':
        return [JenkinsGenerator()]
    elif system == 'gitlab':
        return [GitLabGenerator()]
    elif system == 'both':
        return [JenkinsGenerator(), GitLabGenerator()]
    else:
        raise ValueError(f"Неподдерживаемая CI/CD система: {system}")


def main():
    """Основная функция приложения"""
    args = parse_arguments()
    
    try:
        # Выводим приветственное сообщение
        print("\n🚀 Self-Deploy CI/CD - Автоматическая генерация CI/CD конфигураций")
        print("📋 Поддерживаемые технологии: Java, Go, JavaScript/TypeScript, Python")
        
        if args.verbose:
            print(f"\n🔧 ПАРАМЕТРЫ ЗАПУСКА:")
            print(f"   Репозиторий: {args.repo}")
            print(f"   CI/CD система: {args.system}")
            print(f"   Выходная директория: {args.output}")
            print(f"   Подробный режим: {'Да' if args.verbose else 'Нет'}")
        
        # Валидируем аргументы
        validate_arguments(args)
        
        # Создаем анализатор и генераторы
        analyzer = RepositoryAnalyzer()
        generators = get_generators(args.system)
        
        print(f"\n🚀 ЗАПУСК АНАЛИЗА РЕПОЗИТОРИЯ...")
        
        # Анализируем проект
        analysis = analyzer.analyze_project(args.repo)
        
        if args.verbose:
            print(f"✅ АНАЛИЗ ЗАВЕРШЕН:")
            print(f"   Язык: {analysis.language}")
            print(f"   Фреймворк: {analysis.framework}")
            print(f"   Версия: {analysis.version}")
            print(f"   Инструмент сборки: {analysis.build_tool}")
            print(f"   Зависимости: {len(analysis.dependencies)}")
        
        # Генерируем конфигурации для всех выбранных систем
        output_files = []
        configs = []
        
        for generator in generators:
            print(f"\n🚀 ГЕНЕРАЦИЯ {generator.system_name.upper()} КОНФИГУРАЦИИ...")
            
            output_filename = generator.get_output_filename(analysis)
            output_path = str(Path(args.output) / output_filename)
            
            config = generator.generate(analysis, output_path)
            configs.append(config)
            output_files.append(output_path)
            
            # Валидируем сгенерированную конфигурацию
            if generator.validate(config.config_content):
                print(f"✅ {generator.system_name.upper()} КОНФИГУРАЦИЯ УСПЕШНО ВАЛИДИРОВАНА")
            else:
                print(f"⚠️  ПРЕДУПРЕЖДЕНИЕ: {generator.system_name.upper()} конфигурация может содержать синтаксические ошибки")
        
        # Выводим сводку для первой конфигурации
        if configs:
            print_summary(analysis, configs[0].config_content, output_files[0])
        
        # Выводим успешное сообщение
        print_success_message(output_files)
        
        # Показываем превью первой конфигурации
        if args.verbose and configs:
            print_configuration_preview(configs[0].config_content)
        
    except Exception as e:
        print_error_summary(e, "основной процесс")
        sys.exit(1)


if __name__ == "__main__":
    main()