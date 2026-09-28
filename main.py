"""Точка входа: собирает каталог и печатает отчёт.

До третьего этапа этот файл готов — менять его не нужно.
На этапе 3 он переписывается на работу через источник материалов:
stages/stage-03-source/README.md
"""

import json

from study_assistant.catalog import (
    CATALOG_FILE,
    MATERIALS_DIR,
    build_catalog,
    load_catalog,
    print_report,
    save_catalog,
)


def main():
    """Собирает каталог, сохраняет его, проверяет чтение и печатает отчёт."""
    try:
        catalog = build_catalog(MATERIALS_DIR)
    except FileNotFoundError as error:
        print(f"Ошибка: {error}")
        return

    save_catalog(catalog, CATALOG_FILE)
    print(f"Каталог сохранён в {CATALOG_FILE}")
    print()

    try:
        load_catalog(CATALOG_FILE)
    except json.JSONDecodeError as error:
        print(f"Файл каталога повреждён: {error}")
        return

    print_report(catalog)


if __name__ == "__main__":
    main()
