USE home_library;
--  В.17. 2) Получить информацию о всех книгах, содержащих детективы.
SELECT * FROM books
JOIN book_genre ON books.book_genre_id = book_genre.genre_id
WHERE book_genre.genre_name = 'Детектив';