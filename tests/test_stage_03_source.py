"""Этап 3: источник материалов.

Задание: stages/stage-03-source/README.md
Запуск: uv run pytest -m stage3

Тесты будут дописаны к лекции 11. Разметка ниже — образец для новых
этапов: пока модуля study_assistant/source.py нет, тесты пропускаются
и не мешают работе над текущим этапом.
"""

import pytest

from tests.conftest import stage_not_ready

pytestmark = [
    pytest.mark.stage3,
    pytest.mark.skipif(
        stage_not_ready("study_assistant.source", "FolderSource"),
        reason="этап 3 ещё не начат",
    ),
]


def test_source_returns_materials(materials_dir):
    """FolderSource возвращает список материалов из папки."""
    from study_assistant.source import FolderSource

    assert len(FolderSource(materials_dir).load()) == 4
