-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema home_library
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema home_library
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `home_library` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `home_library` ;

-- -----------------------------------------------------
-- Table `home_library`.`authors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `home_library`.`authors` (
  `author_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NOT NULL,
  `medium_name` VARCHAR(50) NULL DEFAULT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`author_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `home_library`.`book_genre`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `home_library`.`book_genre` (
  `genre_id` INT NOT NULL AUTO_INCREMENT,
  `genre_name` VARCHAR(50) NULL DEFAULT NULL,
  PRIMARY KEY (`genre_id`),
  UNIQUE INDEX `genre_name` (`genre_name` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `home_library`.`books`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `home_library`.`books` (
  `book_id` INT NOT NULL AUTO_INCREMENT,
  `book_name` VARCHAR(50) NULL DEFAULT NULL,
  `release_date` DATE NULL DEFAULT NULL,
  `book_genre_id` INT NOT NULL,
  `ENC_code` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`book_id`),
  INDEX `fk_genre_id` (`book_genre_id` ASC) VISIBLE,
  CONSTRAINT `fk_genre_id`
    FOREIGN KEY (`book_genre_id`)
    REFERENCES `home_library`.`book_genre` (`genre_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 12
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `home_library`.`authors_records`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `home_library`.`authors_records` (
  `record_id` INT NOT NULL AUTO_INCREMENT,
  `book_id` INT NOT NULL,
  `author_id` INT NOT NULL,
  PRIMARY KEY (`record_id`),
  INDEX `fk_authors_book_id` (`book_id` ASC) VISIBLE,
  INDEX `fk_authors_author_id` (`author_id` ASC) VISIBLE,
  CONSTRAINT `fk_authors_author_id`
    FOREIGN KEY (`author_id`)
    REFERENCES `home_library`.`authors` (`author_id`),
  CONSTRAINT `fk_authors_book_id`
    FOREIGN KEY (`book_id`)
    REFERENCES `home_library`.`books` (`book_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 12
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `home_library`.`friends`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `home_library`.`friends` (
  `friend_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`friend_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `home_library`.`debts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `home_library`.`debts` (
  `debt_id` INT NOT NULL AUTO_INCREMENT,
  `friend_id` INT NOT NULL,
  `exchange_type` TINYTEXT NOT NULL,
  `date_start` DATE NULL DEFAULT NULL,
  `date_end` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`debt_id`),
  INDEX `fk_friend_id` (`friend_id` ASC) VISIBLE,
  CONSTRAINT `fk_friend_id`
    FOREIGN KEY (`friend_id`)
    REFERENCES `home_library`.`friends` (`friend_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `home_library`.`disc_format`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `home_library`.`disc_format` (
  `format_id` INT NOT NULL AUTO_INCREMENT,
  `format_name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`format_id`),
  UNIQUE INDEX `format_name` (`format_name` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `home_library`.`discs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `home_library`.`discs` (
  `disc_id` INT NOT NULL AUTO_INCREMENT,
  `disc_name` VARCHAR(50) NULL DEFAULT NULL,
  `disc_format_id` INT NOT NULL,
  `genre_name` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`disc_id`),
  INDEX `fk_format_id` (`disc_format_id` ASC) VISIBLE,
  CONSTRAINT `fk_format_id`
    FOREIGN KEY (`disc_format_id`)
    REFERENCES `home_library`.`disc_format` (`format_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 13
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `home_library`.`debts_records`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `home_library`.`debts_records` (
  `record_id` INT NOT NULL AUTO_INCREMENT,
  `book_id` INT NULL,
  `disc_id` INT NULL,
  `debt_id` INT NOT NULL,
  PRIMARY KEY (`record_id`),
  INDEX `fk_debts_book_id` (`book_id` ASC) VISIBLE,
  INDEX `fk_debts_disc_id` (`disc_id` ASC) VISIBLE,
  INDEX `fk_debt_id` (`debt_id` ASC) VISIBLE,
  CONSTRAINT `fk_debt_id`
    FOREIGN KEY (`debt_id`)
    REFERENCES `home_library`.`debts` (`debt_id`),
  CONSTRAINT `fk_debts_book_id`
    FOREIGN KEY (`book_id`)
    REFERENCES `home_library`.`books` (`book_id`),
  CONSTRAINT `fk_debts_disc_id`
    FOREIGN KEY (`disc_id`)
    REFERENCES `home_library`.`discs` (`disc_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `home_library`.`movies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `home_library`.`movies` (
  `movie_id` INT NOT NULL AUTO_INCREMENT,
  `movie_name` VARCHAR(50) NULL DEFAULT NULL,
  `disc_id` INT NULL DEFAULT NULL,
  `movie_format` VARCHAR(20) NULL DEFAULT NULL,
  `movie_genre` VARCHAR(20) NULL DEFAULT NULL,
  `release_date` DATE NULL DEFAULT NULL,
  `movie_length` TIME NULL DEFAULT NULL,
  PRIMARY KEY (`movie_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 16
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `home_library`.`discs_records`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `home_library`.`discs_records` (
  `record_id` INT NOT NULL AUTO_INCREMENT,
  `movie_id` INT NOT NULL,
  `disc_id` INT NOT NULL,
  PRIMARY KEY (`record_id`),
  INDEX `fk_discs_movie_id` (`movie_id` ASC) VISIBLE,
  INDEX `fk_discs_disc_id` (`disc_id` ASC) VISIBLE,
  CONSTRAINT `fk_discs_disc_id`
    FOREIGN KEY (`disc_id`)
    REFERENCES `home_library`.`discs` (`disc_id`),
  CONSTRAINT `fk_discs_movie_id`
    FOREIGN KEY (`movie_id`)
    REFERENCES `home_library`.`movies` (`movie_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 8
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
