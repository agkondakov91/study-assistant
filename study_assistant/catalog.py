"""Каталог учебных материалов.

Задание: stages/stage-01-catalog/README.md
Проверка: uv run pytest -m stage1
"""

from pathlib import Path

MATERIALS_DIR = Path("materials")
CATALOG_FILE = Path("catalog.json")
EMPTY_TITLE = "(пустой файл)"


def read_material(path):
    """Возвращает описание одного файла материалов.

    Аргументы:
        path — объект Path, путь к файлу .md

    Возвращает словарь ровно с такими ключами:
        "file"   — имя файла с расширением
        "title"  — первая непустая строка; если таких нет — EMPTY_TITLE
        "lines"  — количество непустых строк
        "words"  — количество слов во всём тексте
        "chars"  — количество символов во всём тексте

    Пример для materials/functions.md:
        {
            "file": "functions.md",
            "title": "Функции",
            "lines": 3,
            "words": 15,
            "chars": 112,
        }
    """
    # TODO 1. Прочитайте текст файла: path.read_text(encoding="utf-8")
    # TODO 2. Разбейте на строки методом splitlines()
    # TODO 3. Соберите список непустых строк.
    #         Строка пустая, если line.strip() == ""
    # TODO 4. Заголовок — первая непустая строка,
    #         а если таких нет — EMPTY_TITLE
    # TODO 5. Верните словарь с пятью ключами.
    #         Имя файла: path.name, слова: len(text.split()), символы: len(text)
    raise NotImplementedError("TODO: read_material")


def build_catalog(directory):
    """Собирает каталог по всем файлам .md в папке.

    Аргументы:
        directory — объект Path, папка с материалами

    Возвращает список описаний — по одному на файл,
    в алфавитном порядке имён.

    Если папки не существует — порождает FileNotFoundError
    с текстом: f"Папка {directory} не найдена"
    """
    # TODO 1. Если папки нет (directory.exists() ложно) —
    #         raise FileNotFoundError(f"Папка {directory} не найдена")
    # TODO 2. Заведите пустой список — накопитель
    # TODO 3. Переберите sorted(directory.glob("*.md")).
    #         sorted нужен, иначе порядок будет разным на разных машинах
    # TODO 4. Для каждого файла вызовите read_material
    #         и добавьте результат в накопитель
    # TODO 5. Верните накопитель
    raise NotImplementedError("TODO: build_catalog")


def save_catalog(catalog, path):
    """Записывает каталог в JSON-файл.

    Ничего не возвращает.
    Файл должен быть читаемым человеком: русский текст как есть,
    отступы в два пробела.
    """
    # TODO 1. Откройте файл на запись:
    #         with open(...) as file
    # TODO 2. json.dump(...)
    #         ensure_ascii=False — иначе русский текст станет "Ф..."
    #         indent=2 — иначе всё запишется одной длинной строкой
    raise NotImplementedError("TODO: save_catalog")


def load_catalog(path):
    """Читает каталог из JSON-файла.

    Возвращает то же, что записал save_catalog.

    Ошибки не обрабатывает: отсутствие файла и повреждённый JSON
    должны дойти до вызывающего кода — их ловит main.py.
    """
    # TODO 1. Откройте файл на чтение:
    #         with open(...) as file
    # TODO 2. Верните json.load(file)
    raise NotImplementedError("TODO: load_catalog")


def print_report(catalog):
    """Печатает отчёт по каталогу.

    Ничего не возвращает.

    Формат вывода — ровно такой (отступы в два и четыре пробела):

        Файлов в каталоге: 4

          data_structures.md
            заголовок: Структуры данных
            строк: 5, слов: 36, символов: 250
          empty.md
            заголовок: (пустой файл)
            строк: 0, слов: 0, символов: 0

        Всего слов во всех материалах: 77
    """
    # TODO 1. Напечатайте количество файлов, затем пустую строку
    # TODO 2. Переберите каталог. Для каждого элемента три строки:
    #           два пробела + имя файла
    #           четыре пробела + "заголовок: " + заголовок
    #           четыре пробела + "строк: N, слов: N, символов: N"
    # TODO 3. Напечатайте пустую строку и сумму слов по всем элементам
    raise NotImplementedError("TODO: print_report")
