#include <iostream>
#include <vector>
// #include <cstring> // нужна для strlen()
using namespace std;

int main() {
	char numbers[]{ "7  54,3 33 1, 3" };
	char ans[32]{ " " }; // 32 - максимальный размер считываемых чисел, если меньше numbers, будет страшное
	int n, i, counter = 0;
	vector<int> array_of_num;
	int size_array_of_num = 0;
	// cout << strlen(numbers)-1; // 14

	for (i = 0; i < sizeof(numbers); i += 1) //i<strlen(numbers)
	{
		if ((numbers[i] != ' ') and (numbers[i] != ',')) {
			cout << "number: " << numbers[i] << endl;
			ans[counter] = numbers[i];
			cout << " ans: " << ans << endl;;
			counter += 1;
			if ((numbers[i + 1] == ' ') or (numbers[i + 1] == ',') or (numbers[i + 1] == '\0')) {
				// последняя цифра не пушится
				cout << "atoi(ans) :" << atoi(ans) << endl;
				array_of_num.push_back(atoi(ans));
				size_array_of_num += 1;
				counter = 0;
				ans[0] = ' ';
				ans[1] = ' '; // обнуляем 2 символа -> считываем только двухзначные числа
			}
		}
	}

	// вывод массива
	for (i = 0; i < size_array_of_num; i += 1) {
		cout << array_of_num[i] << ',';
	}
	cout << "\b"; // чтобы в конце не было запятой
}