Use real_estete;

-- Ситуация: Агент изменил фамилию
UPDATE agents SET last_name = 'Иванов-Новый' WHERE id = 1;

-- Ситуация: Изменилась цена квартиры
UPDATE apartments SET price = 4800000.00 WHERE id = 1;

-- Ситуация: Квартира снята с продажи
UPDATE apartments SET is_for_sale = FALSE WHERE id = 2;

-- Ситуация: Исправление площади (была введена с ошибкой)
UPDATE apartments SET area = 55.00 WHERE id = 1;

-- Для некорректных данных
UPDATE cities SET name='   ' where id=1;

-- Каскадное обновление ID улицы
UPDATE agents SET id = 100 WHERE id = 1;
