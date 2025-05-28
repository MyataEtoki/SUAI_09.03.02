USE home_library;
--  В.17. 1) Найти все книги заданного жанра.
SELECT book_name FROM books
JOIN book_genre ON books.book_genre_id = book_genre.genre_id
WHERE book_genre.genre_name = 'Роман';