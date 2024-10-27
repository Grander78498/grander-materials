-- Агрегирующие функции
SELECT
    a.name,
    s.name,
    COUNT(*) OVER (PARTITION BY a.id) AS song_count,
    SUM(s.duration) OVER (PARTITION BY a.id) AS album_duration,
    AVG(s.duration) OVER (PARTITION BY a.id) AS avg_song_duration,
    MIN(s.duration) OVER (PARTITION BY a.id) AS min_song_duration,
    MAX(s.duration) OVER (PARTITION BY a.id) AS max_song_duration
FROM song AS s
JOIN album AS a ON a.id = s.album_id;


-- Ранжирующие функции
SELECT
    a.name,
    s.name,
    ROW_NUMBER() OVER (PARTITION BY a.id ORDER BY s.id) AS song_number
FROM song AS s
JOIN album AS a ON a.id = s.album_id;

WITH song_performer_info
AS
(SELECT CASE WHEN (m.name, g.name) IS NULL THEN NULL
             ELSE concat(m.name, g.name) END AS performer_name,
        COUNT(*) AS song_count
FROM song AS s
JOIN song_performer AS sp ON sp.song_id = s.id
JOIN performer AS p ON p.id = sp.performer_id
LEFT OUTER JOIN musician AS m ON m.id = p.musician_id
LEFT OUTER JOIN music_group AS g ON g.id = p.group_id
GROUP BY performer_name)
SELECT
    performer_name,
    song_count,
    RANK() OVER (ORDER BY song_count DESC) AS song_cnt_rank,
    DENSE_RANK() OVER (ORDER BY song_count DESC) AS song_cnt_dense_rank
FROM song_performer_info;

SELECT
    a.name,
    s.name,
    NTILE(2) OVER (PARTITION BY a.id ORDER BY s.id) AS vinyl_side
FROM song AS s
JOIN album AS a ON a.id = s.album_id;


-- Функции смещения
SELECT
    a.name AS album_name,
    s.name AS song_name,
    LAG(s.name) OVER (PARTITION BY a.name ORDER BY s.id) AS previous_song,
    LEAD(s.name) OVER (PARTITION BY a.name ORDER BY s.id) AS next_song
FROM song AS s
JOIN album AS a ON a.id = s.album_id;

SELECT DISTINCT ON (a.name)
    a.name AS album_name,
    FIRST_VALUE(s.name) OVER (PARTITION BY a.name ORDER BY s.id) AS first_song,
    LAST_VALUE(s.name) OVER value_window AS last_song,
    NTH_VALUE(s.name, 2) OVER value_window AS second_song
FROM song AS s
JOIN album AS a ON a.id = s.album_id
WINDOW value_window AS (PARTITION BY a.name ORDER BY s.id
                         ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING);