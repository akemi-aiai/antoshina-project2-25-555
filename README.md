## Проект представляет собой простую систему работы с базой данных на Python. Позволяет создавать таблицы, добавлять, обновлять, удалять и читать записи через командную строку.

## Установка

Рекомендуется использовать [Poetry](https://python-poetry.org/) для управления зависимостями.

Склонируйте репозиторий:
   git clone https://github.com/akemi-aiai/antoshina-project2-25-555.git
   cd antoshina-project2-25-555

## Установите зависимости:
poetry install
или через make:
make install

## Запуск
make project


## Возможности

- Создание и удаление таблиц
- Добавление, чтение, обновление и удаление данных
- Поддержка типов данных: int, str, bool
- Автоматическая генерация ID
- Красивый табличный вывод
- Подтверждение опасных операций
- Кэширование запросов
- Логирование времени выполнения

## Демонстрация работы проекта

asciicast https://asciinema.org/a/Z5LxhUzXS2bDU7f25Yr30sSjv


### Команды для работы с данными:

- insert into <таблица> values (<значение1>, <значение2>, ...) - добавить запись
- select from <таблица> - показать все записи
- select from <таблица> where <условие> - показать записи по условию
- update <таблица> set <столбец>=<значение> where <условие> - обновить записи
- delete from <таблица> where <условие> - удалить записи
- info <таблица> - информация о таблице

### Пример использования:

1) create_table users name:str age:int is_active:bool
2) insert into users values ("lock", 28, true)
3) select from users
4) update users set age = 28 where name = "lock"
5) delete from users where age = 28
6) info users
