-- Проверка перед удалением
SELECT COUNT(*) FROM apartments WHERE agent_id = 1;  -- Показывает квартиры агента

-- Удаление агента
DELETE FROM agents WHERE id = 1;

-- Проверка после удаления (квартиры агента удалены автоматически)
SELECT COUNT(*) FROM apartments WHERE agent_id = 1;  -- Вернёт 0