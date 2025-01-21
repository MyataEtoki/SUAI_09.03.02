import time
import sys
sys.setrecursionlimit(2000)  # Увеличиваем допустимую глубину рекурсии

# Запоминаем время начала работы
start_time = time.time()

# Разделение массива
def partition(unsorted, start, end):
    part = start # Опорный элемент - 0вой
    for i in range(start + 1, end + 1): # end+1, чтобы включить последний эл-т (по-умолч. не включительно)
        if unsorted[i] <= unsorted[start]: # если правый эл-т меньше опорного(он 0вой)
            part += 1 # мы нашли ещё один элемент, который должен быть перемещён влево от опорного.
            unsorted[i], unsorted[part] = unsorted[part], unsorted[i]
            # все элементы, меньшие либо равные опорному, будут перемещены влево от него
    unsorted[part], unsorted[start] = unsorted[start], unsorted[part] # опорный элемент, теперь на новом индексе
    return part
# возвращает индекс опорного элемента, чтобы использовать его для следующего разбиения в рекурсивной сортировке

# Сортировка
def quick_sort(unsorted, start=0, end=None):
    if end is None: # только начали = охватываем весь массив
        end = len(unsorted) - 1
    def quick(unsorted, start, end):
        if start >= end: # пришли в конец
            return
        part = partition(unsorted, start, end) # делим массив на меньшую часть и большую,
        # относительно опорного эл-та, возвр. его индекс
        # опорный элемент теперь где-то в серединке unsorted
        quick(unsorted, start, part-1) # сортировка левой части массива — слева от опорного эл-та
        quick(unsorted, part+1, end) # сортировка правой
    return quick(unsorted, start, end) # возвращаем результат ф-и quick, которая выполняет всю сортировку

# считаем сколько слов на букву
def words_per_letter(letter, words):
    count=0
    for word in words:
        if word[0] == letter:
            count +=1
    return count


# Считывание файла
# path_of_file = input()
path_of_file = 'input1.txt'  # для тестов
with open(path_of_file, 'r', encoding='utf-8') as in_file:
    text = in_file.read()
    input_text = text

# Убираем числа и спец. символы
for cifra in '1234567890.,-—«"()„!?;':
    text = text.replace(cifra, '')

# Разделяем текст на массив слов
words = text.lower().split()
# text.lower() - делаем заглавные и строчные буквы строчными

# Сортируем
quick_sort(words, start=0, end=None)

# Считаем время сортировки
end_time = time.time()
sort_time_sec = end_time - start_time
sort_time_mlsec = sort_time_sec*1000

# Анализ
## Введённый текст
with open("analysis1.txt", "w", encoding='utf-8') as anal_file:
    # Записываем строки в файл
    anal_file.write("Введённый текст: *5 глав Преступления и Наказания*\n")
    #anal_file.write(input_text)
    anal_file.write("\n\n")
    anal_file.write("Вариант 17: Быстрая сортировка. Кириллица. По алфавиту. По возрастанию. Игнорировать числа и знаки препинания. \n")
    anal_file.write(f"Количество слов: {len(words)} \n")
    anal_file.write(f"Время сортировки: {sort_time_mlsec:.0f} миллисекунд \n")
    anal_file.write("Статистика (кол-во слов на каждую букву алфавита) \n")
    # "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    for letter in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя":
        anal_file.write(f"{letter} - {words_per_letter(letter,words)}\n")

# Выводим массив слов
print(words)
