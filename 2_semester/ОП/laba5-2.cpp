#include <iostream>
#include <vector>

// Функция для записи кодовых слов в битовую последовательность
std::string writeCodeWords(const std::vector<unsigned int>& codeWords, const std::vector<int>& codeWordLengths, const std::vector<int>& inputSequence) {
    std::string result; // Переменная для хранения результирующей битовой последовательности

    for (const auto& index : inputSequence) { // Для каждой последовательности индексов
            // Получаем кодовое слово по индексу
            unsigned int codeWord = codeWords[index]; // Получаем кодовое слово по текущему индексу
            int length = codeWordLengths[index]; // Получаем длину кодового слова

            // Проходим по каждому биту кодового слова и добавляем его к результату
            for (int i = 0; i < length; ++i) { // Проход по каждому биту кодового слова
                // Определяем текущий бит и добавляем его к результату
                int bit = (codeWord >> (length - i - 1)) & 1; // Получаем текущий бит кодового слова - смещаем число вправо на (length - i - 1) разрядов
                result.push_back('0' + bit); // Добавляем текущий бит к выходной строке (преобразование в string)
            }
    }

    return result; // Возвращаем битовую последовательность
}

int main() {
    std::vector<unsigned int> codeWords = { 0b01, 0b100, 0b1011, 0b1101, 0b111101100 }; // CT - Кодовые слова в бинарном виде
    std::vector<int> codeWordLengths = { 2, 3, 4, 4, 9 }; // Длины каждого кодового слова

    std::vector<int> inputSequence = { 1, 0, 0, 0, 2, 1, 4, 3, 2, 0, 0, 1 }; // M - Последовательность индексов кодовых слов

    std::string result = writeCodeWords(codeWords, codeWordLengths, inputSequence); // Получаем битовую последовательность кодовых слов

    // Разделяем результат на группы по 8 бит для удобства чтения
    for (size_t i = 0; i < result.size(); i += 8) { // Проход по результату с шагом 8 для группировки по 8 бит
        std::cout << result.substr(i, 8) << " "; // Выводим очередную группу бит
    }
    std::cout << std::endl;

    return 0;
}