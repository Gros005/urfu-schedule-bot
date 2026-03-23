# Urfu Schedule Bot
Телеграм-бот для получения расписания занятий Уральского федерального университета (УрФУ). Бот предоставляет удобный доступ к расписанию групп и преподавателей прямо в Telegram.
---

## 🚀 Установка и запуск

### Установка проекта

1. Клонируйте репозиторий:
```bash
git clone <ваш-репозиторий>
cd <папка-проекта>
```

2. Установите зависимости через Poetry:
```bash
poetry install
```

3. Активируйте виртуальное окружение:
```bash
poetry shell
```

### 📦 Управление зависимостями

- **Установка новой зависимости:**
  ```bash
  poetry add <пакет>  # основная зависимость
  poetry add --group dev <пакет>  # dev зависимость
  ```

- **Обновление зависимостей:**
  ```bash
  poetry update
  ```

- **Просмотр установленных пакетов:**
  ```bash
  poetry show --tree
  ```

## 🛠 Разработка

### Автоматизация с помощью taskipy

Проект использует `taskipy` для автоматизации рутинных задач. Все доступные команды:

```bash
# Просмотр всех задач
poetry run task --list

# Альтернативно, если вы в poetry shell:
task --list
```

### Основные команды разработки

#### 🏃‍♂️ Запуск приложения
```bash
poetry run bot

# Альтернативно, если вы в poetry shell:
bot
```

#### 🧪 Тестирование
```bash
# Все тесты
poetry run task test

# Тесты с покрытием кода
poetry run task test-cov

# Быстрые тесты с детальным выводом (останавливаются при первой ошибке)
poetry run task test-fast

# Полная проверка с HTML-отчётом о покрытии
poetry run task test-all
```

#### 💅 Форматирование кода
```bash
# Автоформатирование кода (black + isort)
poetry run task format

# Проверка форматирования без изменений
poetry run task format-check

# Проверка стиля кода (flake8)
poetry run task lint

# Проверка типов (если используется типизация)
poetry run task type-check
```

#### 🔍 Комплексная проверка качества
```bash
# Все проверки перед коммитом
poetry run task qa
# (форматирование + линтинг + тесты)
```

### 📁 Структура проекта

```
project/
├── src/
│   ├── api_client.py      # Клиент для API расписания УрФУ
│   ├── config.py          # Конфигурация и логирование
│   └── types.py           # Типы данных
├── tests/                  # Тесты
├── docs/                   # Документация Sphinx
├── pyproject.toml         # Конфигурация Poetry и taskipy
├── poetry.lock            # Фиксированные версии зависимостей
└── README.md
```

### 🔌 API Клиент

Клиент для работы с API расписания УрФУ.

```python
from src.api_client import UrfuAPIClient

client = UrfuAPIClient()

# Поиск групп
groups = client.search_groups("МЕН-333009")
for group in groups:
    print(f"{group.title} (ID: {group.id})")

# Получение расписания
schedule = client.get_group_schedule(group_id=63725)
for day in schedule.days:
    print(f"{day.weekday} {day.date}")
    for lesson in day.lessons:
        print(f"  {lesson.timeBegin} {lesson.title}")

client.close()
```

### 📚 Документация

Документация генерируется с помощью Sphinx.

```bash
# Сборка документации
poetry run sphinx-build -b html docs/source docs/_build
```

### Рабочий процесс разработки

1. **Начало работы:**
   ```bash
   git checkout -b feature/your-feature
   poetry install
   poetry shell
   ```

2. **Перед коммитом:**
   ```bash
   poetry run task qa  # или поэтапно:
   poetry run task format
   poetry run task lint
   poetry run task test
   ```

3. **После коммита:**
   ```bash
   git push origin feature/your-feature
   ```

### 🧪 Запуск тестов без taskipy

Если нужно запустить тесты напрямую:
```bash
poetry run pytest
poetry run pytest -v  # с подробным выводом
poetry run pytest tests/test_file.py::test_function  # конкретный тест
```

### 🔧 Настройка IDE

#### PyCharm
1. Откройте настройки → Project → Python Interpreter
2. Выберите "Add Interpreter" → "Poetry Environment"
3. Установите black и isort как внешние инструменты

### 🐛 Отладка

Запуск с отладкой:
```bash
poetry run python -m pdb -m your_module
```

Или используйте встроенный отладчик:
```python
import pdb; pdb.set_trace()
```

## 📝 Полезные команды Poetry

```bash
# Создать requirements.txt из Poetry
poetry export -f requirements.txt --output requirements.txt --without-hashes

# Проверить целостность pyproject.toml
poetry check

# Обновить версию проекта
poetry version patch  # 1.0.0 → 1.0.1
poetry version minor  # 1.0.0 → 1.1.0
poetry version major  # 1.0.0 → 2.0.0

# Показать информацию о проекте
poetry show --why <пакет>  # почему установлен пакет
```
