DROP TABLE IF EXISTS article;

CREATE TABLE IF NOT EXISTS article
(
    id       varchar(250) NOT NULL,
    language varchar(10)  NOT NULL,
    title    TEXT         NOT NULL,
    url      TEXT         NOT NULL,
    PRIMARY KEY (id, language)
);