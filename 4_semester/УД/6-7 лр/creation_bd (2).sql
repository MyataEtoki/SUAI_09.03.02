CREATE DATABASE IF NOT EXISTS home_library;
USE home_library;

CREATE TABLE IF NOT EXISTS book_genre (
genre_id INTEGER AUTO_INCREMENT PRIMARY KEY,
genre_name VARCHAR(50) unique);

CREATE TABLE IF NOT EXISTS books (
book_id INTEGER AUTO_INCREMENT PRIMARY KEY,
book_name VARCHAR(50),
release_date date,
genre_id INTEGER NOT NULL, 
ENC_code VARCHAR(10) NOT NULL,
CONSTRAINT fk_genre_id
  FOREIGN KEY (genre_id)
  REFERENCES home_library.book_genre (genre_id));

CREATE TABLE IF NOT EXISTS authors (
author_id INTEGER AUTO_INCREMENT PRIMARY KEY,
first_name VARCHAR(50) NOT NULL,
medium_name VARCHAR(50),
last_name VARCHAR(50) NOT NULL);

CREATE TABLE IF NOT EXISTS authors_records (
  book_id INTEGER,
  author_id INTEGER,
  PRIMARY KEY (book_id, author_id),
  CONSTRAINT fk_authors_book_id
    FOREIGN KEY (book_id)
    REFERENCES home_library.books (book_id),
  CONSTRAINT fk_authors_author_id
    FOREIGN KEY (author_id)
    REFERENCES home_library.authors (author_id)
);
  
CREATE TABLE IF NOT EXISTS disc_format (
format_id INTEGER AUTO_INCREMENT PRIMARY KEY,
format_name VARCHAR(50) NOT NULL unique);

CREATE TABLE IF NOT EXISTS discs (
disc_id INTEGER AUTO_INCREMENT PRIMARY KEY,
disc_name VARCHAR(50),
disc_format_id INT NOT NULL,
genre_name VARCHAR(30) NOT NULL,
CONSTRAINT fk_format_id
  FOREIGN KEY (disc_format_id)
  REFERENCES home_library.disc_format (format_id));

CREATE TABLE  IF NOT EXISTS movies (
movie_id INTEGER AUTO_INCREMENT PRIMARY KEY,
movie_name VARCHAR(50),
disc_id INTEGER,
movie_format VARCHAR(20),
movie_genre VARCHAR(20),
release_date date,
movie_length time);

CREATE TABLE IF NOT EXISTS discs_records (
  movie_id INTEGER,
  disc_id INTEGER,
  PRIMARY KEY (movie_id, disc_id),
  CONSTRAINT fk_discs_movie_id
    FOREIGN KEY (movie_id)
    REFERENCES home_library.movies (movie_id),
  CONSTRAINT fk_discs_disc_id
    FOREIGN KEY (disc_id)
    REFERENCES home_library.discs (disc_id)
);
  
CREATE TABLE IF NOT EXISTS friends (
friend_id INTEGER AUTO_INCREMENT PRIMARY KEY,
first_name VARCHAR(50) NOT NULL,
last_name VARCHAR(50) NOT NULL);

CREATE TABLE IF NOT EXISTS debts (
debt_id INTEGER AUTO_INCREMENT PRIMARY KEY,
friend_id INTEGER NOT NULL,
exchange_type tinytext NOT NULL 
CHECK(exchange_type = 'borrowed' or exchange_type = 'taken'),
date_start date,
date_end date,
CONSTRAINT fk_friend_id
  FOREIGN KEY (friend_id)
  REFERENCES home_library.friends (friend_id));
  
CREATE TABLE IF NOT EXISTS debts_records (
record_id INT PRIMARY KEY AUTO_INCREMENT,
book_id INTEGER,
disc_id INTEGER,
debt_id INTEGER NOT NULL,
CONSTRAINT fk_debts_book_id
  FOREIGN KEY (book_id)
  REFERENCES home_library.books (book_id),
CONSTRAINT fk_debts_disc_id
  FOREIGN KEY (disc_id)
  REFERENCES home_library.discs (disc_id),
CONSTRAINT fk_debt_id
  FOREIGN KEY (debt_id)
  REFERENCES home_library.debts (debt_id));

