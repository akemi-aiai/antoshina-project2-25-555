#!/usr/bin/env python3

import prompt
import shlex
from .core import (
    create_table, drop_table, list_tables, insert, select,
    update, delete, get_table_info, format_table_output, get_table_schema
)
from .utils import load_metadata, save_metadata, load_table_data, save_table_data
from .parser import parse_where_condition, parse_set_clause, parse_values
from .decorators import create_cacher
select_cache = create_cacher ()

def show_help():
    """Показывает справку по командам."""
    print("***Операции с данными***")
    print()
    print("Функции:")
    print(
        "<command> insert into <имя_таблицы> values "
        "(<значение1>, <значение2>, ...) - создать запись"
    )
    print(
        "<command> select from <имя_таблицы> where "
        "<столбец> = <значение> - прочитать записи по условию"
    )
    print("<command> select from <имя_таблицы> - прочитать все записи")
    print(
        "<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where "
        "<столбец_условия> = <значение_условия> - обновить запись"
    )
    print(
        "<command> delete from <имя_таблицы> where "
        "<столбец> = <значение> - удалить запись"
    )
    print("<command> info <имя_таблицы> - вывести информацию о таблице")
    print(
        "<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. "
        "- создать таблицу"
    )
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
            command = parts[0].lower()
            args = parts[1:]

            # Загружаем актуальные метаданные
            metadata = load_metadata()

            if command == "exit":
                print("Выход из программы...")
                break

            elif command == "help":
                show_help()

            # CRUD операции
            elif command == "insert":
                if (
                    len(args) < 4
                    or args[0].lower() != "into"
                    or args[2].lower() != "values"
                ):
                    print(
                        "Ошибка: Используйте: insert into <таблица> "
                        "values (<значение1>, <значение2>, ...)"
                    )
                    continue

                table_name = args[1]
                values_str = ' '.join(args[3:])

                try:
                    # Загружаем данные таблицы
                    table_data = load_table_data(table_name)

                    # Парсим значения
                    values = parse_values(values_str)

                    # Вставляем новую запись
                    metadata = load_metadata()
                    new_record = insert(metadata, table_name, values)

                    # Генерируем ID (максимальный ID + 1)
                    if table_data:
                        max_id = max(record.get('ID', 0) for record in table_data)
                        new_record['ID'] = max_id + 1
                    else:
                        new_record['ID'] = 1

                    table_data.append(new_record)
                    save_table_data(table_name, table_data)

                    print(
                        f'Запись с ID={new_record["ID"]} успешно '
                        f'добавлена в таблицу "{table_name}". '
                    )

                except ValueError as e:
                    print(f"Ошибка: {e}")

            elif command == "select":
                if len(args) < 2 or args[0].lower() != "from":
                    print(
                        "Ошибка: Используйте: select from <таблица> "
                        "[where <условие>]"
                        )
                    continue
                table_name = args[1]
                where_clause = None

                # Обрабатываем WHERE если есть
                if len(args) > 2 and args[2].lower() == "where":
                    where_str = ' '.join(args[3:])
                    try:
                        where_clause = parse_where_condition(where_str)
                    except ValueError as e:
                        print(f"Ошибка: {e}")
                        continue

                try:
                    # Загружаем данные таблицы
                    table_data = load_table_data(table_name)
                    metadata = load_metadata()

                    cache_key = f"{table_name}:{str(where_clause)}"

                    def get_selected_data():
                        return select(table_data, where_clause)

                    # Выбираем данные
                    result_data = select_cache(cache_key, get_selected_data)

                    # Форматируем вывод
                    schema = get_table_schema(metadata, table_name)
                    table_output = format_table_output(result_data, schema)
                    print(table_output)

                except ValueError as e:
                    print(f"Ошибка: {e}")

            elif command == "update":
                if (
                    len(args) < 6
                    or args[1].lower() != "set"
                    or "where" not in [arg.lower() for arg in args]
                ):
                    print(
                        "Ошибка: Используйте: update <таблица> set "
                        "<столбец>=<значение> where <условие>"
                    )
                    continue

                table_name = args[0]

                # Находим индексы SET и WHERE
                set_index = args.index("set") if "set" in args else args.index("SET")
                where_index = (
                    args.index("where")
                    if "where" in args
                    else args.index("WHERE")
                )

                set_str = ' '.join(args[set_index+1:where_index])
                where_str = ' '.join(args[where_index+1:])

                try:
                    # Парсим условия
                    set_clause = parse_set_clause(set_str)
                    where_clause = parse_where_condition(where_str)

                    # Загружаем данные таблицы
                    table_data = load_table_data(table_name)
                    metadata = load_metadata()

                    # Обновляем данные
                    updated_data, updated_count = update(
                        table_data,
                        set_clause,
                        where_clause
                    )
                    save_table_data(table_name, updated_data)

                    print(
                        f'Записей в таблице "{table_name}" успешно '
                        f'обновлено: {updated_count}'
                    )

                except ValueError as e:
                    print(f"Ошибка: {e}")

            elif command == "delete":
                if (
                    len(args) < 3
                    or args[0].lower() != "from"
                    or args[2].lower() != "where"
                ):
                    print(
                        "Ошибка: Используйте: delete from <таблица> "
                        "where <условие>"
                    )
                    continue

                table_name = args[1]
                where_str = ' '.join(args[3:])

                try:
                    # Парсим условие
                    where_clause = parse_where_condition(where_str)

                    # Загружаем данные таблицы
                    table_data = load_table_data(table_name)

                    # Удаляем данные
                    remaining_data, deleted_count = delete(table_data, where_clause)
                    save_table_data(table_name, remaining_data)

                    print(f'Записей удалено из таблицы "{table_name}": {deleted_count}')

                except ValueError as e:
                    print(f"Ошибка: {e}")

            elif command == "info":
                if len(args) != 1:
                    print("Ошибка: Используйте: info <имя_таблицы>")
                    continue

                table_name = args[0]

                try:
                    metadata = load_metadata()
                    table_data = load_table_data(table_name)
                    info = get_table_info(metadata, table_data, table_name)
                    print(info)

                except ValueError as e:
                    print(f"Ошибка: {e}")

            # Команды управления таблицами (из предыдущей версии)
            elif command == "create_table":
                if len(args) < 2:
                    print(
                        "Ошибка: Недостаточно аргументов. " \
                        "Используйте: create_table <имя> <столбец1:тип> ..."
                    )
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
