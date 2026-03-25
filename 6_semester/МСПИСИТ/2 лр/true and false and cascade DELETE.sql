-- Удаление квартиры
DELETE FROM apartments WHERE id = 5;

-- Некорректное удаление квартиры (id не существует)
DELETE FROM apartments WHERE id = 999;

-- Удаление агента (каскадно удалит все его квартиры)
DELETE FROM agents WHERE id = 2;
