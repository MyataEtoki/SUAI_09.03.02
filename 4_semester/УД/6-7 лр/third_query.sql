USE home_library;
--  В.17. 3) Получить список книг, взятых вами в долг.
SELECT * FROM debts d
JOIN debts_records dr ON d.debt_id = dr.debt_id
JOIN books b ON dr.book_id = b.book_id
WHERE d.friend_id = 11;