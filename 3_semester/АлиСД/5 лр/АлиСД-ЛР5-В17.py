from collections import deque

def sliding_window_maximum(n, A, m):
    # Дек для хранения индексов элементов массива
    dq = deque()
    max_numbers = []

    for i in range(n):
        # Удаляем элементы вне окна (скользит вправо)
        if dq and dq[0] < i - m + 1:
            dq.popleft()
        # Удаляем элементы из дека, которые меньше текущего элемента
        while dq and A[dq[-1]] < A[i]:
            dq.pop()

        # Добавляем текущий индекс в дек
        dq.append(i)
        # Если окно полностью заполнено, добавляем максимум в результат
        if i >= m - 1:
            max_numbers.append(A[dq[0]])

    return max_numbers

# Чтение входных данных
n = int(input())  # Число элементов
A = list(map(int, input().split()))  # Сам массив
m = int(input())  # Размер окна

# Получаем максимумы и выводим результат
result = sliding_window_maximum(n, A, m)
print(" ".join(map(str, result)))
