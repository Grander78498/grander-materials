-- Операции выборки


-- #1 Операция проекции - вывод нахваний всех альбомов
SELECT name FROM album;


-- #2 Операция селекции - вывод песен, которые не короче 6 минут
SELECT name, duration FROM song WHERE duration >= INTERVAL '00:06:00';


-- #3 Операция соединения - вывод названия альбома у песен
SELECT s.id, s.name, s.duration, a.name FROM song AS s, album AS a
    WHERE s.album_id = a.id;
-- #3.1 То же самое, но с JOIN
SELECT s.id, s.name, s.duration, a.name FROM song AS s 
    INNER JOIN album AS a
    ON s.album_id = a.id;


-- #4 Операция объединения - вывод музыкантов, состоящих в группе QOTSA или Kyuss
SELECT m.name AS musician_name, g.name AS group_name FROM musician AS m
    INNER JOIN (
        SELECT g1.name, gm.musician_id FROM music_group AS g1
        INNER JOIN group_musician AS gm ON gm.group_id = g1.id
    ) AS g ON g.musician_id = m.id
    WHERE g.name LIKE 'Queen%' OR g.name = 'Kyuss';


-- #5 Операция пересечения - вывод музыкантов, состоящих одновременно в группе QOTSA и Kyuss
SELECT m.name AS musician_name
    FROM musician AS m
    INNER JOIN group_musician AS gm ON gm.musician_id = m.id
    INNER JOIN music_group AS g ON gm.group_id = g.id
    WHERE g.name LIKE 'Queen%' AND EXISTS (
        SELECT * FROM group_musician AS gm1
        INNER JOIN music_group AS g1 ON g1.id = gm1.group_id
        WHERE gm1.musician_id = m.id AND g1.name = 'Kyuss'
    );


-- # Вывод всех песен с соответствующими исполнителями (не относится к практике)
SELECT s.name AS song_name,
        CASE WHEN (m.name, g.name) IS NULL THEN NULL
             ELSE concat(m.name, g.name) END AS performer_name
FROM song AS s
JOIN song_performer AS sp ON sp.song_id = s.id
JOIN performer AS p ON p.id = sp.performer_id
LEFT OUTER JOIN musician AS m ON m.id = p.musician_id
RIGHT OUTER JOIN performer AS p1 ON p1.id = p.id
LEFT OUTER JOIN music_group AS g ON g.id = p1.group_id
ORDER BY s.id, g.id, m.id;


-- #6 Гигантский пример на операцию разности 
-- Вывод песен Kanye West без участия Kid Cudi
SELECT s.name AS song_name,
        CASE WHEN (m.name, g.name) IS NULL THEN NULL
             ELSE concat(m.name, g.name) END AS performer_name
FROM song AS s
JOIN song_performer AS sp ON sp.song_id = s.id
JOIN performer AS p ON p.id = sp.performer_id
LEFT OUTER JOIN musician AS m ON m.id = p.musician_id
RIGHT OUTER JOIN performer AS p1 ON p1.id = p.id
LEFT OUTER JOIN music_group AS g ON g.id = p1.group_id
WHERE m.name LIKE 'Kanye%' AND NOT EXISTS (
    SELECT * FROM song AS s1
    JOIN song_performer AS sp ON sp.song_id = s.id
    JOIN performer AS p ON p.id = sp.performer_id
    LEFT OUTER JOIN musician AS m ON m.id = p.musician_id
    RIGHT OUTER JOIN performer AS p1 ON p1.id = p.id
    LEFT OUTER JOIN music_group AS g ON g.id = p1.group_id
    WHERE s1.id = s.id AND m.name LIKE 'Kid%'
)
ORDER BY s.id, g.id, m.id;


-- #7 Операция группировки - вывод длины каждого альбома
SELECT a.name, SUM(s.duration) AS album_duration FROM album AS a
JOIN song AS s ON s.album_id = a.id
GROUP BY a.id;
-- #7.1 Операция группировки c HAVING - вывод альбомов с длиной не менее 10 минут
SELECT a.name, SUM(s.duration) AS album_duration FROM album AS a
JOIN song AS s ON s.album_id = a.id
GROUP BY a.id HAVING album_duration >= INTERVAL '00:10:00';


-- #8 Операция сортировки - вывод альбомов в порядке убывания их длины
SELECT a.name, SUM(s.duration) AS album_duration FROM album AS a
JOIN song AS s ON s.album_id = a.id
GROUP BY a.id ORDER BY album_duration DESC;


-- #9 Ужасающий пример операции деления - вывести продюсера(-ов),
-- который(-е) продюссировал(-и) все альбомы Queens Of The Stone Age
SELECT pr.name, a.name FROM producer AS pr
JOIN producer_album AS pra ON pra.producer_id = pr.id
JOIN album AS a ON a.id = pra.album_id
JOIN album_performer AS ap ON ap.album_id = a.id
JOIN performer AS p ON p.id = ap.performer_id
JOIN music_group AS g ON g.id = p.group_id
WHERE g.name LIKE 'Queen%'
AND NOT EXISTS (
    SELECT pr1.name, a1.name FROM producer AS pr1, album AS a1
    JOIN album_performer AS ap1 ON ap1.album_id = a1.id
    JOIN performer AS p1 ON p1.id = ap1.performer_id
    JOIN music_group AS g1 ON g1.id = p1.group_id
    WHERE g1.name LIKE 'Queen%'
    AND NOT EXISTS (
        SELECT 1 FROM producer AS pr2
        JOIN producer_album AS pra1 ON pra1.producer_id = pr2.id
        JOIN album AS a2 ON a2.id = pra1.album_id
        WHERE pr2.id = pr1.id AND a2.id = a1.id
    )
    AND pr1.id = pr.id
);


-- #10 Создание представлений - запрос на участников Kyuss
CREATE VIEW Kyuss_musicians
AS
SELECT m.* FROM musician AS m
JOIN group_musician AS gm ON gm.musician_id = m.id
JOIN music_group AS g ON g.id = gm.group_id
WHERE g.name = 'Kyuss';
-- Выбор музыкантов с именами на Jo.. из этого представления
SELECT name FROM Kyuss_musicians WHERE name LIKE 'Jo%';


-- Процедуры, функции и триггеры
-- #1 Процедура добавления песни к исполнителю
CREATE PROCEDURE add_song_to_performer (song_id INTEGER, album_id INTEGER)
AS $$
DECLARE performer_id INTEGER;
DECLARE performer_cursor CURSOR FOR
    SELECT ap.performer_id FROM song AS s
    JOIN album AS a ON a.id = s.album_id
    JOIN album_performer AS ap ON ap.album_id = a.id
    WHERE s.id = song_id;
BEGIN
    OPEN performer_cursor;
    LOOP
        FETCH performer_cursor INTO performer_id;
        IF NOT FOUND THEN EXIT; END IF;
        INSERT INTO song_performer (song_id, performer_id)
        VALUES ($1, performer_id);
    END LOOP;
    CLOSE performer_cursor;
END;
$$ LANGUAGE plpgsql;


-- #2 Функция, вычисляющая возраст музыканта
CREATE FUNCTION musician_age (musician_id BIGINT)
RETURNS SMALLINT AS $$
DECLARE age SMALLINT;
BEGIN
    SELECT EXTRACT(years FROM AGE(
        NOW(),
        (SELECT birth_date FROM musician
            WHERE id = musician_id)
    )) INTO age;
    RETURN age;
END;
$$ LANGUAGE plpgsql;


-- #3 Процедура для триггера
CREATE FUNCTION calculate_duration ()
RETURNS trigger AS $$
DECLARE album_duration INTERVAL;
BEGIN
    SELECT SUM(duration) FROM song
    WHERE album_id = NEW.album_id
    GROUP BY album_id
    INTO album_duration;
    UPDATE album SET duration = album_duration WHERE id = NEW.album_id;
    RAISE NOTICE 'Триггер отработал';
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- #3.1 Сам триггер
CREATE TRIGGER tr_calc_dur
AFTER INSERT ON song FOR EACH ROW
EXECUTE FUNCTION calculate_duration();
