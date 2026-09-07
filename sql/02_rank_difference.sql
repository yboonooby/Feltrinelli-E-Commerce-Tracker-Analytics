with leaderboard_jumps as (
select
snapshot_date,
isbn_code,
rank,
coalesce((lag(rank) over (partition by isbn_code order by snapshot_date)), 101) - rank as leaderboard_jump
from daily_book_rankings dbr)

select *
from leaderboard_jumps lj
where snapshot_date::date = current_date
order by leaderboard_jump desc