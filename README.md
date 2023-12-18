# mai-software-architecture-lab-02

## Лабораторная работа № 4. Кеширование

Для создания структуры базы данных необходимо выполнить SQL-скрипт `create_database_1.sql` (для 
первой ноды) и `create_database_2.sql` (для второй ноды) или Python-скрипт 
`user_service/database.py`.

Для наполнения базы данных тестовыми данными необходимо выполнить SQL-скрипт `add_test_data.sql`
(для первой ноды).

OpenAPI для каждого сервиса доступен в файле `index.yaml` в директории соответствующего сервиса,
а также во время развертывания по адресу `/` (например, по адресу `http://localhost:8001/` для
сервиса пользователей).

### Шардинг

Для шардинга использовался подход "умный клиент". Разделение на ноды производится путем получения
остатка от деления на два UUID пользователя. В работе не использовался ProxySQL, так как в данном
случае использование регулярного выражения в SQL-запросе было нецелесообразно. Кроме того,
использование "умного клиент" позволяет в будущем более гибко настроить шардинг и избежать проблемы
единой точки отказа в виде сервиса ProxySQL (или аналогичного).

### Кеширование

Кеширование реализовано для конечной точки `/users/{user_uuid}`. Реализован паттерн "сквозное 
чтение" (проверяется наличие записи в кеше, а уже затем, при необходимости выполняется запрос в БД).
Для конечных точек, изменяющих пользователя, то есть POST, PUT и DELETE реализована "сквозная
запись" (выполняется кеширование данных и запись в БД). Время жизни кеша установлено на 60 секунд.
Для других конечных точек кеширование не выполняется.
