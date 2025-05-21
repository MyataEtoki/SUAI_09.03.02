USE home_library;

-- Заполнение таблицы authors
INSERT INTO authors (first_name, medium_name, last_name) VALUES
('Лев', 'Николаевич', 'Толстой'),
('Фёдор', 'Михайлович', 'Достоевский'),
('Александр', NULL, 'Пушкин')
('Дарья','Донцова');

-- Заполнение таблицы book_genre
INSERT INTO book_genre (genre_name) VALUES
('Роман'),
('Фантастика'),
('Поэзия'),
('Детектив');

-- Заполнение таблицы books. Важно, чтобы book_genre_id совпадал.
INSERT INTO books (book_name, release_date, book_genre_id, ENC_code) VALUES
('Война и мир', '1869-01-01', 13, 'ENC001'),
('Преступление и наказание', '1866-01-01', 11, 'ENC002'),
('Евгений Онегин', '1833-01-01', 12, 'ENC003'),
('Запретите Донцовой писать.', '2025-05-21', 14, 'ENC001');

-- Заполнение таблицы friends
INSERT INTO friends (first_name, last_name) VALUES
('Я', 'Крутой Кузя'),
('Иван', 'Иванов'),
('Пётр', 'Петров'),
('Анна', 'Смирнова');

-- Заполнение таблицы disc_format
INSERT INTO disc_format (format_name) VALUES
('DVD'),
('Blu-Ray'),
('CD');

-- Заполнение таблицы authors_records
INSERT INTO authors_records (book_id, author_id) VALUES
(15, 11),
(16, 12),
(17, 13),
(18, 14);

-- Заполнение таблицы debts
INSERT INTO debts (friend_id, exchange_type, date_start, date_end) VALUES
(14, 'book', '2025-01-01', '2025-01-15'),
(12, 'disc', '2025-02-01', NULL),
(13, 'book', '2025-03-10', NULL);

-- Заполнение таблицы discs
INSERT INTO discs (disc_name, disc_format_id, genre_name) VALUES
('Коллекция фильмов 1', 12, 'Драма'),
('Альбом Queen', 13, 'Рок'),
('Научная фантастика', 12, 'Sci-Fi');

-- Заполнение таблицы movies
INSERT INTO movies (movie_name, disc_id, movie_format, movie_genre, release_date, movie_length) VALUES
('Матрица', 15, 'HD', 'Sci-Fi', '1999-03-31', '02:16:00'),
('Гладиатор', 13, 'FullHD', 'Драма', '2000-05-01', '02:35:00'),
('Амели', 13, 'HD', 'Романтика', '2001-04-25', '02:02:00');

-- Заполнение таблицы discs_records
INSERT INTO discs_records (movie_id, disc_id) VALUES
(16, 15),
(17, 13),
(18, 13);

-- Заполнение таблицы debts_records
INSERT INTO debts_records (book_id, disc_id, debt_id) VALUES
(15, NULL, 11),
(NULL, 13, 12),
(16, NULL, 13);