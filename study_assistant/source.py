"""Источники учебных материалов.

Этот файл понадобится на ЭТАПЕ 3.
Задание: stages/stage-03-source/README.md
Проверка: uv run pytest -m stage3

Идея этапа: программа перестаёт знать, откуда берутся материалы.
Она знает только контракт — «источник умеет отдать список материалов».
Реализаций контракта две: папка с файлами .md и один файл JSON.
"""

from abc import ABC, abstractmethod

# TODO 0. Допишите импорты — они понадобятся в методах ниже:
#           from pathlib import Path
#           from study_assistant.catalog import build_catalog, load_catalog
#           from study_assistant.material import Material
#         Заранее их не ставим: ruff справедливо ругается на импорт,
#         которым никто не пользуется.


class MaterialSource(ABC):
    """Контракт источника учебных материалов.

    Этот класс ничего не делает — он описывает требования.
    Объект от него создать нельзя, и от наследника, реализовавшего
    не все обязательные члены, тоже нельзя.

    Менять этот класс не нужно: он задан заданием.
    """

    @property
    @abstractmethod
    def description(self):
        """Возвращает описание источника для отчёта, строка."""

    @abstractmethod
    def load(self):
        """Возвращает список объектов Material."""


class FolderSource(MaterialSource):
    """Материалы из папки с файлами .md."""

    def __init__(self, directory):
        """Запоминает папку с материалами."""
        # TODO 1. Сохраните путь во внутреннем атрибуте: self._directory
        #         Обязательно оберните в Path(...): в источник могут передать
        #         обычную строку, а метод .glob() есть только у Path.
        #         Подчёркивание в имени означает «внутреннее, снаружи не трогать».
        raise NotImplementedError("TODO этапа 3: FolderSource.__init__")

    @property
    def description(self):
        """Возвращает описание источника для отчёта."""
        # TODO 2. Верните строку вида "папка materials".
        #         Декоратор @property уже стоит — снаружи к описанию
        #         обращаются без скобок: source.description
        raise NotImplementedError("TODO этапа 3: FolderSource.description")

    def load(self):
        """Читает все файлы .md и возвращает список материалов."""
        # TODO 3. Верните build_catalog(self._directory) — одна строка.
        #         В лекции мы писали здесь цикл по glob целиком, чтобы видеть
        #         устройство источника от начала до конца. В проекте такой цикл
        #         уже написан — это build_catalog с первого этапа. Дублировать
        #         его не нужно: источник просто пользуется готовой функцией.
        #         Проверку «папки нет» build_catalog тоже делает сама.
        raise NotImplementedError("TODO этапа 3: FolderSource.load")


class JsonSource(MaterialSource):
    """Материалы из одного файла JSON — из того, что записал save_catalog."""

    def __init__(self, path):
        """Запоминает путь к файлу каталога."""
        # TODO 4. Сохраните путь во внутреннем атрибуте: self._path
        raise NotImplementedError("TODO этапа 3: JsonSource.__init__")

    @property
    def description(self):
        """Возвращает описание источника для отчёта."""
        # TODO 5. Верните строку вида "файл catalog.json"
        raise NotImplementedError("TODO этапа 3: JsonSource.description")

    def load(self):
        """Читает файл каталога и возвращает список материалов."""
        # TODO 6. Прочитайте файл функцией load_catalog — она вернёт список
        #         словарей, ровно тех, что записал save_catalog. Открывать
        #         файл руками не нужно, эта функция написана на первом этапе.
        # TODO 7. Каждый словарь превратите в объект: Material(**item)
        #         Две звёздочки разворачивают словарь в именованные аргументы:
        #         Material(file="...", title="...", lines=3, ...).
        #         Ключи словаря совпадают с именами параметров __init__ —
        #         это не совпадение, так задуман to_dict().
        raise NotImplementedError("TODO этапа 3: JsonSource.load")
