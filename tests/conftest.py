"""Общие фикстуры, данные и настройка вывода для всех тестов проекта.

Этот файл читают все тесты. Менять его не нужно.
"""

import importlib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
MATERIALS = ROOT / "materials"

# Ожидаемые характеристики учебных файлов — эталон на всех этапах курса.
EXPECTED = {
    "data_structures.md": {
        "title": "Структуры данных",
        "lines": 5,
        "words": 36,
        "chars": 250,
    },
    "empty.md": {
        "title": "(пустой файл)",
        "lines": 0,
        "words": 0,
        "chars": 0,
    },
    "functions.md": {
        "title": "Функции",
        "lines": 3,
        "words": 15,
        "chars": 112,
    },
    "python_basics.md": {
        "title": "Основы Python",
        "lines": 4,
        "words": 26,
        "chars": 198,
    },
}

FILES_IN_ORDER = sorted(EXPECTED)
TOTAL_WORDS = 77


# --- определение, начат ли этап ----------------------------------------------


def stage_not_ready(module_name, attribute=None, *call_args):
    """Проверяет, что этап ещё не начат, — для пропуска его тестов.

    Тесты будущих этапов не должны сыпать ошибками, пока студент работает
    над текущим. Как только нужный код появился, тесты включаются сами.

    Этап считается не начатым, если:
      • модуля ещё нет в проекте                  → ImportError
      • в модуле нет нужного класса или функции   → имя не найдено
      • пробный вызов поднимает NotImplementedError → заготовка не дописана

    Применение в файле тестов этапа:

        pytestmark = [
            pytest.mark.stage3,
            pytest.mark.skipif(
                stage_not_ready("study_assistant.source", "FolderSource"),
                reason="этап 3 ещё не начат",
            ),
        ]

    Аргументы после имени передаются при пробном вызове. Если вызывать
    ничего не нужно — не передавайте их: хватит проверки, что имя есть.
    """
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        return True

    if attribute is None:
        return False

    target = getattr(module, attribute, None)
    if target is None:
        return True

    if not call_args:
        return False

    try:
        target(*call_args)
    except NotImplementedError:
        return True
    except Exception:
        # Любая другая ошибка означает, что код уже пишут —
        # тесты должны работать и показать, что именно не так.
        return False

    return False


# --- фикстуры ---------------------------------------------------------------


@pytest.fixture
def materials_dir():
    """Папка с учебными материалами."""
    return MATERIALS


@pytest.fixture
def functions_md():
    """Путь к обычному файлу материалов."""
    return MATERIALS / "functions.md"


@pytest.fixture
def empty_md():
    """Путь к пустому файлу материалов."""
    return MATERIALS / "empty.md"


def make_material(*args):
    """Создаёт объект Material, аккуратно обрабатывая незаконченную работу."""
    from study_assistant.material import Material

    try:
        return Material(*args)
    except NotImplementedError:
        pytest.skip("Material.__init__ ещё не написан — это задание этапа 2")
    except TypeError as error:
        if "positional argument" in str(error):
            pytest.fail(
                f"не удалось создать объект: {error}\nвозможно, забыт self в объявлении __init__"
            )
        raise


@pytest.fixture
def sample_material():
    """Готовый объект Material для проверки методов."""
    return make_material("functions.md", "Функции", 3, 15, 112)


@pytest.fixture
def blank_material():
    """Объект Material, соответствующий пустому файлу."""
    return make_material("empty.md", EXPECTED["empty.md"]["title"], 0, 0, 0)


# --- понятный итог в конце прогона ------------------------------------------


def pytest_terminal_summary(terminalreporter):
    """Печатает итог прогона простым языком."""
    stats = terminalreporter.stats
    passed = stats.get("passed", [])
    failed = stats.get("failed", []) + stats.get("error", [])
    skipped = stats.get("skipped", [])

    # Пропуски бывают двух видов: будущие этапы и незаконченная работа.
    future = 0
    unfinished = 0
    for report in skipped:
        reason = str(getattr(report, "longrepr", "") or "")
        if "ещё не начат" in reason:
            future += 1
        else:
            unfinished += 1

    checked = len(passed) + len(failed) + unfinished
    if checked == 0 and future == 0:
        return

    write = terminalreporter.write_line
    write("")
    write("=" * 62)

    if not failed and unfinished == 0:
        write(f"  ГОТОВО: пройдено {len(passed)} из {checked}")
        write("  Можно коммитить.")
    else:
        write(f"  Пройдено {len(passed)} из {checked}")
        if unfinished:
            write(f"  Пропущено {unfinished} — нужные функции пока не написаны")
        if failed:
            write(f"  Не проходит {len(failed)}")
            if len(failed) > 1:
                write("")
                write("  Совет: добавьте флаг -x, чтобы разбирать по одной ошибке:")
                write("    uv run pytest -x")

    if future:
        write("")
        write(f"  Ещё {future} тестов относятся к будущим этапам — это нормально.")

    write("=" * 62)
