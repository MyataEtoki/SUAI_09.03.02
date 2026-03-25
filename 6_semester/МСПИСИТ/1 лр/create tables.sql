USE real_estate;

-- 1. Города
CREATE TABLE cities (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    CONSTRAINT chk_city_name CHECK (CHAR_LENGTH(TRIM(name)) > 0)
);

-- 2. Районы
CREATE TABLE districts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    city_id INT DEFAULT NULL,
    CONSTRAINT chk_district_name CHECK (CHAR_LENGTH(TRIM(name)) > 0),
    CONSTRAINT fk_district_city 
        FOREIGN KEY (city_id) 
        REFERENCES cities(id) 
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 3. Улицы
CREATE TABLE streets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    CONSTRAINT chk_street_name CHECK (CHAR_LENGTH(TRIM(name)) > 0)
);

-- 4. Связь Улицы-Районы 
CREATE TABLE street_districts (
    street_id INT NOT NULL,
    district_id INT NOT NULL,
    PRIMARY KEY (street_id, district_id),
    
    CONSTRAINT fk_sd_street 
        FOREIGN KEY (street_id) 
        REFERENCES streets(id) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    
    CONSTRAINT fk_sd_district 
        FOREIGN KEY (district_id) 
        REFERENCES districts(id) 
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 5. Агенты
CREATE TABLE agents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50) DEFAULT NULL,
    CONSTRAINT chk_agent_names CHECK (
        CHAR_LENGTH(TRIM(last_name)) > 0 AND 
        CHAR_LENGTH(TRIM(first_name)) > 0
    )
);

-- 6. Строительные серии
CREATE TABLE building_series (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    CONSTRAINT chk_series_name CHECK (CHAR_LENGTH(TRIM(name)) > 0)
);

-- 7. Квартиры
CREATE TABLE apartments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    street_id INT NOT NULL,
    district_id INT NOT NULL,
    floor INT NOT NULL DEFAULT 1,
    apartment_number VARCHAR(20) DEFAULT NULL,
    rooms INT DEFAULT NULL,
    area DECIMAL(10, 2) DEFAULT NULL,
    price DECIMAL(12, 2) DEFAULT NULL,
    is_for_sale BOOLEAN DEFAULT TRUE,
    agent_id INT DEFAULT NULL,
    series_id INT DEFAULT NULL,

    -- CHECK ограничения для числовых данных
    CONSTRAINT chk_floor CHECK (floor > 0),
    CONSTRAINT chk_rooms CHECK (rooms IS NULL OR rooms > 0),
    CONSTRAINT chk_area CHECK (area IS NULL OR area > 0),
    CONSTRAINT chk_price CHECK (price IS NULL OR price >= 0),
    
    -- Внешние ключи с каскадным удалением
    CONSTRAINT fk_apt_street 
        FOREIGN KEY (street_id) 
        REFERENCES streets(id) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_apt_district 
        FOREIGN KEY (district_id) 
        REFERENCES districts(id) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_apt_agent 
        FOREIGN KEY (agent_id) 
        REFERENCES agents(id) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_apt_series 
        FOREIGN KEY (series_id) 
        REFERENCES building_series(id) 
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
