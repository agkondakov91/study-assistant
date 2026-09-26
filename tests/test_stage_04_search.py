"""Этап 4: поиск по материалам.

Задание: stages/stage-04-search/README.md
Запуск: uv run pytest -m stage4

Тесты будут дописаны к соответствующей лекции.
"""

import pytest

from tests.conftest import stage_not_ready

pytestmark = [
    pytest.mark.stage4,
    pytest.mark.skipif(
        stage_not_ready("study_assistant.search", "SearchIndex"),
        reason="этап 4 ещё не начат",
    ),
]


def test_placeholder():
    """Место для тестов этапа 4."""
    from study_assistant.search import SearchIndex

    assert SearchIndex is not None
