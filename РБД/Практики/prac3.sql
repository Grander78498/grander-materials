SELECT s.id, s.name, s.duration, a.name FROM song AS s, album AS a
    WHERE s.album_id = a.id; -- Операция соединения
SELECT s.id, s.name, s.duration, a.name FROM song AS s 
    INNER JOIN album AS a
    ON s.album_id = a.id; -- Тоже операция соединения, но с JOIN

SELECT m.name AS musician_name, g.name AS group_name FROM musician AS m
    INNER JOIN (
        SELECT g1.name, gm.musician_id FROM music_group AS g1
        INNER JOIN group_musician AS gm ON gm.group_id = g1.id
    ) AS g ON g.musician_id = m.id
    WHERE g.name LIKE 'Queen%' OR g.name = 'Kyuss'; -- Операция объединения


SELECT m.name AS musician_name
    FROM musician AS m
    INNER JOIN group_musician AS gm ON gm.musician_id = m.id
    INNER JOIN music_group AS g ON gm.group_id = g.id
    WHERE g.name LIKE 'Queen%' AND EXISTS (
        SELECT * FROM group_musician AS gm1
        INNER JOIN music_group AS g1 ON g1.id = gm1.group_id
        WHERE gm1.musician_id = m.id AND g1.name = 'Kyuss'
    ); -- Операция пересечения

SELECT DISTINCT ON (song_name) s.name AS song_name, a.name AS album_name, m.name AS musician FROM song AS s
    JOIN album AS a ON a.id = s.album_id
    JOIN album_performer AS ap ON ap.album_id = a.id
    JOIN performer AS p ON p.id = ap.performer_id
    JOIN music_group AS g ON g.id = p.group_id
    JOIN group_musician AS gm ON gm.group_id = g.id
    JOIN musician AS m ON m.id = gm.musician_id
    WHERE m.name LIKE 'Jo%'; -- БОЛЬШЕ JOIN-ов !!!!!!!!!!!!!!!!!!!!!!!!!