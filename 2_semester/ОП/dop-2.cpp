#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <map>

using namespace std;

struct Person { // Инфа на человека
    string name; // Имя
    double expenses; // Общие расходы
    vector<string> not_involved; // Люди, не вовлеченные в трату
    vector<string> involved; // Люди, вовлеченные в трату
    double true_expenses = 0; // Фактические расходы
    map<string, double> debts; // Ему должны - кто и сколько
};

// Вычисляем фактические траты и долги
void calculateTrueExpenses(vector<Person>& persons, int total_people) {
    for (auto& person : persons) { // Для каждого человека в списке persons

        // Вычисляем, на сколько нужно поделить трату - количество вовлеченных людей
        int num_involved = total_people - person.not_involved.size();
        // Вычисляем трату на человека
        double split_expenses = person.expenses / num_involved;

        // Распределяем фактическую трату
        for (auto& involved_person : person.involved) { // Для каждого вовлеченного человека
            for (auto& p : persons) { // Для каждого обычного человека
                if (involved_person == p.name) { // Если текущий человек в списке совпадает с вовлеченным
                    p.true_expenses += split_expenses; // Увеличиваем его фактические расходы
                }
            }
        }

        for (auto& involved_person : person.involved) { // Для каждого вовлеченного человека
            for (auto& p : persons) { // Для каждого обычного человека
                if ((involved_person == p.name) && (involved_person != person.name)) { // Если вовлеченный обычный человек не является текущим рассматриваемым человеком
                    person.debts[involved_person] += split_expenses; // Добавляем его в список должников с необходимой суммой
                }
            }
        }
    }
}

int main() {
    setlocale(LC_ALL, "Russian"); // Отображение кириллицы в консоли
    ifstream inputFile("participant.txt");// Открываем файл для чтения

    if (!inputFile.is_open()) { // Если файл не удалось открыть
        cerr << "Не удалось открыть файл." << endl; // Выводим сообщение об ошибке
        return 1;
    }

    int num_people; // Количество людей
    string line; // Строка для считывания данных из файла
    getline(inputFile, line, '/'); // Считываем количество людей
    istringstream num_people_stream(line.substr(line.find(":") + 1, line.find("/") - line.find(":") - 1)); // Создаем поток для считывания числа людей
    num_people_stream >> num_people; // Записываем количество людей

    // Считываем список людей
    getline(inputFile, line);

    // Создаем массив для хранения людей
    vector<string> people;
    istringstream people_stream(line.substr(line.find(":") + 1));

    while (getline(people_stream, line, ',')) { // Пока есть имена в строке
        people.push_back(line); // Добавляем их в массив людей
    }

    vector<Person> persons; // Информация о людях

    // Считываем информацию о расходах каждого человека
    while (getline(inputFile, line)) { // Считываем данные для каждого человека
        Person p; // временная структура информации на человека

        string not_involved_str; // Строка не вовлеченных людей
        istringstream iss(line); // Поток для разбора строки
        iss >> p.name; // Считываем имя
        iss.ignore(100, ':'); // Игнорируем символы до двоеточия
        iss >> p.expenses; // Считываем расходы
        iss.ignore(100, '/'); // Игнорируем символы до слэша
        getline(iss, not_involved_str); // Считываем строку с не вовлеченными людьми

        istringstream not_involved_stream(not_involved_str); // Поток для строки не вовлеченных людей

        while (getline(not_involved_stream, line, ',')) { // Пока есть имена в строке не вовлеченных
            p.not_involved.push_back(line); // Добавляем их в список
        }

        persons.push_back(p); // Добавляем структуру в итоговый массив людей
    }

    // Вывод информации на экран
    cout << "Количество людей в компании: " << num_people << endl;
    cout << "Список людей: ";
    for (const auto& person : people) {
        cout << person << " ";
    }
    cout << endl; 

    // Вычисляем вовлеченных людей
    for (auto& person : persons) { // Проходим по каждому человеку (нужен его список невовлечённых людей)
        for (const auto& involved_person : persons) { // Проверяем каждого человека на вовлеченность в трату
            if (person.name != involved_person.name) { // Проверяем, не является ли человек сам собой
                bool is_not_involved = true; // по-дефолту считаем вовлечённым (скажи нет презумции невиновности)
                for (const auto& not_involved_person : person.not_involved) { // Для каждого не вовлеченного
                    if (not_involved_person == involved_person.name) { // Если текущий не вовлеченный совпадает с проверяемым человеком
                        is_not_involved = false; // Снимаем флаг не вовлечения
                        break; // Прерываем цикл
                    }
                }
                if (is_not_involved) { // Если оказалось, что человек вовлечен
                    person.involved.push_back(involved_person.name); // Добавляем его в список вовлеченных
                }
            }
        }
    }
    for (auto& person : persons) { // Для каждого человека
        person.involved.push_back(person.name); // Добавляем его самого в его список вовлеченных
    }

    // Вычисляем фактические траты
    cout << endl;
    calculateTrueExpenses(persons, num_people);

    // Печать фактических трат каждого человека
    for (const auto& person : persons) { // Для каждого человека в списке
        cout << "Фактические траты для " << person.name << ": " << person.true_expenses << endl; // Выводим фактические затраты
        for (const auto& pair : person.debts) { // Для каждой пары(элемента) словаря долгов
            cout << pair.first << " должен " << person.name << ": " << pair.second << endl; // Выводим информацию о долгах
        }
        cout << endl;
    }

    inputFile.close(); // Закрываем файл
    return 0; // Возвращаем успешный код завершения программы
}