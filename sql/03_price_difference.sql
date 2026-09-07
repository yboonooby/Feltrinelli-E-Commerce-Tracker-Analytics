with price_jumps as (
select
snapshot_date,
isbn_code,
coalesce(old_price, price) as full_price,
price as current_price,
discount as current_discount,
(lag(price) over (partition by isbn_code order by snapshot_date)) as yesterday_price,
price - coalesce(lag(price) over (partition by isbn_code order by snapshot_date), price) as price_difference,
min(price) over (partition by isbn_code) as lowest_price,
max(discount) over (partition by isbn_code) as highest_discount
from daily_book_rankings dbr)

select *
from price_jumps
where snapshot_date::date = current_date
order by price_difference asc