def phone_book(max_contacts):
    # Создаем словарь для хранения телефонной книги
    book = {}

    # Читаем количество запросов
    n = int(input())

    # Обрабатываем каждый запрос
    for _ in range(n):
        query = input().split()
        command = query[0]

        if command == 'add':
            number = query[1]
            name = query[2]
            # Проверяем, достигнут ли лимит по контактам
            if number not in book and len(book) >= max_contacts:
                print("Error: contact limit reached")
                continue
            # Проверка на существование имени с другим номером
            if name in book.values() and number not in book:
                print("Error: name already used with a different number")
                continue
            if len(number) >7 or len(name)>15:
                print("Error: length of number > 7 or length of name > 15")
                continue
            else:
                # Добавляем или обновляем запись
                book[number] = name
        elif command == 'del':
            number = query[1]
            # Удаляем запись, если она существует
            if number in book:
                del book[number]
        elif command == 'find':
            number = query[1]
            # Ищем запись и выводим соответствующий результат
            if number in book:
                print(book[number])
            else:
                print("not found")
        elif command == '0':
            print(book)

def main():
    # Устанавливаем лимит по количеству контактов
    max_contact_limit = 3
    # Запускаем телефонную книгу
    phone_book(max_contact_limit)

if __name__ == "__main__":
    main()