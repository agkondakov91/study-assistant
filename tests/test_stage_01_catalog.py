"""Этап 1: каталог учебных материалов.

Задание: stages/stage-01-catalog/README.md
Запуск только этих тестов: uv run pytest -m stage1

Внимание: на этапе 2 контракт read_material меняется — она начинает
возвращать объект Material вместо словаря. Тесты, помеченные
stage1_dict, после этого перестают быть актуальными: удалите их,
когда перейдёте к этапу 2. Это нормальная инженерная ситуация —
изменение контракта требует изменения тестов.
"""

import json

import pytest

from tests.conftest import EXPECTED, FILES_IN_ORDER

pytestmark = pytest.mark.stage1


def test_reads_regular_file(functions_md):
    """read_material считает строки, слова и символы верно."""
    from study_assistant.catalog import read_material

    result = read_material(functions_md)
    expected = EXPECTED["functions.md"]

    assert result["title"] == expected["title"]
    assert result["lines"] == expected["lines"], (
        "lines считает только непустые строки — "
        "в файлах материалов есть пустые строки внутри текста"
    )
    assert result["words"] == expected["words"]
    assert result["chars"] == expected["chars"], "chars считает все символы, включая переводы строк"


def test_reads_empty_file(empty_md):
    """Пустой файл не ломает программу и получает особый заголовок."""
    from study_assistant.catalog import EMPTY_TITLE, read_material

    result = read_material(empty_md)

    assert result["title"] == EMPTY_TITLE
    assert result["lines"] == 0
    assert result["words"] == 0
    assert result["chars"] == 0


def test_catalog_collects_all_files(materials_dir):
    """build_catalog находит все .md файлы папки."""
    from study_assistant.catalog import build_catalog

    catalog = build_catalog(materials_dir)

    assert len(catalog) == len(FILES_IN_ORDER)
    assert [item["file"] for item in catalog] == FILES_IN_ORDER


def test_missing_folder_raises_error(tmp_path):
    """build_catalog сообщает о проблеме через исключение, а не печатью."""
    from study_assistant.catalog import build_catalog

    missing = tmp_path / "нет-такой-папки"

    with pytest.raises(FileNotFoundError):
        build_catalog(missing)


def test_json_round_trip(tmp_path, materials_dir):
    """Данные переживают запись в файл и чтение обратно."""
    from study_assistant.catalog import build_catalog, load_catalog, save_catalog

    catalog = build_catalog(materials_dir)
    path = tmp_path / "catalog.json"

    save_catalog(catalog, path)
    assert path.exists(), "save_catalog не создала файл"

    loaded = load_catalog(path)

    assert loaded == catalog, "после записи и чтения данные изменились"


def test_json_is_human_readable(tmp_path, materials_dir):
    """В файле русский текст и отступы, а не коды и одна строка."""
    from study_assistant.catalog import build_catalog, save_catalog

    path = tmp_path / "catalog.json"
    save_catalog(build_catalog(materials_dir), path)
    raw = path.read_text(encoding="utf-8")

    assert "\\u0424" not in raw, "русский текст записан кодами — нужен ensure_ascii=False"
    assert "\n" in raw.strip(), "файл записан одной строкой — нужен indent=2"


def test_broken_json_raises_error(tmp_path):
    """load_catalog не скрывает повреждение файла."""
    from study_assistant.catalog import load_catalog

    path = tmp_path / "broken.json"
    path.write_text("{ это не json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        load_catalog(path)
