USE home_library;
--  В.17. 3) Получить список книг, взятых вами в долг.
SELECT 
	b.book_id, 
	b.book_name, 
    d.date_start, 
    d.date_end, 
	a.first_name,
    a.medium_name,
    a.last_name
FROM debts d
JOIN debts_records dr ON d.debt_id = dr.debt_id
JOIN books b ON dr.book_id = b.book_id

JOIN authors_records ar ON b.book_id = ar.book_id
JOIN authors a ON ar.author_id = a.author_id

WHERE d.friend_id = 11;