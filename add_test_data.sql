INSERT INTO user (uuid, email, first_name, last_name, patronymic, access_rights)
VALUES ('cd636f16-7e12-43f7-b229-e7c685755b2c', 'ivanov@mail.com', 'Ivan', 'Ivanov', 'Ivanovich', 'USER'),
       ('beec10a0-15ca-4e29-868c-a65035ef8036', 'petrov@mail.com', 'Petr', 'Petrov', 'Petrovich', 'ADMIN');

INSERT INTO conference (title, date)
VALUES ('Main Conference', '2023-09-01 12:00:00');

INSERT INTO report (title, annotation, text, moderation_flag, user_uuid, conference_id)
VALUES ('Some Report', 'Report annotation', 'Report text', 0, 'cd636f16-7e12-43f7-b229-e7c685755b2c', 1),
       ('Some Other Report', 'Report annotation', 'Report text', 0, 'beec10a0-15ca-4e29-868c-a65035ef8036', NULL);
