class Stack:
    # конструктор
    def __init__(self, stack_size):
        self.stack = []
        self.max_stack = []
        self.total_sum = 0
        self.count = 0 # чисел в стеке
        self.min_stack = []
        self.stack_size = stack_size

    # метод добавления элемента
    def push(self, value):
        if self.count >= self.stack_size:
            return "stack overflow"

        self.stack.append(value)
        # для avg и overflow
        self.total_sum += value
        self.count += 1

        if not self.max_stack or value >= self.max_stack[-1]:
            self.max_stack.append(value)

        if not self.min_stack or value <= self.min_stack[-1]:
            self.min_stack.append(value)
    # метод удаления последнего элемента
    def pop(self):
        if self.stack:
            value = self.stack.pop()
            self.total_sum -= value
            self.count -= 1

            if value == self.max_stack[-1]:
                self.max_stack.pop()

            if value == self.min_stack[-1]:
                self.min_stack.pop()

    def get_max(self):
        return self.max_stack[-1] if self.max_stack else None

    def get_avg(self):
        if self.count == 0:
            return None
        return self.total_sum / self.count

    def get_min(self):
        return self.min_stack[-1] if self.min_stack else None


def main():
    import sys

    input = sys.stdin.read # переопределяем input - поток ввода в консоль, чтения до конца
    data = input().strip().splitlines() # убираем пустоты, разбиваем строку на много

    q = int(data[0])
    stack_size = 3  # Размер стека
    max_stack = Stack(stack_size)

    results = []
    for i in range(1, q + 1):
        command = data[i].split() # ['push', '(int)']
        if command[0] == 'push':
            if command[1] is str:
                value = int(command[1])
                overflow_message = max_stack.push(value)
                if overflow_message:
                    results.append(overflow_message)
            else:
                results.append('this not a number')
        elif command[0] == 'pop':
            max_stack.pop()
        elif command[0] == 'max':
            current_max = max_stack.get_max()
            if current_max is not None: # проверяем что стек не пуст
                results.append(str(current_max))
        elif command[0] == 'avg':
            current_avg = max_stack.get_avg()
            if current_avg is not None:
                results.append(f"{current_avg:.6f}")
        elif command[0] == 'min':
            current_min = max_stack.get_min()
            if current_min is not None:
                results.append(str(current_min))

    # Запись результатов в файл
    with open('output.txt', 'w') as f:
        f.write('\n'.join(results) + '\n')


if __name__ == '__main__':
    main()
