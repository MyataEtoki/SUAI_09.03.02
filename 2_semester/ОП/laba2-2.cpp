#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <cmath>

using namespace std;
//вычисляем хэш
int computeHash(string s, int P, int M) { 
    int hash_val = 0;//хэш
    int i = 0;//степень P
    for (char c : s) {//для каждого символа с в строке s
        //hash_val = (hash_val * P + c) % M; //формула из методы
        hash_val += + c*pow(P, i);  //формула из методы
        i++;
    }
    return hash_val%M;
}

void checkHashCollisions(string s, int P, int M) {
    int n = s.size(); //количество элементов
    int total_subsets = pow(2, n); //количество возможных подмножеств, если исходное множество из n элементов.
    unordered_map<int, vector<string>> hash_to_strings; //словарь хэшей и соответствующих им подстрок.

    for (int i = 1; i < total_subsets; i++) { //находим все подмножества - проходим числа от 0 до 2^n - 1, где n - это длина входной строки.
        string subset = ""; //подстрока
        for (int j = 0; j < n; j++) { //проходимся по каждому символу входной строки
            if (i & (1 << j)) { //проверяется, установлен ли j-й бит в числе i (является ли j-й элемент частью текущего подмножества)
                subset += s[j];
            }
        }
        int hash_val = computeHash(subset, P, M); //вычисленный хэш
        hash_to_strings[hash_val].push_back(subset);
    }

    bool found = false; //отслеживаем были ли найдены подстроки с одинаковыми хешами
    for (auto entry : hash_to_strings) { //проходим по каждому элементу словаря (ключ:вектор с подстроками)
        if (entry.second.size() > 1) { //entry содержит пару ключ:вектор -> смотрим второе, размер вектора.
            found = true;
            cout << entry.first << " : ["; //выводим хэш:[подстроки]
            for (int i = 0; i < entry.second.size(); i++) {//идём по каждой подстроке
                cout << "\"" << entry.second[i] << "\"";//выводим каждую подстроку с одинаковым хэшем
                if (i < entry.second.size() - 1) {//после каждой не последней подстроки, ставим запятую
                    cout << ", ";
                }
            }
            cout << "]" << endl;
        }
    }

    if (!found) { //если подстроки с одинаковыми хешами не найдены, выводим false
        cout << "false" << endl;
    }
}

int main() {
    int P = 3; //основание хэша
    int M = 10; //модуль
    string S = "aabc";

    checkHashCollisions(S, P, M);
    return 0;
}