def min_heapify(array, n, i, swaps):
    smallest = i
    left = 2 * i + 1
    right = 2 * i + 2

    # не вышли за пределы массива? и родительский эл-т меньше дочернего?
    # ищем эл-т, чтобы поменять с i-тым.
    if left < n and array[left] < array[smallest]:
        smallest = left
    if right < n and array[right] < array[smallest]:
        smallest = right
    # Если i-тый эл-т не наименьший - значит стоит не там, меняем.
    if smallest != i:
        array[i], array[smallest] = array[smallest], array[i]
        swaps.append((i, smallest))
        print(array)
        # проверяем нужно ли переместившийся эл-т опустить ещё ниже
        min_heapify(array, n, smallest, swaps)

def build_min_heap(array, n):
    swaps = []
    # Запускаем функцию восстановления кучи для каждого узла, начиная с последнего родительского
    # с р3 - [р1, р2, р3, д2, д2, д3] - [р1, р2, д1, д2, д2]
    for i in range(n // 2 - 1, -1, -1): # start, step, stop
        min_heapify(array, n, i, swaps)

    return swaps


# Чтение входных данных
flag = False
while not flag:
    try:
        n = int(input())
        A = list(map(int, input().split()))
        flag = True
    except ValueError:
        print("Это не целые числа, попробуйте ещё")

if flag and len(A)==n:
# Генерация мин-кучи
    swaps = build_min_heap(A, n)

# Вывод результата
    print(len(swaps))  # Количество обменов
    for swap in swaps:
        print(swap[0], swap[1])  # Индексы обменов

else:
    print("Длина массива А и n не совпадают. ")