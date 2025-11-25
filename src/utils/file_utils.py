import os
import tempfile
from pathlib import Path
from typing import List, Optional


def find_files_by_pattern(directory: str, patterns: List[str]) -> List[Path]:
    """Находит файлы по шаблонам в директории"""
    found_files = []
    path = Path(directory)
    
    for pattern in patterns:
        for file_path in path.rglob(pattern):
            if file_path.is_file():
                found_files.append(file_path)
    
    return found_files


def read_file_safe(file_path: Path) -> Optional[str]:
    """Читает содержимое файла безопасно с обработкой ошибок кодировки"""
    try:
        return file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        try:
            return file_path.read_text(encoding='latin-1')
        except Exception:
            return None
    except Exception:
        return None


def create_temp_directory() -> str:
    """Создает временную директорию"""
    return tempfile.mkdtemp(prefix="self_deploy_")


def ensure_directory_exists(directory: str):
    """Создает директорию если она не существует"""
    Path(directory).mkdir(parents=True, exist_ok=True)


def get_file_extension(file_path: str) -> str:
    """Возвращает расширение файла"""
    return Path(file_path).suffix.lower()


def is_config_file(file_path: str) -> bool:
    """Проверяет, является ли файл конфигурационным"""
    config_extensions = {'.xml', '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.properties'}
    config_filenames = {
        'pom.xml', 'build.gradle', 'build.gradle.kts', 'package.json', 
        'requirements.txt', 'pyproject.toml', 'setup.py', 'go.mod',
        'tsconfig.json', 'webpack.config.js', 'vite.config.js'
    }
    
    path = Path(file_path)
    return path.name in config_filenames or path.suffix in config_extensions


def count_files_by_extension(directory: str, extension: str) -> int:
    """Считает количество файлов с указанным расширением"""
    path = Path(directory)
    pattern = f"**/*{extension}"
    return len(list(path.rglob(pattern)))