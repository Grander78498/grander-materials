SELECT * FROM album WHERE id = 2;
SELECT * FROM song WHERE id > 3;
SELECT * FROM album WHERE release_date < '2000-01-01';
SELECT * FROM song WHERE duration >= INTERVAL '6 MINUTES';
SELECT * FROM album WHERE release_type_id <= 2;
SELECT * FROM album WHERE release_type_id != 1;
SELECT * FROM song WHERE album_id IS NOT NULL;
SELECT * FROM song WHERE album_id IS NULL;
SELECT * FROM song WHERE duration BETWEEN INTERVAL '4 MINUTES' AND INTERVAL '6 MINUTES';
SELECT * FROM album WHERE id IN (2, 5, 7, 9, 10);
SELECT * FROM music_group WHERE id NOT IN (2, 3, 5);
SELECT * FROM musician WHERE name LIKE 'Jo%';
SELECT * FROM album WHERE name NOT LIKE '%The%';

SELECT * FROM song ORDER BY duration;
SELECT * FROM album ORDER BY name DESC;

ALTER TABLE album ADD COLUMN duration INTERVAL;
UPDATE album SET duration = INTERVAL '00:06:35' WHERE name = 'PULSE';
BEGIN;
DELETE FROM musician WHERE name LIKE 'Kanye%';
ROLLBACK;