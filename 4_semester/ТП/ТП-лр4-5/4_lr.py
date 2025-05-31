# Бинарное дерево с CRUD, без балансировки.

import random

# Генерация случайной последовательности
def generate_random_sequence():
    return [random.randint(0, 127) for _ in range(random.randint(1, 16))]

# Класс для узлов
class Node:
    def __init__(self, key):
        self.val = key
        self.left = None
        self.right = None
        self.parent = None

# Класс бинарного дерева
class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        new_node = Node(key)
        if self.root is None:
            self.root = new_node
        else:
            self._insert_recursive(self.root, new_node)

    def _insert_recursive(self, current, new_node):
        if new_node.val < current.val:
            if current.left is None:
                current.left = new_node
                new_node.parent = current
            else:
                self._insert_recursive(current.left, new_node)
        else:
            if current.right is None:
                current.right = new_node
                new_node.parent = current
            else:
                self._insert_recursive(current.right, new_node)

    def find(self, key):
        path = []
        node = self._find_recursive_verbose(self.root, key, path)
        for step in path:
            print(step)
        return node

    def _find_recursive_verbose(self, current, key, path):
        if current is None:
            path.append("Дошли до пустого узла — значение не найдено.")
            return None
        path.append(f"Находимся в узле {current.val}")
        if key == current.val:
            path.append(f"Значение {key} найдено!")
            return current
        elif key < current.val:
            path.append(f"{key} < {current.val} → идём влево")
            return self._find_recursive_verbose(current.left, key, path)
        else:
            path.append(f"{key} > {current.val} → идём вправо")
            return self._find_recursive_verbose(current.right, key, path)

    def delete(self, key):
        node = self.find(key)
        if node is None:
            print(f"Удалять нечего. {key} не найден.")
            return False
        self._delete_node(node)
        print(f"Узел со значением {key} успешно удалён.")
        return True

    def _delete_node(self, node):
        if node.left is None:
            self._transplant(node, node.right)
        elif node.right is None:
            self._transplant(node, node.left)
        else: # выбираем преемника - левый или правый ребёнок (чаще всего минимальный в правом)
            successor = self._minimum(node.right)
            if successor.parent != node: # преемник не прямой наследник
                self._transplant(successor, successor.right)
                successor.right = node.right
                if successor.right:
                    successor.right.parent = successor
            self._transplant(node, successor)
            successor.left = node.left
            if successor.left:
                successor.left.parent = successor

    # непосредственно пересадка поддерева чуть выше - заменяет u на v в дереве, обновляет родителя v.
    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    def _minimum(self, node):
        while node.left:
            node = node.left
        return node

    def print_tree(self):
        if self.root is not None:
            self._print_tree(self.root)
        else:
            print("Дерево пусто.")

    def _print_tree(self, node, prefix="", is_left=True):
        if node.right:
            new_prefix = prefix + ("│   " if is_left else "    ")
            self._print_tree(node.right, new_prefix, False)
        print(prefix + ("└── " if is_left else "┌── ") + str(node.val))
        if node.left:
            new_prefix = prefix + ("    " if is_left else "│   ")
            self._print_tree(node.left, new_prefix, True)

    def add(self, key):
        if self.find(key):
            print(f"Узел со значением {key} уже существует.")
            return False
        self.insert(key)
        print(f"Узел со значением {key} успешно добавлен.")
        return True


if __name__ == "__main__":
    numbers = generate_random_sequence()
    print("Сгенерированная последовательность:", numbers)

    tree = BinaryTree()
    for num in numbers:
        tree.insert(num)

    print("\nБинарное дерево:")
    tree.print_tree()

    while True:
        print("\nВыберите действие:")
        print("1. Добавить узел")
        print("2. Удалить узел")
        print("3. Найти узел")
        print("4. Показать дерево")
        print("5. Выход")
        choice = input("Введите номер действия: ")

        if choice == "1":
            try:
                value = int(input("Введите значение для добавления: "))
                tree.add(value)
            except ValueError:
                print("Ошибка: введите корректное число.")
        elif choice == "2":
            try:
                value = int(input("Введите значение для удаления: "))
                tree.delete(value)
            except ValueError:
                print("Ошибка: введите корректное число.")
        elif choice == "3":
            try:
                value = int(input("Введите значение для поиска: "))
                node = tree.find(value)
            except ValueError:
                print("Ошибка: введите корректное число.")
        elif choice == "4":
            print("\nБинарное дерево:")
            tree.print_tree()
        elif choice == "5":
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод. Пожалуйста, выберите от 1 до 5.")
