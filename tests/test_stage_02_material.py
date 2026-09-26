"""Этап 2: материал как объект.

Задание: stages/stage-02-material/README.md
Запуск: uv run pytest -m stage2

Тесты включатся сами, как только вы напишете Material.__init__.
"""

import json

import pytest

from tests.conftest import stage_not_ready

pytestmark = [
    pytest.mark.stage2,
    pytest.mark.skipif(
        stage_not_ready("study_assistant.material", "Material", "x", "y", 0, 0, 0),
        reason="этап 2 ещё не начат — напишите Material.__init__, и тесты включатся",
    ),
]

SAMPLE_DICT = {
    "file": "functions.md",
    "title": "Функции",
    "lines": 3,
    "words": 15,
    "chars": 112,
}


def test_object_attributes(sample_material):
    """__init__ сохраняет все пять значений как атрибуты."""
    for attr, value in SAMPLE_DICT.items():
        assert hasattr(sample_material, attr), (
            f"у объекта нет атрибута {attr!r} — "
            "проверьте, что написали self.имя = имя, а не просто имя = имя"
        )
        assert getattr(sample_material, attr) == value


def test_is_empty_false_for_filled(sample_material):
    """Материал с тремя строками не считается пустым."""
    assert sample_material.is_empty() is False


def test_is_empty_true_for_blank(blank_material):
    """Материал без непустых строк считается пустым."""
    assert blank_material.is_empty() is True


def test_summary_format(sample_material):
    """Сводка собирается в точном формате."""
    assert sample_material.summary() == "строк: 3, слов: 15, символов: 112"


def test_to_dict_keys(sample_material):
    """to_dict возвращает словарь с пятью ожидаемыми ключами."""
    result = sample_material.to_dict()

    assert isinstance(result, dict), f"ожидался словарь, получено {type(result).__name__}"
    assert result == SAMPLE_DICT


def test_object_is_not_json_serializable(sample_material):
    """Объект нельзя сохранить в JSON — именно поэтому нужен to_dict."""
    with pytest.raises(TypeError):
        json.dumps([sample_material])

    assert "functions.md" in json.dumps([sample_material.to_dict()], ensure_ascii=False)


def test_repr_is_readable(sample_material):
    """__repr__ даёт человекочитаемую строку, а не адрес в памяти."""
    text = repr(sample_material)

    assert "object at 0x" not in text, (
        "__repr__ не написан — объект печатается как адрес в памяти, "
        "и отладить список таких объектов невозможно"
    )
    assert text == "Material('functions.md', слов=15)"


def test_empty_title_moved_to_material():
    """Константа EMPTY_TITLE относится к материалу, а не к каталогу."""
    import study_assistant.material as material_module

    assert hasattr(material_module, "EMPTY_TITLE"), (
        "перенесите константу EMPTY_TITLE из catalog.py в material.py — она относится к материалу"
    )
    assert material_module.EMPTY_TITLE == "(пустой файл)"


def test_read_material_returns_object(functions_md):
    """read_material отдаёт Material, а не словарь."""
    from study_assistant.catalog import read_material
    from study_assistant.material import Material

    result = read_material(functions_md)

    assert not isinstance(result, dict), (
        "функция всё ещё возвращает словарь — нужно вернуть объект Material"
    )
    assert isinstance(result, Material)
    assert result.title == "Функции"


def test_catalog_contains_objects(materials_dir):
    """build_catalog отдаёт список объектов Material."""
    from study_assistant.catalog import build_catalog
    from study_assistant.material import Material

    for item in build_catalog(materials_dir):
        assert isinstance(item, Material), (
            f"в списке должны быть объекты Material, найден {type(item).__name__}"
        )


def test_saves_objects_as_json(tmp_path, materials_dir):
    """save_catalog превращает объекты в словари перед записью."""
    from study_assistant.catalog import build_catalog, load_catalog, save_catalog

    path = tmp_path / "catalog.json"
    catalog = build_catalog(materials_dir)

    try:
        save_catalog(catalog, path)
    except TypeError as error:
        if "not JSON serializable" in str(error):
            pytest.fail(
                f"{error}\n"
                "json.dump не умеет сохранять объекты — "
                "перед записью нужно вызвать to_dict() у каждого материала"
            )
        raise

    assert load_catalog(path) == [item.to_dict() for item in catalog]


def test_report_uses_summary_method(capsys, materials_dir):
    """print_report берёт сводку из метода, а не собирает её заново."""
    from study_assistant.catalog import build_catalog, print_report
    from study_assistant.material import Material

    calls = []
    original = Material.summary

    def counting_summary(self):
        calls.append(self.file)
        return original(self)

    Material.summary = counting_summary
    try:
        print_report(build_catalog(materials_dir))
    finally:
        Material.summary = original

    capsys.readouterr()

    assert len(calls) == 4, (
        "summary() вызван не для каждого материала — "
        "строку со счётчиками не нужно собирать в print_report заново"
    )
