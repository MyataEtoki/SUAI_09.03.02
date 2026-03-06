USE real_estate;

-- Города
CREATE TABLE cities (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);

-- Районы
CREATE TABLE districts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    city_id INT,
    CONSTRAINT fk_district_city 
        FOREIGN KEY (city_id) 
        REFERENCES cities(id) 
        ON DELETE CASCADE
);

-- Улицы
-- Поле district_id удалено, так как связь теперь многосторонняя
CREATE TABLE streets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL
);

-- Связь Улицы-Районы 
CREATE TABLE street_districts (
    street_id INT NOT NULL,
    district_id INT NOT NULL,
    PRIMARY KEY (street_id, district_id),
    
    CONSTRAINT fk_sd_street 
        FOREIGN KEY (street_id) 
        REFERENCES streets(id) 
        ON DELETE CASCADE,
    
    CONSTRAINT fk_sd_district 
        FOREIGN KEY (district_id) 
        REFERENCES districts(id) 
        ON DELETE CASCADE
);

-- Агенты
CREATE TABLE agents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50)
);

-- Строительные серии
CREATE TABLE building_series (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL unique
);

-- Квартиры
CREATE TABLE apartments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    street_id INT NOT NULL,
    district_id INT NOT NULL,
    floor INT NOT NULL,
    apartment_number VARCHAR(20),
    rooms INT,
    area DECIMAL(10, 2),
    price DECIMAL(12, 2),
    is_for_sale BOOLEAN DEFAULT TRUE,
    agent_id INT,
    series_id INT,

    -- Внешние ключи с каскадным удалением
    CONSTRAINT fk_apt_street 
        FOREIGN KEY (street_id) 
        REFERENCES streets(id) 
        ON DELETE CASCADE,

    CONSTRAINT fk_apt_district 
        FOREIGN KEY (district_id) 
        REFERENCES districts(id) 
        ON DELETE CASCADE,

    CONSTRAINT fk_apt_agent 
        FOREIGN KEY (agent_id) 
        REFERENCES agents(id) 
        ON DELETE CASCADE,

    CONSTRAINT fk_apt_series 
        FOREIGN KEY (series_id) 
        REFERENCES building_series(id) 
        ON DELETE CASCADE
);