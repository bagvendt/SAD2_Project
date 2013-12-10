select distinct a.id from actors as a
join roles R
on r.actor_id = a.id
where r.movie_id in(
select m.id from movies as m
where m.id in (
SELECT M.id FROM actors as A 
	JOIN roles R
	ON R.`actor_id` = A.`id`
		JOIN movies M 
		ON M.`id` = R.`movie_id` where R.actor_id = 12342 
))