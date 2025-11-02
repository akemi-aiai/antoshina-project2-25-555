#!/usr/bin/env python3

def create_table(metadata, table_name, columns):
    """
    Создает таблицу в метаданных.

    Args:
        metadata: словарь с метаданными
        table_name: имя таблицы
        columns: список столбцов в формате ['name:str', 'age:int']

    Returns:
        Обновленный словарь metadata
    """
    # Проверяем существование таблицы
    if table_name in metadata:
        raise ValueError(f'Таблица "{table_name}" уже существует.')

    # Проверяем корректность типов и формируем список столбцов
    validated_columns = ["ID:int"]  # Автоматически добавляем ID

    for column in columns:
        if ':' not in column:
            raise ValueError(f'Некорректный формат столбца: {column}')

        col_name, col_type = column.split(':', 1)
        if col_type not in ['int', 'str', 'bool']:
            raise ValueError(f'Неподдерживаемый тип данных: {col_type}')

        validated_columns.append(f"{col_name}:{col_type}")

    # Добавляем таблицу в метаданные
    metadata[table_name] = validated_columns
    return metadata


def drop_table(metadata, table_name):
    """
    Удаляет таблицу из метаданных.

    Args:
        metadata: словарь с метаданными
        table_name: имя таблицы

    Returns:
        Обновленный словарь metadata
    """
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует.')

    del metadata[table_name]
    return metadata


def list_tables(metadata):
    """
    Возвращает список таблиц.

    Args:
        metadata: словарь с метаданными

    Returns:
        Список имен таблиц
    """
    return list(metadata.keys())
