CREATE OR REPLACE VIEW daily_book_rankings AS
SELECT DISTINCT ON (dr.snapshot_date, dr.isbn_code)
    dr.snapshot_date,
    b.title,
    b.author,
    dr.isbn_code,
    dr.rank,
    dr.stars,
    dr.reviews,
    dr.price,
    dr.discount,
    dr.old_price
FROM daily_rankings dr
JOIN books b ON b.isbn_code = dr.isbn_code
ORDER BY dr.snapshot_date DESC, dr.isbn_code, dr.rank ASC;