#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <map>

using namespace std;

struct Person { // ���� �� ��������
    string name; // ���
    double expenses; // ����� �������
    vector<string> not_involved; // ����, �� ����������� � �����
    vector<string> involved; // ����, ����������� � �����
    double true_expenses = 0; // ����������� �������
    map<string, double> debts; // ��� ������ - ��� � �������
};

// ��������� ����������� ����� � �����
void calculateTrueExpenses(vector<Person>& persons, int total_people) {
    for (auto& person : persons) { // ��� ������� �������� � ������ persons

        // ���������, �� ������� ����� �������� ����� - ���������� ����������� �����
        int num_involved = total_people - person.not_involved.size();
        // ��������� ����� �� ��������
        double split_expenses = person.expenses / num_involved;

        // ������������ ����������� �����
        for (auto& involved_person : person.involved) { // ��� ������� ������������ ��������
            for (auto& p : persons) { // ��� ������� �������� ��������
                if (involved_person == p.name) { // ���� ������� ������� � ������ ��������� � �����������
                    p.true_expenses += split_expenses; // ����������� ��� ����������� �������
                }
            }
        }

        for (auto& involved_person : person.involved) { // ��� ������� ������������ ��������
            for (auto& p : persons) { // ��� ������� �������� ��������
                if ((involved_person == p.name) && (involved_person != person.name)) { // ���� ����������� ������� ������� �� �������� ������� ��������������� ���������
                    person.debts[involved_person] += split_expenses; // ��������� ��� � ������ ��������� � ����������� ������
                }
            }
        }
    }
}

int main() {
    setlocale(LC_ALL, "Russian"); // ����������� ��������� � �������
    ifstream inputFile("participant.txt");// ��������� ���� ��� ������

    if (!inputFile.is_open()) { // ���� ���� �� ������� �������
        cerr << "�� ������� ������� ����." << endl; // ������� ��������� �� ������
        return 1;
    }

    int num_people; // ���������� �����
    string line; // ������ ��� ���������� ������ �� �����
    getline(inputFile, line, '/'); // ��������� ���������� �����
    istringstream num_people_stream(line.substr(line.find(":") + 1, line.find("/") - line.find(":") - 1)); // ������� ����� ��� ���������� ����� �����
    num_people_stream >> num_people; // ���������� ���������� �����

    // ��������� ������ �����
    getline(inputFile, line);

    // ������� ������ ��� �������� �����
    vector<string> people;
    istringstream people_stream(line.substr(line.find(":") + 1));

    while (getline(people_stream, line, ',')) { // ���� ���� ����� � ������
        people.push_back(line); // ��������� �� � ������ �����
    }

    vector<Person> persons; // ���������� � �����

    // ��������� ���������� � �������� ������� ��������
    while (getline(inputFile, line)) { // ��������� ������ ��� ������� ��������
        Person p; // ��������� ��������� ���������� �� ��������

        string not_involved_str; // ������ �� ����������� �����
        istringstream iss(line); // ����� ��� ������� ������
        iss >> p.name; // ��������� ���
        iss.ignore(100, ':'); // ���������� ������� �� ���������
        iss >> p.expenses; // ��������� �������
        iss.ignore(100, '/'); // ���������� ������� �� �����
        getline(iss, not_involved_str); // ��������� ������ � �� ������������ ������

        istringstream not_involved_stream(not_involved_str); // ����� ��� ������ �� ����������� �����

        while (getline(not_involved_stream, line, ',')) { // ���� ���� ����� � ������ �� �����������
            p.not_involved.push_back(line); // ��������� �� � ������
        }

        persons.push_back(p); // ��������� ��������� � �������� ������ �����
    }

    // ����� ���������� �� �����
    cout << "���������� ����� � ��������: " << num_people << endl;
    cout << "������ �����: ";
    for (const auto& person : people) {
        cout << person << " ";
    }
    cout << endl; 

    // ��������� ����������� �����
    for (auto& person : persons) { // �������� �� ������� �������� (����� ��� ������ ������������� �����)
        for (const auto& involved_person : persons) { // ��������� ������� �������� �� ������������� � �����
            if (person.name != involved_person.name) { // ���������, �� �������� �� ������� ��� �����
                bool is_not_involved = true; // ��-������� ������� ����������� (����� ��� ��������� ������������)
                for (const auto& not_involved_person : person.not_involved) { // ��� ������� �� ������������
                    if (not_involved_person == involved_person.name) { // ���� ������� �� ����������� ��������� � ����������� ���������
                        is_not_involved = false; // ������� ���� �� ����������
                        break; // ��������� ����
                    }
                }
                if (is_not_involved) { // ���� ���������, ��� ������� ��������
                    person.involved.push_back(involved_person.name); // ��������� ��� � ������ �����������
                }
            }
        }
    }
    for (auto& person : persons) { // ��� ������� ��������
        person.involved.push_back(person.name); // ��������� ��� ������ � ��� ������ �����������
    }

    // ��������� ����������� �����
    cout << endl;
    calculateTrueExpenses(persons, num_people);

    // ������ ����������� ���� ������� ��������
    for (const auto& person : persons) { // ��� ������� �������� � ������
        cout << "����������� ����� ��� " << person.name << ": " << person.true_expenses << endl; // ������� ����������� �������
        for (const auto& pair : person.debts) { // ��� ������ ����(��������) ������� ������
            cout << pair.first << " ������ " << person.name << ": " << pair.second << endl; // ������� ���������� � ������
        }
        cout << endl;
    }

    inputFile.close(); // ��������� ����
    return 0; // ���������� �������� ��� ���������� ���������
}