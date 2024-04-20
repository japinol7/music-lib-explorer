------------------------------------------------------------------------------
------------------------------------------------------------------------------
select x_id from song
    group by x_id
    having COUNT(x_id) > 1;
------------------------------------------------------------------------------
select * from song where artist like '%chitai%';
select * from song order by id;
------------------------------------------------------------------------------

------------------------------------------------------------------------------
-- From XML to CSV:
-- 1. Delete unnecessary data
update song set date_added_orig = NULL, is_data_added_fixed = NULL where id > 0;
-------
-- 2. Join songs and albums genres that are alike but with different capitalization
update album set genre = 'Hard rock', genre_internal = '||Hard rock||' where genre_internal = '||Hard Rock||';
update song set genre = 'Hard rock' where genre = 'Hard Rock';
update album set genre = 'Classical crossover', genre_internal = '||Classical crossover||' where genre_internal = '||Classical Crossover||';
update song set genre = 'Classical crossover' where genre = 'Classical Crossover';
-------
-- 3. Data to export as csv
select s.*, a.name as album, a.artist as album_artist from song s
    left join album a on s.album_id = a.id
    order by s.id
    ;
------------------------------------------------------------------------------
select * from album where artist like '%chitai%';
select * from album order by name;
select * from album where genre like '%blues%' order by name;

select name, track_count from album order by name;
------------------------------------------------------------------------------
select count(id) count from song;
-----
--  > R: 56630

--------------------
select count(id) count from album;
-----
--  > R: 4444

--
-- \Music\iTunes\iTunes Media\Music
------------------------------------------------------------------------------
select genre from song
    group by genre
    having COUNT(genre) > 0;
-----
--  > R: 29 genres:
--
-- Alternative
-- Blues
-- Celtic
-- Children's Music
-- Christmas
-- Classical
-- Classical crossover
-- Country
-- Disco
-- Electronic
-- Folk
-- Folk rock
-- Folk trad
-- Gospel
-- Hard rock
-- Jazz
-- Jazz vocal
-- Metal
-- New Age
-- Pop
-- Pop dynamic
-- R&B/Soul
-- Reggae
-- Rock
-- Rock neoclassical
-- Singer-Songwriter
-- Soundtrack
-- Spoken Word
-- Strings crossover
------------------------------------------------------------------------------
------------------------------------------------------------------------------
select count(id) count from song where is_data_added_fixed = TRUE order by id;
--
select a.name as album, a.artist as album_artist, s.date_released, s.date_added, s.date_added_orig, s.is_data_added_fixed from song s
    left join album a on s.album_id = a.id
    where is_data_added_fixed = TRUE
    order by s.id
    ;
------------------------------------------------------------------------------
select a.name as album, a.artist as album_artist, s.name, s.year, s.is_user_added  from song s
    left join album a on s.album_id = a.id
    where is_user_added = TRUE
    order by s.id
    ;
------------------------------------------------------------------------------
-- Count albums with same name
select name, count(*)
    from album
    group by name
    having count(*) > 1
    order by name
    ;
------------------------------------------------------------------------------
------------------------------------------------------------------------------
