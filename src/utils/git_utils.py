import os
import tempfile
import shutil
from pathlib import Path
from typing import Optional
import git


def clone_repository(repo_url: str, temp_dir: str) -> str:
    """Клонирует репозиторий во временную директорию"""
    try:
        print(f"Клонирование репозитория: {repo_url}")
        git.Repo.clone_from(repo_url, temp_dir)
        print(f"Репо клонирован в: {temp_dir}")
        return temp_dir
    except git.GitCommandError as e:
        raise Exception(f"Ошибка клонирования репозитория: {e}")
    except Exception as e:
        raise Exception(f"Неожиданная ошибка при клонировании: {e}")


def get_repo_name_from_url(repo_url: str) -> str:
    """Извлекает имя репозитория из URL"""
    # Убираем .git в конце если есть
    if repo_url.endswith('.git'):
        repo_url = repo_url[:-4]
    
    # Извлекаем последнюю часть пути
    return repo_url.split('/')[-1]


def validate_git_url(repo_url: str) -> bool:
    """Проверяет валидность Git URL"""
    # Базовая проверка формата URL
    git_patterns = [
        r'https?://[^\s/$.?#].[^\s]*\.git$',
        r'https?://[^\s/$.?#].[^\s]*$',
        r'git@[^\s/$.?#].[^\s]*\.git$',
        r'git@[^\s/$.?#].[^\s]*:[^\s/$.?#].[^\s]*\.git$'
    ]
    
    import re
    for pattern in git_patterns:
        if re.match(pattern, repo_url):
            return True
    
    return False


def create_temp_repo_dir() -> str:
    """Создает временную директорию для клонирования репозитория"""
    return tempfile.mkdtemp(prefix="self_deploy_")


def cleanup_temp_dir(temp_dir: str):
    """Очищает временную директорию"""
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"Предупреждение: не удалось удалить временную директорию {temp_dir}: {e}")