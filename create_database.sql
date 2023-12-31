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

CREATE TABLE conference
(
    id    INTEGER      NOT NULL AUTO_INCREMENT,
    title VARCHAR(128) NOT NULL,
    date  DATETIME     NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE report
(
    id              INTEGER      NOT NULL AUTO_INCREMENT,
    title           VARCHAR(128) NOT NULL,
    annotation      TEXT         NOT NULL,
    text            TEXT         NOT NULL,
    creation_date   DATETIME     NOT NULL DEFAULT now(),
    update_date     DATETIME,
    moderation_flag BOOL         NOT NULL,
    user_id         UUID         NOT NULL,
    conference_id   INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES user (uuid) ON DELETE CASCADE,
    FOREIGN KEY (conference_id) REFERENCES conference (id) ON DELETE CASCADE
);