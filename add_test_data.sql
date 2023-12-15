INSERT INTO user (email, first_name, last_name, patronymic, access_rights)
VALUES ('ivanov@mail.com', 'Ivan', 'Ivanov', 'Ivanovich', 'USER'),
       ('petrov@mail.com', 'Petr', 'Petrov', 'Petrovich', 'ADMIN');

INSERT INTO conference (title, date)
VALUES ('Main Conference', '2023-09-01 12:00:00');

INSERT INTO report (title, annotation, text, moderation_flag, user_id, conference_id)
VALUES ('Some Report', 'Report annotation', 'Report text', 0, 1, 1),
       ('Some Other Report', 'Report annotation', 'Report text', 0, 2, NULL);
