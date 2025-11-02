## Управление таблицами

### Команды:

- `create_table <имя> <столбец1:тип> ...` - создать таблицу
- `list_tables` - показать все таблицы  
- `drop_table <имя>` - удалить таблицу
- `help` - справка
- `exit` - выход

### Пример использования:

```bash
project

Введите команду: create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool

Введите команду: list_tables
- users

Введите команду: drop_table users
Таблица "users" успешно удалена.