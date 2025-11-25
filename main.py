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
    print_welcome_message, 
    print_supported_technologies,
    print_summary,
    print_error_summary,
    generate_analysis_report,
    generate_cicd_report,
    save_report_to_file
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
        choices=['jenkins', 'gitlab'],
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


def get_generator(system: str):
    """Возвращает соответствующий генератор для выбранной CI/CD системы"""
    if system == 'jenkins':
        return JenkinsGenerator()
    elif system == 'gitlab':
        return GitLabGenerator()
    else:
        raise ValueError(f"Неподдерживаемая CI/CD система: {system}")


def main():
    """Основная функция приложения"""
    args = parse_arguments()
    
    try:
        # Выводим приветственное сообщение
        print_welcome_message()
        print_supported_technologies()
        
        if args.verbose:
            print(f"\n🔧 ПАРАМЕТРЫ ЗАПУСКА:")
            print(f"   Репозиторий: {args.repo}")
            print(f"   CI/CD система: {args.system}")
            print(f"   Выходная директория: {args.output}")
            print(f"   Подробный режим: {'Да' if args.verbose else 'Нет'}")
        
        # Валидируем аргументы
        validate_arguments(args)
        
        # Создаем анализатор и генератор
        analyzer = RepositoryAnalyzer()
        generator = get_generator(args.system)
        
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
        
        # Генерируем конфигурацию
        print(f"\n🚀 ГЕНЕРАЦИЯ CI/CD КОНФИГУРАЦИИ...")
        
        output_filename = generator.get_output_filename(analysis)
        output_path = str(Path(args.output) / output_filename)
        
        config = generator.generate(analysis, output_path)
        
        # Валидируем сгенерированную конфигурацию
        if generator.validate(config.config_content):
            print("✅ КОНФИГУРАЦИЯ УСПЕШНО ВАЛИДИРОВАНА")
        else:
            print("⚠️  ПРЕДУПРЕЖДЕНИЕ: Конфигурация может содержать синтаксические ошибки")
        
        # Сохраняем отчеты
        analysis_report = generate_analysis_report(analysis)
        cicd_report = generate_cicd_report(config, output_path)
        
        analysis_report_path = save_report_to_file(analysis_report, args.output, "analysis")
        cicd_report_path = save_report_to_file(cicd_report, args.output, "cicd")
        
        if args.verbose:
            print(f"📊 ОТЧЕТЫ СОХРАНЕНЫ:")
            print(f"   Анализ: {analysis_report_path}")
            print(f"   CI/CD: {cicd_report_path}")
        
        # Выводим сводку
        print_summary(analysis, config, output_path)
        
        print(f"\n🎉 САМОРАЗВЕРТЫВАНИЕ CI/CD УСПЕШНО ЗАВЕРШЕНО!")
        
    except Exception as e:
        print_error_summary(e, "основной процесс")
        sys.exit(1)


if __name__ == "__main__":
    main()