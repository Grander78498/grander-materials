CREATE DATABASE music_label;
\c music_label

CREATE TABLE musician (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR (100) NOT NULL,
    country VARCHAR (100) NOT NULL,
    birth_date DATE
);
CREATE TABLE music_group (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR (100) NOT NULL UNIQUE,
    country VARCHAR (100) NOT NULL,
    creation_date DATE
);
CREATE TABLE performer (
    id BIGSERIAL PRIMARY KEY,
    musician_id BIGINT REFERENCES musician(id) ON DELETE CASCADE,
    group_id BIGINT REFERENCES music_group(id) ON DELETE CASCADE,
    UNIQUE (musician_id, group_id)
);
CREATE TABLE group_musician (
    group_id BIGINT REFERENCES music_group(id) ON DELETE CASCADE NOT NULL,
    musician_id BIGINT REFERENCES musician(id) ON DELETE CASCADE NOT NULL,
    PRIMARY KEY (group_id, musician_id)
);
CREATE TABLE producer (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR (100) NOT NULL,
    country VARCHAR (100) NOT NULL,
    birth_date DATE
);
CREATE TABLE release_type (
    id SMALLSERIAL PRIMARY KEY,
    type VARCHAR (30) UNIQUE
);
CREATE TABLE album (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR (100) NOT NULL,
    release_date DATE NOT NULL,
    release_type_id SMALLINT REFERENCES release_type(id) ON DELETE RESTRICT NOT NULL
);
CREATE TABLE album_performer (
    album_id BIGINT REFERENCES album (id) ON DELETE CASCADE NOT NULL,
    performer_id BIGINT REFERENCES performer (id) ON DELETE CASCADE NOT NULL,
    PRIMARY KEY (album_id, performer_id)
);
CREATE TABLE producer_album (
    producer_id BIGINT REFERENCES producer (id) ON DELETE CASCADE NOT NULL,
    album_id BIGINT REFERENCES album (id) ON DELETE CASCADE NOT NULL,
    PRIMARY KEY (producer_id, album_id)
);
CREATE TABLE song (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR (100) NOT NULL,
    duration INTERVAL NOT NULL,
    album_id BIGINT REFERENCES album (id) ON DELETE SET NULL
);
CREATE TABLE song_performer (
    song_id BIGINT REFERENCES song (id) ON DELETE CASCADE NOT NULL,
    performer_id BIGINT REFERENCES performer (id) ON DELETE CASCADE NOT NULL,
    PRIMARY KEY (song_id, performer_id)
);
CREATE TABLE single (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR (100) NOT NULL,
    release_date DATE NOT NULL
);
CREATE TABLE single_song (
    single_id BIGINT REFERENCES single (id) ON DELETE CASCADE NOT NULL,
    song_id BIGINT REFERENCES song (id) ON DELETE CASCADE NOT NULL,
    PRIMARY KEY (single_id, song_id)
);
CREATE TABLE producer_song (
    producer_id BIGINT REFERENCES producer (id) ON DELETE CASCADE NOT NULL,
    song_id BIGINT REFERENCES song (id) ON DELETE CASCADE NOT NULL,
    PRIMARY KEY (producer_id, song_id)
);


INSERT INTO music_group (name, country, creation_date) VALUES 
    ('Queens Of The Stone Age', 'USA', '1996-01-01'),
    ('Kyuss', 'USA', '1987-01-01'),
    ('Pink Floyd', 'Great Britain', '1965-01-01'),
    ('Radiohead', 'Great Britain', '1985-01-01'),
    ('Kids See Ghosts', 'USA', '2018-01-01');

INSERT INTO musician (name, country, birth_date) VALUES
    ('Josh Homme', 'USA', '1973-05-17'),
    ('Dave Grohl', 'USA', '1969-01-14'),
    ('Nick Oliveri', 'USA', '1971-10-21'),
    ('Mark Lanegan', 'USA', '1964-11-25'),
    ('Brant Bjork', 'USA', '1973-03-19'),
    ('John Garcia', 'USA', '1970-09-04'),
    ('David Gilmour', 'Great Britain', '1946-03-06'),
    ('Roger Waters', 'Great Britain', '1943-09-06'),
    ('Thom Yorke', 'Great Britain', '1968-10-07'),
    ('Colin Greenwood', 'Great Britain', '1969-06-26'),
    ('Kanye West', 'USA', '1977-06-08'),
    ('JAY-Z', 'USA', '1969-12-04'),
    ('Frank Ocean', 'USA', '1987-10-28'),
    ('The-Dream', 'USA', '1977-09-20'),
    ('Pusha T', 'USA', '1977-05-13'),
    ('Kid Cudi', 'USA', '1984-01-30'),
    ('Raekwon', 'USA', '1970-01-12');

INSERT INTO performer (musician_id, group_id) VALUES
    (NULL, 1),
    (NULL, 2),
    (NULL, 3),
    (NULL, 4),
    (NULL, 5),
    (11, NULL),
    (12, NULL),
    (13, NULL),
    (14, NULL),
    (15, NULL),
    (16, NULL),
    (17, NULL);

INSERT INTO group_musician (group_id, musician_id) VALUES
    (1, 1), (1, 2), (1, 3), (1, 4),
    (2, 1), (2, 3), (2, 5), (2, 6),
    (3, 7), (3, 8),
    (4, 9), (4, 10),
    (5, 11), (5, 16);

INSERT INTO release_type (type) VALUES ('LP'), ('EP'), ('Live'), ('Compilation');


INSERT INTO album (name, release_date, release_type_id) VALUES
    ('...Like Clockwork', '2013-06-03', 1),
    ('Songs For The Deaf', '2002-08-27', 1),
    ('Welcome To Sky Valley', '1994-06-28', 1),
    ('Wish You Were Here', '1975-09-12', 1),
    ('OK Computer', '1997-05-21', 1),
    ('Watch The Throne', '2011-08-08', 1),
    ('Kids See Ghosts', '2018-06-08', 2),
    ('My Beautiful Dark Twisted Fantasy', '2010-11-22', 1),
    ('PULSE', '1995-05-28', 3);

INSERT INTO album_performer (album_id, performer_id) VALUES
    (1, 1), (2, 1),
    (3, 2),
    (4, 3),
    (5, 4),
    (6, 6), (6, 7),
    (7, 5), (7, 6), (7, 11),
    (8, 6),
    (9, 3);

INSERT INTO producer (name, country, birth_date) VALUES
    ('Josh Homme', 'USA', '1973-05-17'),
    ('Eric Valentine', 'USA', '1968-03-07'),
    ('Adam Kasper', 'USA', '1962-12-01'),
    ('Chris Goss', 'USA', '1959-08-17'),
    ('Roger Waters', 'Great Britain', '1943-09-06'),
    ('David Gilmour', 'Great Britain', '1946-03-06'),
    ('Nigel Godrich', 'Great Britain', '1971-02-28'),
    ('Kanye West', 'USA', '1977-06-08'),
    ('Kid Cudi', 'USA', '1984-01-30'),
    ('Mike Dean', 'USA', '1965-03-01');

INSERT INTO producer_album (producer_id, album_id) VALUES
    (1, 1),
    (1, 2), (2, 2), (3, 2),
    (4, 3),
    (5, 4), (6, 4),
    (7, 5),
    (8, 6), (10, 6),
    (8, 7), (9, 7), (10, 7),
    (8, 8), (10, 8),
    (6, 9);

INSERT INTO song (name, duration, album_id) VALUES
    ('I Sat By The Ocean', '00:03:55', 1),
    ('My God Is The Sun', '00:03:55', 1),
    ('No One Knows', '00:04:38', 2),
    ('A Song For The Dead', '00:05:52', 2),
    ('Gardenia', '00:06:54', 3),
    ('Space Cadet', '00:07:02', 3),
    ('Shine on You Crazy Diamond (Parts I-V)', '00:13:30', 4),
    ('Welcome To The Machine', '00:07:31', 4),
    ('Have A Cigar', '00:05:08', 4),
    ('Wish You Were Here', '00:05:40', 4),
    ('Shine on You Crazy Diamond (Parts VI-IX)', '00:12:31', 4),
    ('Paranoid Android', '00:06:23', 5),
    ('Let Down', '00:04:59', 5),
    ('Pearly', '00:03:33', NULL),
    ('No Church In The Wild', '00:04:32', 6),
    ('N****s In Paris', '00:03:39', 6),
    ('Gorgeous', '00:05:57', 8),
    ('POWER', '00:04:52', 8),
    ('Runaway', '00:09:07', 8),
    ('Feel The Love', '00:02:33', 7),
    ('Cudi Montage', '00:03:17', 7),
    ('Wish You Were Here - Live', '00:06:35', 9);

INSERT INTO song_performer (song_id, performer_id) VALUES 
    (14, 4),
    (15, 8), (15, 9),
    (17, 11), (17, 12),
    (19, 10),
    (20, 10);

INSERT INTO producer_song (producer_id, song_id) VALUES (7, 14);

INSERT INTO single (name, release_date) VALUES
    ('My God Is The Sun', '2013-04-08'),
    ('No One Knows', '2002-11-26'),
    ('Gardenia', '1995-01-01'),
    ('Have A Cigar', '1975-11-15'),
    ('Paranoid Android', '1997-05-26'),
    ('No Church In The Wild', '2012-03-20'),
    ('N****s In Paris', '2011-09-13'),
    ('POWER', '2010-07-01'),
    ('Runaway', '2010-10-04');

INSERT INTO single_song (single_id, song_id) VALUES
    (1, 1),
    (2, 3),
    (3, 5),
    (4, 9), (4, 8),
    (5, 12), (5, 13), (5, 14),
    (6, 15),
    (7, 16),
    (8, 18),
    (9, 19);
