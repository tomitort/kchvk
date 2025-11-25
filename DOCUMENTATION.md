# Документация Self-Deploy CI/CD

## Обзор системы

Self-Deploy CI/CD - это интеллектуальный скрипт, который автоматически анализирует Git-репозитории и генерирует полнофункциональные конфигурации CI/CD для Jenkins и GitLab CI. Система поддерживает 4 базовых языка программирования и их экосистемы.

## Поддерживаемые языки и экосистемы

### 1. Java/Kotlin

#### Логика определения
- **Основные файлы**: `pom.xml` (Maven), `build.gradle` (Gradle), `build.gradle.kts`
- **Фреймворки**: Spring Boot, Jakarta EE, Micronaut, Quarkus
- **Версии**: Определяется из файлов конфигурации (Java version в pom.xml или build.gradle)

#### Анализируемые файлы конфигурации
```xml
<!-- pom.xml -->
<project>
  <groupId>com.example</groupId>
  <artifactId>my-app</artifactId>
  <version>1.0.0</version>
  <properties>
    <java.version>11</java.version>
    <maven.compiler.source>11</maven.compiler.source>
  </properties>
  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
  </dependencies>
</project>
```

```gradle
// build.gradle
plugins {
    id 'org.springframework.boot' version '2.7.0'
    id 'java'
}

java {
    sourceCompatibility = '11'
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
}
```

#### Build-инструменты
| Инструмент | Файлы конфигурации | Команды сборки |
|------------|-------------------|----------------|
| Maven | pom.xml | `mvn clean compile`, `mvn test`, `mvn deploy` |
| Gradle | build.gradle, build.gradle.kts | `gradle build`, `gradle test`, `gradle publish` |

### 2. Go

#### Логика определения
- **Основные файлы**: `go.mod`, `go.sum`, `main.go`
- **Фреймворки**: Gin, Echo, Fiber, Gorilla Mux
- **Версии**: Определяется из go.mod (go version)

#### Анализируемые файлы конфигурации
```go
// go.mod
module github.com/user/my-app

go 1.19

require (
    github.com/gin-gonic/gin v1.8.1
    github.com/stretchr/testify v1.8.0
)
```

#### Build-инструменты
| Инструмент | Файлы конфигурации | Команды сборки |
|------------|-------------------|----------------|
| Go Modules | go.mod, go.sum | `go mod download`, `go build`, `go test` |

### 3. TypeScript/JavaScript

#### Логика определения
- **Основные файлы**: `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
- **Фреймворки**: React, Vue.js, Angular, Express.js, NestJS
- **Версии**: Node.js version из package.json (engines.node)

#### Анализируемые файлы конфигурации
```json
// package.json
{
  "name": "my-app",
  "version": "1.0.0",
  "scripts": {
    "build": "webpack --mode production",
    "test": "jest",
    "test:coverage": "jest --coverage"
  },
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  },
  "devDependencies": {
    "webpack": "^5.0.0",
    "jest": "^28.0.0"
  },
  "engines": {
    "node": ">=16.0.0"
  }
}
```

#### Build-инструменты
| Инструмент | Файлы конфигурации | Команды сборки |
|------------|-------------------|----------------|
| npm | package.json, package-lock.json | `npm ci`, `npm run build`, `npm test` |
| Yarn | package.json, yarn.lock | `yarn install`, `yarn build`, `yarn test` |
| pnpm | package.json, pnpm-lock.yaml | `pnpm install`, `pnpm build`, `pnpm test` |

### 4. Python

#### Логика определения
- **Основные файлы**: `requirements.txt`, `setup.py`, `pyproject.toml`, `Pipfile`, `poetry.lock`
- **Фреймворки**: Django, Flask, FastAPI, Pyramid
- **Версии**: Python version из pyproject.toml или setup.py

#### Анализируемые файлы конфигурации
```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="my-app",
    version="1.0.0",
    python_requires=">=3.8",
    packages=find_packages(),
    install_requires=[
        "django>=4.0.0",
        "requests>=2.25.0"
    ]
)
```

```toml
# pyproject.toml
[tool.poetry]
name = "my-app"
version = "1.0.0"
description = "My Python application"

[tool.poetry.dependencies]
python = "^3.8"
django = "^4.0.0"

[tool.poetry.dev-dependencies]
pytest = "^7.0.0"
```

#### Build-инструменты
| Инструмент | Файлы конфигурации | Команды сборки |
|------------|-------------------|----------------|
| pip | requirements.txt, setup.py | `pip install -r requirements.txt`, `python setup.py build` |
| Poetry | pyproject.toml, poetry.lock | `poetry install`, `poetry build`, `poetry publish` |
| Pipenv | Pipfile, Pipfile.lock | `pipenv install`, `pipenv run python setup.py build` |

## Таблица соответствия языков и build-инструментов

| Язык | Основные build-инструменты | Альтернативные инструменты |
|------|---------------------------|---------------------------|
| Java/Kotlin | Maven, Gradle | Ant, Bazel |
| Go | Go Modules | Dep, Glide |
| JavaScript/TypeScript | npm, Yarn, pnpm | Bun, Deno |
| Python | pip, Poetry, Pipenv | Conda, Hatch |

## Архитектура детекторов

### Базовый детектор
Все детекторы наследуются от [`BaseDetector`](src/analyzers/detectors/base_detector.py:1) и реализуют:
- Метод `detect()` - проверка наличия характерных файлов
- Метод `analyze()` - детальный анализ проекта
- Свойство `language_name` - название языка

### Java детектор
- **Файлы обнаружения**: `pom.xml`, `build.gradle`, `build.gradle.kts`
- **Анализ версии**: Извлекает из свойств Maven или Gradle
- **Определение фреймворка**: По зависимостям в pom.xml или build.gradle

### Go детектор
- **Файлы обнаружения**: `go.mod`, `go.sum`, `*.go` файлы
- **Анализ версии**: Из директивы `go` в go.mod
- **Определение фреймворка**: По импортам в исходном коде

### JavaScript детектор
- **Файлы обнаружения**: `package.json`, `package-lock.json`, `yarn.lock`
- **Анализ версии**: Из поля `engines.node` в package.json
- **Определение фреймворка**: По зависимостям в package.json

### Python детектор
- **Файлы обнаружения**: `requirements.txt`, `setup.py`, `pyproject.toml`
- **Анализ версии**: Из python_requires в setup.py или pyproject.toml
- **Определение фреймворка**: По установленным пакетам

## Шаблоны CI/CD пайплайнов

### Обязательные этапы для всех языков

1. **Build** - Сборка проекта с кешированием зависимостей
2. **Test** - Запуск unit и интеграционных тестов
3. **Code Analysis** - Статический анализ с SonarQube
4. **Docker Build** - Многоэтапная сборка Docker образа
5. **Publish** - Публикация артефактов в Nexus/Docker Registry
6. **Deploy** - Развертывание на staging и production

### Особенности для каждого языка

#### Java
- **Кеширование**: .m2/repository (Maven) или .gradle/caches (Gradle)
- **Анализ кода**: Maven Sonar Plugin или Gradle SonarQube Plugin
- **Публикация**: Maven deploy или Gradle publish

#### Go
- **Кеширование**: go/pkg/mod
- **Анализ кода**: SonarScanner с отчетом о покрытии
- **Публикация**: Docker образ в registry

#### JavaScript
- **Кеширование**: node_modules и package manager cache
- **Анализ кода**: SonarScanner с отчетом о покрытии
- **Публикация**: npm/yarn/pnpm publish и Docker образ

#### Python
- **Кеширование**: виртуальное окружение и dist папка
- **Анализ кода**: SonarScanner с отчетом о покрытии pytest
- **Публикация**: twine upload и Docker образ

## Переменные окружения

### Общие переменные
- `PROJECT_NAME` - Имя проекта
- `DOCKER_REGISTRY` - URL Docker registry
- `NEXUS_URL` - URL Nexus repository
- `SONAR_URL` - URL SonarQube сервера

### Jenkins специфичные
- `BUILD_NUMBER` - Номер сборки
- `JOB_NAME` - Имя джобы
- `WORKSPACE` - Рабочая директория

### GitLab CI специфичные
- `CI_COMMIT_SHA` - Хэш коммита
- `CI_PROJECT_NAME` - Имя проекта
- `CI_REGISTRY` - GitLab container registry

## Обработка Edge Cases

### Мультимодульные проекты
- Java: Анализ родительского pom.xml и модулей
- JavaScript: Анализ workspace конфигурации в package.json
- Python: Анализ setup.py с несколькими пакетами

### Нестандартные структуры
- Кастомные пути к исходному коду
- Альтернативные имена конфигурационных файлов
- Гибридные проекты (например, фронтенд + бэкенд)

### Обработка ошибок
- Отсутствие конфигурационных файлов
- Неподдерживаемые версии языков
- Конфликтующие зависимости

## Интеграция с инструментами

### SonarQube
- Настройка качества кода для каждого языка
- Интеграция тестового покрытия
- Анализ уязвимостей зависимостей

### Nexus/Artifactory
- Хранение артефактов сборки
- Управление зависимостями
- Публикация пакетов

### Docker Registry
- Хранение Docker образов
- Тегирование версий
- Многоэтапные сборки для оптимизации

## Безопасность

### Переменные окружения
- Использование секретов для учетных данных
- Маскирование чувствительной информации в логах
- Безопасное хранение токенов доступа

### Доступ к инфраструктуре
- RBAC для CI/CD систем
- Ограничение прав контейнеров
- Аудит действий пайплайнов

## Мониторинг и логирование

### Метрики пайплайнов
- Время выполнения каждого этапа
- Успешность сборок
- Использование ресурсов

### Логи анализа
- Детальный отчет об обнаруженных технологиях
- Предупреждения о потенциальных проблемах
- Рекомендации по оптимизации