# Многоэтапный Dockerfile для Self-Deploy CI/CD
FROM python:3.9-slim as builder

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Создание виртуального окружения
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копирование и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Финальный образ
FROM python:3.9-slim

# Метаданные образа
LABEL maintainer="Self-Deploy CI/CD Team"
LABEL version="1.0.0"
LABEL description="Автоматическая генерация CI/CD конфигураций для Jenkins и GitLab CI"

# Установка системных зависимостей для работы с Git
RUN apt-get update && apt-get install -y \
    git \
    openssh-client \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Копирование виртуального окружения из builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Создание пользователя приложения
RUN useradd --create-home --shell /bin/bash app
USER app
WORKDIR /home/app

# Копирование исходного кода
COPY --chown=app:app . .

# Создание директорий для работы
RUN mkdir -p output temp

# Переменные окружения
ENV PYTHONPATH=/home/app/src
ENV PYTHONUNBUFFERED=1
ENV TEMP_DIR=/home/app/temp

# Точка входа
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]