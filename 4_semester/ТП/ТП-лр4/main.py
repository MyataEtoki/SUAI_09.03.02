import random

numbers = [int(x) for x in str(random.random())[2::]]
print(numbers)

# класс для узлов
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

# добавить узел
def insert(root, key):
    if root is None:
        return Node(key)
    else:
        if key < root.val:
            root.left = insert(root.left, key)
        else:
            root.right = insert(root.right, key)
    return root

# удалить узел
def delete(key):

# найти узел - тупой обход дерева
def find(root, key):
    if key < root.val:
        find(root.left, key)
    elif key > root.val:
        find(root.right, key)
    elif key == root.val:
        return 


# странный вывод, ПЕРЕДЕЛАТЬ
def print_tree(root, level=0, prefix="Root: "):
    if root is not None:
        print(" " * (level * 4) + prefix + str(root.val))
        if root.left is not None or root.right is not None:
            print_tree(root.left, level + 1, "L--- ")
            print_tree(root.right, level + 1, "R--- ")


def build_tree_from_array(arr):
    root = None
    for num in arr:
        root = insert(root, num)
    return root


# Пример использования
if __name__ == "__main__":

    # Построение дерева
    tree_root = build_tree_from_array(numbers)

    # Вывод дерева в консоль
    print("Бинарное дерево:")
    print_tree(tree_root)
