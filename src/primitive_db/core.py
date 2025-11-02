#!/usr/bin/env python3

from prettytable import PrettyTable
from .decorators import handle_db_errors, confirm_action, log_time
from .constants import(
    ERROR_TABLE_EXISTS, ERROR_COLUMN_FORMAT,
    ERROR_DATA_TYPE,
)

@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создает таблицу в метаданных."""
    if table_name in metadata:
        raise ValueError(ERROR_COLUMN_FORMAT.format(table_name))

    validated_columns = ["ID:int"]

    for column in columns:
        if ':' not in column:
            raise ValueError(ERROR_TABLE_EXISTS.format(column))

        col_name, col_type = column.split(':', 1)
        if col_type not in ['int', 'str', 'bool']:
            raise ValueError(ERROR_DATA_TYPE.format(col_type))

        validated_columns.append(f"{col_name}:{col_type}")

    metadata[table_name] = validated_columns
    return metadata

@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных."""
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует.')

    del metadata[table_name]
    return metadata

@handle_db_errors
def list_tables(metadata):
    """Возвращает список таблиц."""
    return list(metadata.keys())

@handle_db_errors
def get_table_schema(metadata, table_name):
    """Возвращает схему таблицы в виде списка кортежей (имя, тип)."""
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует.')

    schema = []
    for column_def in metadata[table_name]:
        name, type_ = column_def.split(':')
        schema.append((name, type_))

    return schema

@handle_db_errors
def validate_data_types(schema, values):
    """Проверяет соответствие значений типам данных схемы."""
    # Пропускаем ID (первый столбец)
    for (col_name, col_type), value in zip(schema[1:], values):
        if col_type == 'int' and not isinstance(value, int):
            raise ValueError(f'Столбец "{col_name}" должен быть int, получено: {value}')
        elif col_type == 'str' and not isinstance(value, str):
            raise ValueError(f'Столбец "{col_name}" должен быть str, получено: {value}')
        elif col_type == 'bool' and not isinstance(value, bool):
            raise ValueError(
                f'Столбец "{col_name}" должен быть bool, '
                f'получено: {value}'
            )

@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    """Добавляет новую запись в таблицу."""
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует.')

    schema = get_table_schema(metadata, table_name)

    # Проверяем количество значений (без ID)
    if len(values) != len(schema) - 1:
        raise ValueError(f'Ожидается {len(schema)-1} значений, получено {len(values)}')

    # Валидируем типы данных
    validate_data_types(schema, values)

    # Создаем новую запись
    new_id = 1

    record = {'ID': new_id}
    for (col_name, _), value in zip(schema[1:], values):
        record[col_name] = value

    return record

@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    """Выбирает записи из таблицы с опциональным условием WHERE."""
    if where_clause is None:
        return table_data

    filtered_data = []
    for record in table_data:
        match = True
        for column, value in where_clause.items():
            if record.get(column) != value:
                match = False
                break
        if match:
            filtered_data.append(record)

    return filtered_data

@handle_db_errors
def update(table_data, set_clause, where_clause):
    """Обновляет записи в таблице."""
    updated_count = 0

    for record in table_data:
        match = True
        for column, value in where_clause.items():
            if record.get(column) != value:
                match = False
                break

        if match:
            for column, new_value in set_clause.items():
                record[column] = new_value
            updated_count += 1

    return table_data, updated_count

@handle_db_errors
@confirm_action("удаление записей")
def delete(table_data, where_clause):
    """Удаляет записи из таблицы."""
    if where_clause is None:
        return [], len(table_data)

    remaining_data = []
    deleted_count = 0

    for record in table_data:
        match = True
        for column, value in where_clause.items():
            if record.get(column) != value:
                match = False
                break

        if not match:
            remaining_data.append(record)
        else:
            deleted_count += 1

    return remaining_data, deleted_count

@handle_db_errors
def format_table_output(data, schema):
    """Форматирует данные для вывода в виде таблицы."""
    if not data:
        return "Нет данных для отображения."

    table = PrettyTable()
    table.field_names = [col_name for col_name, _ in schema]

    for record in data:
        row = []
        for col_name, _ in schema:
            row.append(record.get(col_name, ''))
        table.add_row(row)

    return table

@handle_db_errors
def get_table_info(metadata, table_data, table_name):
    """Возвращает информацию о таблице."""
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует.')

    schema = get_table_schema(metadata, table_name)
    column_info = ', '.join(metadata[table_name])
    record_count = len(table_data)

    return (
        f"Таблица: {table_name}\nСтолбцы: {column_info}\n"
        f"Количество записей: {record_count}\nСхема: {schema}"
    )
