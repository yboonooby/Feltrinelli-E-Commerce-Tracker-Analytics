with discount_price_previous_days as (
select *,
lag(discount) over (partition by isbn_code order by snapshot_date) - discount as discount_difference_1,
lag(discount, 2) over (partition by isbn_code order by snapshot_date) - 
lag(discount) over (partition by isbn_code order by snapshot_date) as discount_difference_2,
coalesce(lag(rank) over (partition by isbn_code order by snapshot_date), 101) - rank as rank_difference
from daily_book_rankings dbr)

select
snapshot_date,
isbn_code,
discount_difference_1,
discount_difference_2,
discount,
rank,
rank_difference
from discount_price_previous_days
where snapshot_date::date = current_date
order by rank_difference desc