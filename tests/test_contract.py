"""Контракт программы: то, что не меняется ни на одном этапе.

Эти тесты живут весь курс и не правятся. Они смотрят только на то,
что программа **печатает**, и ничего не знают о её внутреннем устройстве:
словари там внутри или объекты — им всё равно.

Именно поэтому они работают и на этапе 1, и на всех следующих.
Если такой тест покраснел — вы изменили поведение программы,
а не улучшили её устройство.

Это характеризационное тестирование: сначала фиксируем поведение,
потом меняем код.
"""

import pytest

pytestmark = pytest.mark.contract


EXPECTED_REPORT = """Файлов в каталоге: 4

  data_structures.md
    заголовок: Структуры данных
    строк: 5, слов: 36, символов: 250
  empty.md
    заголовок: (пустой файл)
    строк: 0, слов: 0, символов: 0
  functions.md
    заголовок: Функции
    строк: 3, слов: 15, символов: 112
  python_basics.md
    заголовок: Основы Python
    строк: 4, слов: 26, символов: 198

Всего слов во всех материалах: 77
"""


@pytest.fixture
def printed_report(capsys, materials_dir):
    """Возвращает строки отчёта, напечатанные программой."""
    from study_assistant.catalog import build_catalog, print_report

    try:
        print_report(build_catalog(materials_dir))
    except NotImplementedError as error:
        pytest.skip(f"программа ещё не собирает отчёт: {error}")

    return capsys.readouterr().out.splitlines()


def test_report_matches_reference(printed_report):
    """Отчёт совпадает с эталоном до последнего пробела."""
    expected = EXPECTED_REPORT.splitlines()

    for number, line in enumerate(expected, start=1):
        assert number <= len(printed_report), f"в выводе не хватает строки {number}: {line!r}"
        assert printed_report[number - 1] == line, (
            f"строка {number} отличается\n"
            f"  ожидалось: {line!r}\n"
            f"  получено:  {printed_report[number - 1]!r}"
        )

    assert len(printed_report) == len(expected), (
        f"в выводе {len(printed_report)} строк вместо {len(expected)}"
    )


def test_files_printed_alphabetically(printed_report):
    """Файлы печатаются в одном и том же порядке на любой машине."""
    printed_files = [
        line.strip() for line in printed_report if line.startswith("  ") and line.endswith(".md")
    ]

    assert printed_files == sorted(printed_files), (
        f"файлы напечатаны не по алфавиту: {printed_files}\nпроверьте, что glob обёрнут в sorted()"
    )


def test_total_word_count(printed_report):
    """Суммарное количество слов во всех материалах постоянно."""
    total_lines = [line for line in printed_report if line.startswith("Всего слов")]

    assert total_lines, "в отчёте нет итоговой строки «Всего слов во всех материалах»"
    assert total_lines[-1] == "Всего слов во всех материалах: 77"
