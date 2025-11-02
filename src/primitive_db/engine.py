#!/usr/bin/env python3

import prompt
import shlex
from .core import create_table, drop_table, list_tables
from .utils import load_metadata, save_metadata


def show_help():
    """Показывает справку по командам."""
    print("***База данных***")
    print()
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип>"
    " <столбец2:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация")
    print()


def run():
    """Основной цикл программы."""
    show_help()

    while True:
        try:
            user_input = prompt.string("Введите команду: ")
            if not user_input.strip():
                continue

            # Разбиваем ввод на команду и аргументы
            parts = shlex.split(user_input)
            command = parts[0]
            args = parts[1:]

            # Загружаем актуальные метаданные
            metadata = load_metadata()

            if command == "exit":
                print("Выход из программы...")
                break

            elif command == "help":
                show_help()

            elif command == "create_table":
                if len(args) < 2:
                    print("Ошибка: Недостаточно аргументов. " \
                    "Используйте: create_table <имя> <столбец1:тип> ...")
                    continue

                table_name = args[0]
                columns = args[1:]

                try:
                    metadata = create_table(metadata, table_name, columns)
                    save_metadata(metadata)
                    column_list = ", ".join(metadata[table_name])
                    print(
                    f'Таблица "{table_name}" успешно создана '
                    f'со столбцами: {column_list}'
                    )
                except ValueError as e:
                    print(f"Ошибка: {e}")

            elif command == "list_tables":
                tables = list_tables(metadata)
                if tables:
                    for table in tables:
                        print(f"- {table}")
                else:
                    print("Нет созданных таблиц.")

            elif command == "drop_table":
                if len(args) != 1:
                    print("Ошибка: Используйте: drop_table <имя_таблицы>")
                    continue

                table_name = args[0]
                try:
                    metadata = drop_table(metadata, table_name)
                    save_metadata(metadata)
                    print(f'Таблица "{table_name}" успешно удалена.')
                except ValueError as e:
                    print(f"Ошибка: {e}")

            else:
                print(f"Функции '{command}' нет. Попробуйте снова.")

        except Exception as e:
            print(f"Произошла ошибка: {e}. Попробуйте снова.")


def welcome():
    """Старая функция для обратной совместимости."""
    run()
