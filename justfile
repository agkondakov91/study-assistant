# Команды проекта. Запустите "just" без аргументов, чтобы увидеть список.
#
# just показывает команду, которую выполняет, — так вы видите настоящие
# команды uv и можете запускать их напрямую, без just.

# Список доступных команд
default:
    @just --list --unsorted

# Установить зависимости и окружение
setup:
    uv sync

# Запустить программу
run:
    uv run main.py

# Все тесты
test:
    uv run pytest -v

# Тесты одного этапа, с остановкой на первой ошибке: just stage 1
stage NUMBER:
    uv run pytest -m stage{{NUMBER}} -x

# Только контрактные тесты — поведение программы
contract:
    uv run pytest -m contract

# Проверить стиль кода
lint:
    uv run ruff check .

# Исправить стиль автоматически
fix:
    uv run ruff check --fix .
    uv run ruff format .

# Всё, что проверяет преподаватель: стиль и тесты
check: lint test

# Удалить кеши и временные файлы
clean:
    rm -rf .pytest_cache
    find . -type d -name __pycache__ -exec rm -rf {} +
    rm -f catalog.json