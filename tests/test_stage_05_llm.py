"""Этап 5: запросы к модели.

Задание: stages/stage-05-llm/README.md
Запуск: uv run pytest -m stage5

Тесты будут дописаны к соответствующей лекции.
"""

import pytest

from tests.conftest import stage_not_ready

pytestmark = [
    pytest.mark.stage5,
    pytest.mark.skipif(
        stage_not_ready("study_assistant.llm", "ModelClient"),
        reason="этап 5 ещё не начат",
    ),
]


def test_placeholder():
    """Место для тестов этапа 5."""
    from study_assistant.llm import ModelClient

    assert ModelClient is not None
