# 🚀 Быстрый старт Self-Deploy CI/CD

Пошаговое руководство по запуску системы Self-Deploy CI/CD

## 📋 Предварительные требования

- **Docker** и **Docker Compose** (рекомендуемый способ)
- ИЛИ **Python 3.8+** и **Git** (нативный способ)

## 🐳 Способ 1: Запуск через Docker (рекомендуется)

### Шаг 1: Клонирование репозитория
```bash
git clone <repository-url>
cd self-deploy-ci-cd
```

### Шаг 2: Сборка Docker образа
```bash
docker build -t self-deploy-ci-cd .
```

### Шаг 3: Базовое использование
```bash
# Просмотр справки
docker run self-deploy-ci-cd --help

# Анализ Java проекта и генерация Jenkins конфигурации
docker run -v $(pwd)/output:/home/app/output self-deploy-ci-cd \
  --repo https://github.com/user/java-project --system jenkins

# Анализ Go проекта и генерация GitLab CI конфигурации
docker run -v $(pwd)/output:/home/app/output self-deploy-ci-cd \
  --repo https://github.com/user/go-project --system gitlab

# Генерация конфигураций для обеих систем
docker run -v $(pwd)/output:/home/app/output self-deploy-ci-cd \
  --repo https://github.com/user/project --system both --verbose
```

### Шаг 4: Демонстрационный режим
```bash
# Запуск демонстрации на тестовых проектах
docker run -v $(pwd)/demo_output:/home/app/demo_output self-deploy-ci-cd --demo
```

## 🐳 Способ 2: Полный стек с Docker Compose

### Шаг 1: Запуск всей системы
```bash
# Запуск Self-Deploy CI/CD и всей инфраструктуры
docker-compose up -d
```

### Шаг 2: Использование системы
```bash
# Выполнение команды в контейнере
docker-compose run self-deploy-ci-cd --repo https://github.com/user/project --system both

# Или подключение к контейнеру
docker-compose exec self-deploy-ci-cd bash
```

### Шаг 3: Доступ к сервисам инфраструктуры
После запуска будут доступны:
- **Jenkins**: http://localhost:8080
- **GitLab**: http://localhost:8081  
- **SonarQube**: http://localhost:9000
- **Nexus**: http://localhost:8082

## 🐍 Способ 3: Нативная установка (без Docker)

### Шаг 1: Установка зависимостей
```bash
git clone <repository-url>
cd self-deploy-ci-cd
pip install -r requirements.txt
```

### Шаг 2: Базовое использование
```bash
# Просмотр справки
python main.py --help

# Анализ проекта и генерация конфигурации
python main.py --repo https://github.com/user/project --system jenkins

# Подробный режим
python main.py --repo https://github.com/user/project --system both --verbose
```

### Шаг 3: Запуск локальной инфраструктуры (опционально)
```bash
cd infrastructure
docker-compose up -d
```

## 🎯 Примеры использования

### Пример 1: Java проект с Maven
```bash
# Через Docker
docker run -v $(pwd)/output:/home/app/output self-deploy-ci-cd \
  --repo https://github.com/spring-projects/spring-petclinic --system jenkins

# Нативно
python main.py --repo https://github.com/spring-projects/spring-petclinic --system jenkins
```

### Пример 2: React приложение
```bash
# Через Docker
docker run -v $(pwd)/output:/home/app/output self-deploy-ci-cd \
  --repo https://github.com/facebook/react --system gitlab --verbose

# Нативно  
python main.py --repo https://github.com/facebook/react --system gitlab --verbose
```

### Пример 3: Python проект
```bash
# Через Docker
docker run -v $(pwd)/output:/home/app/output self-deploy-ci-cd \
  --repo https://github.com/tiangolo/fastapi --system both

# Нативно
python main.py --repo https://github.com/tiangolo/fastapi --system both
```

## 🔧 Параметры командной строки

| Параметр | Описание | Пример |
|----------|----------|---------|
| `--repo` | URL Git-репозитория | `--repo https://github.com/user/project` |
| `--system` | CI/CD система | `--system jenkins` / `--system gitlab` / `--system both` |
| `--output` | Директория для сохранения | `--output ./my-config` |
| `--verbose` | Подробный вывод | `--verbose` |
| `--demo` | Демонстрационный режим | `--demo` |

## 📁 Структура выходных файлов

После успешного выполнения в указанной директории будут созданы:

```
output/
├── Jenkinsfile          # Конфигурация для Jenkins
├── .gitlab-ci.yml       # Конфигурация для GitLab CI  
├── analysis_report.txt  # Отчет об анализе проекта
└── cicd_report.txt      # Отчет о сгенерированной конфигурации
```

## 🐛 Решение проблем

### Проблема: Ошибка доступа к Docker
```bash
# Добавьте пользователя в группу docker
sudo usermod -aG docker $USER
# Перезапустите сессию терминала
```

### Проблема: Недостаточно прав для записи
```bash
# Создайте директорию output с правильными правами
mkdir -p output
chmod 755 output
```

### Проблема: Ошибка сети
```bash
# Проверьте подключение к интернету
ping github.com

# Если используете прокси, настройте переменные окружения
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
```

## 📞 Получение помощи

### Просмотр справки
```bash
# Основная справка
docker run self-deploy-ci-cd --help

# Или
python main.py --help
```

### Документация
- **README.md** - Основная документация
- **DOCUMENTATION.md** - Подробное описание системы
- **TEST_REPORT.md** - Отчет о тестировании
- **PRESENTATION.md** - Презентация проекта

### Демонстрация
```bash
# Запуск полной демонстрации
docker run -v $(pwd)/demo_output:/home/app/demo_output self-deploy-ci-cd --demo

# Или
python demo/demo_script.py
```

## ⏱️ Ожидаемое время выполнения

- **Сборка Docker образа**: 2-5 минут
- **Анализ проекта**: 2-5 секунд
- **Генерация конфигурации**: < 1 секунды
- **Полный цикл**: 5-10 секунд

---

**Готово!** Теперь вы можете автоматически генерировать CI/CD конфигурации для ваших проектов. 🎉

# Self-Deploy CI/CD - Автоматическая генерация CI/CD конфигураций

![Self-Deploy CI/CD](https://img.shields.io/badge/Self--Deploy-CI%2FCD-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Self-Deploy CI/CD** - это интеллектуальная система для автоматической генерации полнофункциональных CI/CD конфигураций на основе анализа структуры Git-репозитория. Система определяет стек технологий проекта и генерирует готовые конфигурации для Jenkins или GitLab CI.

## 🚀 Возможности

- **Автоматический анализ** Git-репозитория и определение стека технологий
- **Поддержка 4 основных языков**: Java/Kotlin, Go, JavaScript/TypeScript, Python
- **Генерация конфигураций** для Jenkins (Jenkinsfile) и GitLab CI (.gitlab-ci.yml)
- **Полный цикл CI/CD**: сборка, тестирование, анализ кода, Docker, деплой
- **Локальная инфраструктура** с Docker Compose для тестирования
- **Оптимизация кеширования** зависимостей для ускорения сборок

## 📋 Поддерживаемые технологии

### Java/Kotlin
- **Сборщики**: Maven, Gradle
- **Фреймворки**: Spring Boot, Micronaut, Quarkus
- **Анализ**: pom.xml, build.gradle, исходный код

### Go
- **Менеджер зависимостей**: Go Modules
- **Фреймворки**: Gin, Echo, Fiber, Gorilla Mux
- **Анализ**: go.mod, исходный код

### JavaScript/TypeScript
- **Пакетные менеджеры**: npm, yarn, pnpm
- **Фреймворки**: React, Vue, Angular, Express, Next.js
- **Анализ**: package.json, tsconfig.json

### Python
- **Менеджеры пакетов**: pip, poetry, pipenv
- **Фреймворки**: Django, Flask, FastAPI
- **Анализ**: requirements.txt, pyproject.toml, setup.py

## 🛠️ Установка и настройка

### Предварительные требования

- Python 3.8 или выше
- Git
- Docker и Docker Compose (для локальной инфраструктуры)

### Установка

#### Способ 1: Нативная установка

1. **Клонируйте репозиторий**:
```bash
git clone https://github.com/your-org/self-deploy-ci-cd.git
cd self-deploy-ci-cd
```

2. **Установите зависимости**:
```bash
pip install -r requirements.txt
```

3. **Запустите локальную инфраструктуру** (опционально):
```bash
cd infrastructure
docker-compose up -d
```

#### Способ 2: Docker контейнер

1. **Соберите Docker образ**:
```bash
docker build -t self-deploy-ci-cd .
```

2. **Запустите контейнер**:
```bash
# Базовая команда
docker run -v $(pwd)/output:/home/app/output self-deploy-ci-cd --help

# Анализ репозитория
docker run -v $(pwd)/output:/home/app/output self-deploy-ci-cd \
  --repo https://github.com/user/project.git --system jenkins

# Демонстрационный режим
docker run -v $(pwd)/demo_output:/home/app/demo_output self-deploy-ci-cd \
  --demo
```

#### Способ 3: Docker Compose

1. **Запустите полный стек**:
```bash
# Запуск Self-Deploy CI/CD и инфраструктуры
docker-compose up -d

# Запуск только Self-Deploy CI/CD
docker-compose up self-deploy-ci-cd

# Выполнение команды в контейнере
docker-compose run self-deploy-ci-cd --repo https://github.com/user/project.git --system both
```

## 🚀 Использование

### Базовое использование

#### Нативный запуск
```bash
# Анализ репозитория и генерация Jenkins конфигурации
python main.py --repo https://github.com/user/java-project --system jenkins

# Генерация GitLab CI конфигурации
python main.py --repo https://gitlab.com/user/python-app --system gitlab --output ./ci-config

# Подробный режим
python main.py --repo git@github.com:user/go-service.git --system jenkins --verbose
```

#### Docker запуск
```bash
# Анализ репозитория через Docker
docker run -v $(pwd)/output:/home/app/output self-deploy-ci-cd \
  --repo https://github.com/user/java-project --system jenkins

# Генерация для обеих систем
docker run -v $(pwd)/output:/home/app/output self-deploy-ci-cd \
  --repo https://github.com/user/project.git --system both --verbose

# Демонстрация на примерах проектов
docker run -v $(pwd)/demo_output:/home/app/demo_output self-deploy-ci-cd --demo
```

### Параметры командной строки

| Параметр | Обязательный | Описание | По умолчанию |
|----------|--------------|----------|--------------|
| `--repo` | ✅ | URL Git-репозитория | - |
| `--system` | ❌ | CI/CD система (jenkins/gitlab/both) | jenkins |
| `--output` | ❌ | Директория для сохранения | ./output |
| `--verbose` | ❌ | Подробный вывод | False |
| `--demo` | ❌ | Демонстрационный режим | False |

### Примеры использования

#### Java проект с Maven
```bash
python main.py --repo https://github.com/spring-projects/spring-petclinic --system jenkins
```

#### Go проект
```bash
python main.py --repo https://github.com/gin-gonic/gin --system gitlab --output ./gin-ci
```

#### React приложение
```bash
python main.py --repo https://github.com/facebook/react --system jenkins --verbose
```

#### Python проект с FastAPI
```bash
python main.py --repo https://github.com/tiangolo/fastapi --system gitlab
```

## 🏗️ Локальная инфраструктура

Система включает полную локальную CI/CD инфраструктуру на базе Docker Compose:

### Запуск инфраструктуры

#### Способ 1: Отдельная инфраструктура
```bash
cd infrastructure
docker-compose up -d
```

#### Способ 2: Полный стек с Self-Deploy CI/CD
```bash
# Запуск всей системы
docker-compose up -d

# Остановка системы
docker-compose down

# Просмотр логов
docker-compose logs -f
```

### Доступные сервисы

| Сервис | URL | Порт | Описание |
|--------|-----|------|----------|
| Self-Deploy CI/CD | Контейнер | - | Основное приложение |
| Jenkins | http://localhost:8080 | 8080 | CI/CD сервер |
| GitLab | http://localhost:8081 | 8081 | GitLab CE |
| SonarQube | http://localhost:9000 | 9000 | Анализ кода |
| Nexus | http://localhost:8082 | 8082 | Репозиторий артефактов |

### Настройка Jenkins

1. Откройте http://localhost:8080
2. Плагины установятся автоматически из `infrastructure/jenkins/plugins.txt`
3. Настройте инструменты (JDK, Maven, Node.js) через UI

### Настройка GitLab

1. Откройте http://localhost:8081
2. Установите пароль для root пользователя при первом входе
3. Создайте проект и настройте Runner

## 📊 Этапы CI/CD пайплайна

Сгенерированные конфигурации включают все необходимые этапы:

1. **Build** - Сборка проекта с кешированием зависимостей
2. **Test** - Unit и интеграционные тесты с генерацией отчетов
3. **Code Analysis** - Статический анализ кода через SonarQube
4. **Docker Build** - Multi-stage сборка Docker образа
5. **Publish** - Публикация артефактов в Nexus/Docker Registry
6. **Deploy** - Развертывание на staging/production окружения

## 🧪 Тестирование

### Запуск тестов

```bash
# Установите тестовые зависимости
pip install -r tests/requirements.txt

# Запустите тесты
python -m pytest tests/ -v
```

### Структура тестов

- `tests/test_analyzers.py` - Тесты анализаторов
- `tests/test_generators.py` - Тесты генераторов
- `tests/test_integration.py` - Интеграционные тесты

## 📁 Структура проекта

```
self-deploy-ci-cd/
├── src/                    # Исходный код
│   ├── analyzers/         # Модули анализа репозитория
│   ├── generators/        # Генераторы CI/CD конфигураций
│   ├── templates/         # Шаблоны Jenkins и GitLab CI
│   └── utils/             # Вспомогательные утилиты
├── infrastructure/        # Локальная инфраструктура
│   ├── docker-compose.yml
│   └── jenkins/plugins.txt
├── examples/              # Примеры использования
├── docs/                  # Документация
├── tests/                 # Тесты
├── main.py               # Основной скрипт
├── requirements.txt      # Зависимости Python
├── Dockerfile           # Docker образ приложения
├── docker-compose.yml   # Полный стек с приложением
└── .dockerignore        # Игнорируемые файлы для Docker
```

## 🔧 Разработка

### Установка для разработки

```bash
git clone https://github.com/your-org/self-deploy-ci-cd.git
cd self-deploy-ci-cd
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
pip install -r requirements.txt
pip install -r tests/requirements.txt
```

### Добавление поддержки нового языка

1. Создайте детектор в `src/analyzers/detectors/`
2. Добавьте шаблоны в `src/templates/jenkins/` и `src/templates/gitlab/`
3. Обновите `RepositoryAnalyzer` для использования нового детектора
4. Добавьте тесты

### Создание кастомных шаблонов

Шаблоны используют синтаксис Jinja2. Основные переменные:
- `project_name` - Имя проекта
- `language` - Язык программирования
- `framework` - Фреймворк
- `build_tool` - Инструмент сборки
- `docker_registry` - Docker registry URL

## 🤝 Вклад в проект

Мы приветствуем вклады в развитие проекта! 

1. Форкните репозиторий
2. Создайте ветку для вашей функции (`git checkout -b feature/amazing-feature`)
3. Закоммитьте изменения (`git commit -m 'Add amazing feature'`)
4. Запушьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.

## 📞 Поддержка

- **Issues**: [GitHub Issues](https://github.com/your-org/self-deploy-ci-cd/issues)
- **Документация**: [Docs](docs/)
- **Примеры**: [Examples](examples/)

## 🎯 Дорожная карта

- [x] Поддержка 4 базовых языков (Java, Go, JavaScript, Python)
- [x] Генерация конфигураций для Jenkins и GitLab CI
- [x] Локальная инфраструктура с Docker Compose
- [x] Docker образ приложения
- [ ] Поддержка дополнительных языков (Rust, Ruby, PHP)
- [ ] Интеграция с Kubernetes для деплоя
- [ ] Поддержка мониторинга и алертинга
- [ ] Графический интерфейс
- [ ] CI/CD для мобильных приложений

---

**Self-Deploy CI/CD** - автоматизируйте ваши пайплайны без DevOps экспертизы! 🚀