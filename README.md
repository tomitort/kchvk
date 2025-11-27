# 🚀 Self-Deploy CI/CD

Автоматическая генерация CI/CD конфигураций для Jenkins и GitLab CI. Система анализирует репозитории и генерирует готовые конфигурации для 4 языков программирования: Java, Go, JavaScript/TypeScript, Python.

---

## 🛠️ Быстрый старт

### Способ 1: Локальный запуск (рекомендуется)

```bash
# Установка зависимостей
pip install -r requirements.txt

# Анализ репозитория
python main.py --repo https://github.com/user/project --system both --verbose

# Демонстрационный режим
python main.py --demo
```

### Способ 2: Запуск через Docker

```bash
# Сборка образа
docker build -t self-deploy-ci-cd .

# Запуск анализа
docker run -v $(pwd)/output:/home/app/output self-deploy-ci-cd \
  --repo https://github.com/user/project --system both
```

### Способ 3: Полная CI/CD инфраструктура

```bash
# Запуск всей инфраструктуры
cd infrastructure
docker-compose up -d
```

**Сервисы будут доступны:**
- **Jenkins**: http://localhost:8080
- **GitLab**: http://localhost:8081  
- **SonarQube**: http://localhost:9000
- **Nexus**: http://localhost:8082

---

## 📋 Параметры запуска

| Параметр | Описание | Пример |
|----------|----------|--------|
| `--repo <url>` | URL репозитория для анализа | `--repo https://github.com/user/project` |
| `--system <jenkins\|gitlab\|both>` | Целевая CI/CD система | `--system both` |
| `--output <dir>` | Выходная директория | `--output ./my-configs` |
| `--verbose` | Подробный режим | `--verbose` |
| `--demo` | Демонстрационный режим | `--demo` |
| `--help` | Показать справку | `--help` |

---

## 🎯 Примеры использования

```bash
# Анализ Go проекта
python main.py --repo https://github.com/syncthing/syncthing --system both

# Анализ Java проекта  
python main.py --repo https://github.com/jenkinsci/jenkins --system jenkins

# Анализ JavaScript проекта
python main.py --repo https://github.com/RocketChat/Rocket.Chat --system gitlab

# Анализ Python проекта
python main.py --repo https://github.com/pallets/flask --system both
```

---

## 🛠️ Управление инфраструктурой

```bash
# Остановка сервисов
docker-compose down

# Перезапуск
docker-compose restart

# Просмотр логов
docker-compose logs -f

# Полная очистка
docker-compose down -v
```

---

## 🔧 Поддерживаемые технологии

- **Java**: Maven, Gradle
- **Go**: Go Modules
- **JavaScript/TypeScript**: npm, yarn
- **Python**: pip, poetry

---

## 📞 Поддержка

Если возникли проблемы:
1. Проверьте логи: `docker-compose logs [service]`
2. Убедитесь что порты свободны
3. Перезапустите: `docker-compose down && docker-compose up -d`

**Подробная документация:** [ИНСТРУКЦИЯ_ЗАПУСКА.md](./ИНСТРУКЦИЯ_ЗАПУСКА.md)

**Готово!** Система запущена и готова к использованию! 🚀