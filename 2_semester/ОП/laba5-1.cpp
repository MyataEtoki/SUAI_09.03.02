#include <iostream>
#include <bitset>

// Функция для инвертирования K битов начиная с T бита
void invertBits(int& data, int N, int K, int T) {
    // Маска для выделения битов, которые нужно инвертировать
    int mask = ((1 << K) - 1) << (N - T - K); // включая K бит, начиная с T
    // 1 сдвигаем влево на K - 2 в степени K, -1 чтобы все биты до K-того  были 1-цами, 
    // получ. бит. последоват. сдвигаем влево на N-T-K позиций - начало инвертир. будет на T-той позиции
    // Инвертируем биты с помощью XOR с маской
    data ^= mask;
}

#define BITSOV 8
int main() {
    int N = BITSOV;
    int data = 0b11101010; // исходная битовая последовательность
    int K = 3; //инвертировать K битов
    int T = 1; //начиная с T бита (начало индексации - 0)

    // Выводим исходные данные
    std::cout << "Input:\n";
    std::bitset<BITSOV> bits(data);
    std::cout << bits << '\n';

    // Инвертируем биты
    invertBits(data, N, K, T);

    // Выводим измененные данные
    std::cout << "Output:\n";
    bits = data;
    std::cout << bits << '\n';

    return 0;
}