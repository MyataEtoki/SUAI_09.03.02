-- Проверка перед обновлением
SELECT id, street_id FROM apartments WHERE street_id = 1;

-- Обновление ID улицы (изменение первичного ключа)
UPDATE streets SET id = 100 WHERE id = 1;

-- Проверка после обновления (ID в квартирах обновился автоматически)
SELECT id, street_id FROM apartments WHERE street_id = 100;  -- Покажет обновлённые записи