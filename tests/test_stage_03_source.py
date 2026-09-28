"""Этап 3: источник материалов.

Задание: stages/stage-03-source/README.md
Запуск: uv run pytest -m stage3

Тесты проверяют три вещи:
  • контракт нельзя обойти — объект абстрактного класса не создаётся;
  • обе реализации отдают одинаковые по типу данные;
  • отчёт не зависит от того, какой источник подставили.

Пока FolderSource.__init__ не написан, весь файл пропускается.
"""

import json

import pytest

from tests.conftest import EXPECTED, FILES_IN_ORDER, MATERIALS, stage_not_ready

pytestmark = [
    pytest.mark.stage3,
    pytest.mark.skipif(
        stage_not_ready("study_assistant.source", "FolderSource", MATERIALS),
        reason="этап 3 ещё не начат",
    ),
]


@pytest.fixture
def catalog_json(tmp_path):
    """Файл каталога в формате save_catalog — для проверки JsonSource."""
    records = [
        {
            "file": name,
            "title": EXPECTED[name]["title"],
            "lines": EXPECTED[name]["lines"],
            "words": EXPECTED[name]["words"],
            "chars": EXPECTED[name]["chars"],
        }
        for name in FILES_IN_ORDER
    ]
    path = tmp_path / "catalog.json"
    with open(path, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)
    return path


# --- контракт ----------------------------------------------------------------


def test_abstract_source_cannot_be_created():
    """Объект MaterialSource создать нельзя — это описание требований."""
    from study_assistant.source import MaterialSource

    with pytest.raises(TypeError) as info:
        MaterialSource()

    assert "abstract" in str(info.value), (
        "ожидалась ошибка про абстрактный класс, а получена другая:\n"
        f"  {info.value}\n"
        "проверьте, что MaterialSource наследуется от ABC, "
        "а description и load помечены @abstractmethod"
    )


def test_incomplete_subclass_cannot_be_created():
    """Наследник, реализовавший не всё, тоже не создаётся."""
    from study_assistant.source import MaterialSource

    class BrokenSource(MaterialSource):
        """Источник, у которого есть load, но нет description."""

        def load(self):
            """Возвращает пустой список."""
            return []

    with pytest.raises(TypeError) as info:
        BrokenSource()

    assert "description" in str(info.value), (
        f"Python должен пожаловаться именно на description\n  получено: {info.value}"
    )


def test_both_sources_are_material_source(catalog_json):
    """Обе реализации — источники материалов с точки зрения isinstance."""
    from study_assistant.source import FolderSource, JsonSource, MaterialSource

    assert isinstance(FolderSource(MATERIALS), MaterialSource), (
        "FolderSource должен наследоваться от MaterialSource"
    )
    assert isinstance(JsonSource(catalog_json), MaterialSource), (
        "JsonSource должен наследоваться от MaterialSource"
    )


# --- описание источника ------------------------------------------------------


def test_description_is_property_not_method():
    """К описанию обращаются без скобок — это @property."""
    from study_assistant.source import FolderSource

    value = FolderSource(MATERIALS).description

    assert isinstance(value, str), (
        f"description вернул {type(value).__name__} вместо строки\n"
        "если получилось <bound method ...> — забыт декоратор @property"
    )


def test_folder_description_names_the_folder():
    """Описание папки содержит её имя."""
    from study_assistant.source import FolderSource

    assert FolderSource(MATERIALS).description == f"папка {MATERIALS}"


def test_json_description_names_the_file(catalog_json):
    """Описание файла содержит путь к нему."""
    from study_assistant.source import JsonSource

    assert JsonSource(catalog_json).description == f"файл {catalog_json}"


def test_description_is_read_only():
    """Описание нельзя перезаписать снаружи — у property нет сеттера."""
    from study_assistant.source import FolderSource

    source = FolderSource(MATERIALS)

    with pytest.raises(AttributeError):
        source.description = "что угодно"


# --- источник из папки -------------------------------------------------------


def test_folder_source_loads_all_materials():
    """Из папки читаются все файлы .md."""
    from study_assistant.source import FolderSource

    materials = FolderSource(MATERIALS).load()

    assert len(materials) == len(EXPECTED), (
        f"загружено {len(materials)} материалов вместо {len(EXPECTED)}"
    )


def test_folder_source_returns_material_objects():
    """Источник отдаёт объекты Material, а не словари."""
    from study_assistant.material import Material
    from study_assistant.source import FolderSource

    first = FolderSource(MATERIALS).load()[0]

    assert isinstance(first, Material), (
        f"получен {type(first).__name__} вместо Material\n"
        "load должен возвращать то же, что read_material"
    )


def test_folder_source_keeps_alphabetical_order():
    """Порядок файлов одинаков на любой машине."""
    from study_assistant.source import FolderSource

    names = [material.file for material in FolderSource(MATERIALS).load()]

    assert names == FILES_IN_ORDER, (
        f"порядок файлов: {names}\nпроверьте, что glob обёрнут в sorted()"
    )


def test_folder_source_reads_correct_data():
    """Характеристики материалов совпадают с эталоном."""
    from study_assistant.source import FolderSource

    for material in FolderSource(MATERIALS).load():
        reference = EXPECTED[material.file]
        assert material.title == reference["title"], f"заголовок {material.file}"
        assert material.words == reference["words"], f"слова в {material.file}"


def test_folder_source_accepts_string_path():
    """Папку можно передать строкой, а не только объектом Path."""
    from study_assistant.source import FolderSource

    try:
        materials = FolderSource(str(MATERIALS)).load()
    except AttributeError as error:
        pytest.fail(
            f"источник не принял строку: {error}\n"
            "оберните аргумент в Path(...) прямо в конструкторе — "
            "тогда всё остальное работает одинаково"
        )

    assert len(materials) == len(EXPECTED)


def test_folder_source_reports_missing_folder(tmp_path):
    """Если папки нет — понятная ошибка, а не пустой список."""
    from study_assistant.source import FolderSource

    missing = tmp_path / "nowhere"

    with pytest.raises(FileNotFoundError) as info:
        FolderSource(missing).load()

    assert str(info.value) == f"Папка {missing} не найдена", (
        f"текст ошибки: {info.value!r}\nожидался: 'Папка {missing} не найдена'"
    )


# --- источник из файла JSON --------------------------------------------------


def test_json_source_loads_all_materials(catalog_json):
    """Из файла каталога читаются все записи."""
    from study_assistant.source import JsonSource

    materials = JsonSource(catalog_json).load()

    assert len(materials) == len(EXPECTED), (
        f"загружено {len(materials)} материалов вместо {len(EXPECTED)}"
    )


def test_json_source_returns_material_objects(catalog_json):
    """Словари из файла превращаются в объекты."""
    from study_assistant.material import Material
    from study_assistant.source import JsonSource

    first = JsonSource(catalog_json).load()[0]

    assert isinstance(first, Material), (
        f"получен {type(first).__name__} вместо Material\n"
        "каждый словарь нужно развернуть в объект: Material(**item)"
    )
    assert first.title == EXPECTED[first.file]["title"]


def test_json_source_reads_what_save_catalog_wrote(tmp_path):
    """Что записал save_catalog, то читает JsonSource."""
    from study_assistant.catalog import save_catalog
    from study_assistant.source import FolderSource, JsonSource

    path = tmp_path / "catalog.json"
    save_catalog(FolderSource(MATERIALS).load(), path)

    restored = JsonSource(path).load()

    assert [material.file for material in restored] == FILES_IN_ORDER
    assert sum(material.words for material in restored) == 77


# --- главное: отчёт не зависит от источника ----------------------------------


def test_report_is_identical_for_both_sources(capsys, tmp_path):
    """Подмена источника не меняет отчёт ни на символ.

    Это и есть смысл контракта: код вокруг источника не знает,
    откуда пришли данные, и не должен этого замечать.
    """
    from study_assistant.catalog import print_report, save_catalog
    from study_assistant.source import FolderSource, JsonSource

    path = tmp_path / "catalog.json"
    save_catalog(FolderSource(MATERIALS).load(), path)

    print_report(FolderSource(MATERIALS).load())
    from_folder = capsys.readouterr().out

    print_report(JsonSource(path).load())
    from_json = capsys.readouterr().out

    assert from_folder == from_json, (
        "отчёты из двух источников различаются\n"
        "значит, источники отдают разные данные — сравните их вручную:\n"
        "  print(FolderSource('materials').load()[0])\n"
        "  print(JsonSource('catalog.json').load()[0])"
    )


def test_main_chooses_source_in_one_place():
    """Точка входа работает через источник, а не через build_catalog напрямую."""
    import main
    from study_assistant.source import MaterialSource

    assert hasattr(main, "SOURCE"), (
        "в main.py нет переменной SOURCE\n"
        "источник выбирается одной строкой: SOURCE = FolderSource(MATERIALS_DIR)"
    )
    assert isinstance(main.SOURCE, MaterialSource), (
        f"SOURCE — это {type(main.SOURCE).__name__}, а должен быть источником материалов"
    )
