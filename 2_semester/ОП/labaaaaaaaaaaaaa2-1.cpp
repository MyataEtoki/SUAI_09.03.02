#include <iostream>
#include <vector>
using namespace std;

int main(){
	char numbers[]{ "7  54,3 33 1, 3" };
	// char ans[] { "" };
	int n, i, counter = 0;
	vector<int> array_of_num;
	vector<char> ans;
	int size_array_of_num = 0;
	// cout << strlen(numbers)-1; // 14
	
	for (i = 0; i<strlen(numbers) ; i += 1) {
		if ((numbers[i]!=' ') and (numbers[i] != ',')) {			
			cout << "number: " << numbers[i];
			// ans[counter] = numbers[i]; // тут всё ломается - пытаюсь сделать чтобы считывало более чем однозначные числа
			// cout << " ans: " << ans;
			counter += 1;
			if ((numbers[i + 1] == ' ') or (numbers[i + 1] == ',')) {
				// array_of_num.push_back(atoi(ans));
				for (n = 0; n < counter; counter = counter - 1) {
					ans.push_back(numbers[i-counter]);
				}
				array_of_num.push_back(atoi(ans));
				// array_of_num.push_back(atoi(ans));
				size_array_of_num += 1;
				counter = 0;
			}
		}
	}

	// вывод массива
	for (i = 0; i < size_array_of_num; i += 1) {
		cout << array_of_num[i] << ',';
	}
} 