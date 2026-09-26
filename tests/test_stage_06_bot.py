"""Этап 6: бот и оценка качества.

Задание: stages/stage-06-bot/README.md
Запуск: uv run pytest -m stage6

Тесты будут дописаны к соответствующей лекции.
"""

import pytest

from tests.conftest import stage_not_ready

pytestmark = [
    pytest.mark.stage6,
    pytest.mark.skipif(
        stage_not_ready("study_assistant.bot", "Bot"),
        reason="этап 6 ещё не начат",
    ),
]


def test_placeholder():
    """Место для тестов этапа 6."""
    from study_assistant.bot import Bot

    assert Bot is not None
