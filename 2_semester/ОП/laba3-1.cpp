#include <iostream>
#include <vector>;
using namespace std;


void numeral_to_numbers(int numeral, int depth, vector<int> &numbers) {
    if (numeral < 10) {
        // первая цифра числа
        numbers.push_back(numeral);
        cout << "(Final)Recursion's depth: " << depth << "; Numeral = " << numeral << "; In numbers: " << numbers.size() << " numbers!" << endl;
    } else {
        numeral_to_numbers(numeral / 10, depth+1, numbers); // рекурсивный вызов функции для оставшихся цифр числа, число с каждым вызовом функции уменьшается на разряд
        numbers.push_back(numeral%10);
        cout << "Recursion's depth: " << depth << "; Numeral = " << numeral << "; In numbers: " << numbers.size() << " numbers!" << endl;
    }
}

int main() {
    int numeral; // число
    int depth = 1; // глубина рекурсии
    vector<int> numbers; // цифры
    cout << "Input numeral: ";
    cin >> numeral;

    numeral_to_numbers(numeral, depth, numbers);
    cout << "Every number of numeral: {";
    for (int i = 0; i < numbers.size(); i += 1) {
        cout << numbers[i] << ',';
    }
    cout << "\b" << "}";
    return 0;
}