# ToneScript to WAV Generator 🎵
ToneScript telephone tone to WAV file converter
Генератор WAV файлов из телефонных тонов в формате ToneScript.

## ✨ Возможности

- 🎯 Полная поддержка формата ToneScript
- 📞 18 стандартных телефонных тонов (Северная Америка)
- 🔧 Поддержка сложных паттернов
- 🎚 Автоматическая нормализация

## 📦 Быстрый старт с uv

### Установка uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Клонирование и установка

```bash
# Клонируем репозиторий
git clone https://github.com/andrew-palamar/tonescript-generator.git
cd tonescript-generator

# Устанавливаем зависимости одной командой!
uv sync
```

### Активация окружения

```bash
# Автоматическая активация при запуске команд
uv run tonescript2wav --help

# Или активируйте вручную
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate      # Windows
```

## 🚀 Использование

### Генерация одного тона

```bash
# Через uv run
uv run tonescript2wav "350@-19,440@-19;10(*/0/1+2)" output/dial_tone.wav

# Или после активации окружения
tonescript2wav "480@-19,620@-19;10(.5/.5/1+2)" output/busy.wav --duration 5.0
```

### Генерация всех тонов

```bash
uv run test-tones
# или после активации окружения
test-tones
```

## 📝 Команды проекта

| Команда                 | Описание                      |
| ----------------------- | ----------------------------- |
| `uv sync`               | Установить все зависимости    |
| `uv run tonescript2wav` | Запустить генератор           |
| `uv run test-tones`     | Сгенерировать все тоны        |
| `uv pip list`           | Показать установленные пакеты |
| `uv add numpy`          | Добавить новую зависимость    |

## 🏗 Структура проекта

```
.
├── pyproject.toml          # Конфигурация и зависимости
├── README.md
├── src/
│   └── tonescript_generator/
│       ├── __init__.py
│       ├── core.py        # Основная логика
│       ├── cli.py         # CLI интерфейс
│       └── tester.py      # Тестер тонов
└── output/                 # Сгенерированные WAV файлы
```

## 🔧 Разработка

Для разработки установите dev-зависимости:

```bash
uv pip install -e ".[dev]"
# или через uv sync с dev зависимостями
uv sync --dev
```

## 📄 Лицензия

MIT

## Референсы

https://en.wikipedia.org/wiki/ToneScript
