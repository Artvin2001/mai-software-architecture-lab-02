-- Создание схемы базы данных для второй ноды
-- (только таблица пользователей)

CREATE TABLE user
(
    uuid          UUID                              NOT NULL,
    email         VARCHAR(64)                       NOT NULL,
    first_name    VARCHAR(64)                       NOT NULL,
    last_name     VARCHAR(64)                       NOT NULL,
    patronymic    VARCHAR(64),
    access_rights ENUM ('ADMIN','USER','MODERATOR') NOT NULL,
    PRIMARY KEY (uuid),
    UNIQUE (email)
);
