CREATE TABLE user
(
    id            INTEGER                           NOT NULL AUTO_INCREMENT,
    email         VARCHAR(64)                       NOT NULL,
    first_name    VARCHAR(64)                       NOT NULL,
    last_name     VARCHAR(64)                       NOT NULL,
    patronymic    VARCHAR(64),
    access_rights ENUM ('ADMIN','USER','MODERATOR') NOT NULL,
    PRIMARY KEY (id),
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
    user_id         INTEGER      NOT NULL,
    conference_id   INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (conference_id) REFERENCES conference (id)
);
