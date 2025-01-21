import random
from math import gcd
from sympy import isprime

# Генерация простого числа заданной битности
def generate_large_prime(length):

    while True:
        candidate = random.getrandbits(length) | 1  # Генерируем нечетное число
        if isprime(candidate):
            return candidate


def generate_keypair(p, q):
    # p и q - простые числа (генерация выше)
    n = p * q # модуль rsa
    # Вычисление функции Эйлера
    phi = (p - 1) * (q - 1)

    # Проверка на взаимную простоту
    def is_coprime(e, phi):
        return gcd(e, phi) == 1 # НОД

    e = 65537  # Обычно выбирается простое число 65537
    if not is_coprime(e, phi):
        raise ValueError("e не является взаимно простым с phi(n)")

    # Вычисление закрытой экспоненты d
    d = pow(e, -1, phi)

    return ((e, n), (d, n))



# Шифрование сообщения на основе открытого ключа
def encrypt(pk, plaintext):
    numbers = [ord(char) for char in plaintext]
    ciphertext = [pow(num, pk[0], pk[1]) for num in numbers]
    return ciphertext


# Расшифровка сообщения на основе закрытого ключа
def decrypt(sk, ciphertext):
    plaintext_numbers = [pow(c, sk[0], sk[1]) for c in ciphertext]
    message = ''.join(chr(num) for num in plaintext_numbers)
    return message


def main():
    print("Добро пожаловать в программу шифрования RSA! 😊")

    public_key, private_key = None, None

    while True:
        print("\nВыберите опцию:")
        print("1. Сгенерировать ключи")
        print("2. Ввести открытый ключ вручную")
        print("3. Ввести закрытый ключ вручную")
        print("4. Зашифровать сообщение")
        print("5. Расшифровать сообщение")
        print("6. Выход")

        choice = input("Ваш выбор: ")

        if choice == '1':

            length = int(input("Введите длину простых чисел в битах: "))
            p = generate_large_prime(length)
            q = generate_large_prime(length)
            public_key, private_key = generate_keypair(p, q)
            print("Открытый ключ:", public_key)
            print("Закрытый ключ:", private_key)

        elif choice == '2':
            e = int(input("Введите значение e: "))
            n = int(input("Введите значение n: "))
            public_key = (e, n)
            print("Открытый ключ установлен:", public_key)

        elif choice == '3':
            d = int(input("Введите значение d: "))
            n = int(input("Введите значение n: "))
            private_key = (d, n)
            print("Закрытый ключ установлен:", private_key)

        elif choice == '4':
            if public_key is None:
                print("Сначала сгенерируйте или введите открытый ключ! 🔑")
                continue
            message = input("Введите сообщение для шифрования: ")
            encrypted_message = encrypt(public_key, message)
            print("Зашифрованное сообщение:", encrypted_message)

        elif choice == '5':
            if private_key is None:
                print("Сначала сгенерируйте или введите закрытый ключ! 🔑")
                continue
            ciphertext_input = input("Введите зашифрованное сообщение (список чисел, разделенных запятыми): ")
            ciphertext = list(map(int, ciphertext_input.split(',')))
            decrypted_message = decrypt(private_key, ciphertext)
            print("Расшифрованное сообщение:", decrypted_message)

        elif choice == '6':
            print("Выход из программы. Всего хорошего! 👋")
            break

        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
