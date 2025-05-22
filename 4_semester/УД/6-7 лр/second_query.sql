USE home_library;
--  В.17. 2) Получить информацию о всех книгах, содержащих детективы. (+автор)
SELECT 
	books.book_id, 
    books.book_name, 
	a.first_name, 
    a.last_name, 
    book_genre.genre_name 
FROM books
JOIN book_genre ON books.book_genre_id = book_genre.genre_id
JOIN authors_records ar ON books.book_id = ar.book_id
JOIN authors a ON ar.author_id = a.author_id
WHERE book_genre.genre_name = 'Детектив';