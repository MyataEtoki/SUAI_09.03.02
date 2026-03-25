-- Ситуация: потребовалось хранить год постройки дома
ALTER TABLE apartments 
ADD COLUMN year_built INT DEFAULT NULL;

-- Заполнение данных
UPDATE apartments SET year_built = 2013 WHERE id = 4;
UPDATE apartments SET year_built = 2000 WHERE id = 3;
UPDATE apartments SET year_built = null WHERE id = 1;