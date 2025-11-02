#!/usr/bin/env python3

# Файлы и пути
META_FILE = "db_meta.json"
DATA_DIR = "data"

# Поддерживаемые типы данных
VALID_TYPES = ["int", "str", "bool"]

# Сообщения
ERROR_TABLE_EXISTS = 'Таблица "{}" уже существует.'
ERROR_TABLE_NOT_FOUND = 'Таблица "{}" не существует.'
ERROR_COLUMN_FORMAT = 'Некорректный формат столбца: {}'
ERROR_DATA_TYPE = 'Неподдерживаемый тип данных: {}'
ERROR_WHERE_FORMAT = "Некорректный формат условия WHERE"
ERROR_SET_FORMAT = "Некорректный формат условия SET"

# Команды
EXIT_COMMAND = "exit"
HELP_COMMAND = "help"
CREATE_TABLE_COMMAND = "create_table"
DROP_TABLE_COMMAND = "drop_table"
LIST_TABLES_COMMAND = "list_tables"
INSERT_COMMAND = "insert"
SELECT_COMMAND = "select"
UPDATE_COMMAND = "update"
DELETE_COMMAND = "delete"
INFO_COMMAND = "info"
