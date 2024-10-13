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
CREATE TABLE album_group (
    album_id BIGINT REFERENCES album (id) ON DELETE CASCADE NOT NULL,
    group_id BIGINT REFERENCES music_group (id) ON DELETE CASCADE NOT NULL,
    PRIMARY KEY (album_id, group_id)
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
CREATE TABLE song_group (
    song_id BIGINT REFERENCES song (id) ON DELETE CASCADE NOT NULL,
    group_id BIGINT REFERENCES music_group (id) ON DELETE CASCADE NOT NULL,
    PRIMARY KEY (song_id, group_id)
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


INSERT INTO music_group (name, country) VALUES 
    ('Queens Of The Stone Age', 'USA'),
    ('Kyuss', 'USA'),
    ('Pink Floyd', 'Great Britain'),
    ('Radiohead', 'Great Britain'),
    ('Kanye West', 'USA'),
    ('JAY-Z', 'USA'),
    ('Frank Ocean', 'USA'),
    ('The-Dream', 'USA'),
    ('Pusha T', 'USA'),
    ('Kid Cudi', 'USA'),
    ('Raekwon', 'USA'),
    ('Kids See Ghosts', 'USA');

INSERT INTO musician (name, country) VALUES
    ('Josh Homme', 'USA'),
    ('Dave Grohl', 'USA'),
    ('Nick Oliveri', 'USA'),
    ('Mark Lanegan', 'USA'),
    ('Brant Bjork', 'USA'),
    ('John Garcia', 'USA'),
    ('David Gilmour', 'Great Britain'),
    ('Roger Waters', 'Great Britain'),
    ('Thom Yorke', 'Great Britain'),
    ('Colin Greenwood', 'Great Britain'),
    ('Kanye West', 'USA'),
    ('JAY-Z', 'USA'),
    ('Frank Ocean', 'USA'),
    ('The-Dream', 'USA'),
    ('Pusha T', 'USA'),
    ('Kid Cudi', 'USA'),
    ('Raekwon', 'USA');

INSERT INTO group_musician (group_id, musician_id) VALUES
    (1, 1), (1, 2), (1, 3), (1, 4),
    (2, 1), (2, 3), (2, 5), (2, 6),
    (3, 7), (3, 8),
    (4, 9), (4, 10),
    (5, 11),
    (6, 12),
    (7, 13),
    (8, 14),
    (9, 15),
    (10, 16),
    (11, 17),
    (12, 11), (12, 16);

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

INSERT INTO album_group (album_id, group_id) VALUES
    (1, 1), (2, 1),
    (3, 2),
    (4, 3),
    (5, 4),
    (6, 5), (6, 6),
    (7, 5), (7, 10), (7, 12),
    (8, 5),
    (9, 3);

INSERT INTO producer (name, country) VALUES
    ('Josh Homme', 'USA'),
    ('Eric Valentine', 'USA'),
    ('Adam Casper', 'USA'),
    ('Chris Goss', 'USA'),
    ('Roger Waters', 'Great Britain'),
    ('David Gilmour', 'Great Britain'),
    ('Nigel Goldrich', 'Great Britain'),
    ('Kanye West', 'USA'),
    ('Kid Cudi', 'USA'),
    ('Mike Dean', 'USA');

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
    ('I Sat By The Ocean', 'PT3M55S', 1),
    ('My God Is The Sun', 'PT3M55S', 1),
    ('No One Knows', 'PT4M38S', 2),
    ('A Song For The Dead', 'PT5M52S', 2),
    ('Gardenia', 'PT6M54S', 3),
    ('Space Cadet', 'PT7M2S', 3),
    ('Shine on You Crazy Diamond (Parts I-V)', 'PT13M30S', 4),
    ('Welcome To The Machine', 'PT7M31S', 4),
    ('Have A Cigar', 'PT5M8S', 4),
    ('Wish You Were Here', 'PT5M40S', 4),
    ('Shine on You Crazy Diamond (Parts VI-IX)', 'PT12M31S', 4),
    ('Paranoid Android', 'PT6M23S', 5),
    ('Let Down', 'PT4M59S', 5),
    ('Pearly', 'PT3M33S', null),
    ('No Church In The Wild', 'PT4M32S', 6),
    ('N****s In Paris', 'PT3M39S', 6),
    ('Gorgeous', 'PT5M57S', 8),
    ('POWER', 'PT4M52S', 8),
    ('Runaway', 'PT9M7S', 8),
    ('Feel The Love', 'PT2M33S', 7),
    ('Cudi Montage', 'PT3M17S', 7),
    ('Wish You Were Here - Live', 'PT6M35S', 9);

INSERT INTO song_group (song_id, group_id) VALUES 
    (14, 4),
    (15, 7), (15, 8),
    (17, 10), (17, 11),
    (19, 9),
    (20, 9);

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
