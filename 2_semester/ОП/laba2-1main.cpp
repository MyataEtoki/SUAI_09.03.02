#include <iostream>
#include <vector>
using namespace std;

int main(){
	char numbers[] {"7  54,3 33 1, 3"} ;
	char ans[] {""};
	int i;
	vector<int> array_of_num;
	int size_array_of_num = 0;
	// cout << strlen(numbers)-1; // 14
	
	for (i = 0; i<strlen(numbers)-2 ; i += 1) {
		if ((numbers[i]!=' ') and (numbers[i] != ',')) {
			ans += numbers[i];
			cout << " ha-tfu " << ans;
			if ((numbers[i + 1] == ' ') or (numbers[i + 1] == ',')) {
				array_of_num.push_back(int(ans));
				size_array_of_num += 1;
				ans = "";
			}
		}
	}

	// ����� �������
	for (i = 0; i < size_array_of_num; i += 1) {
		cout << array_of_num[i] << ',';
	}
} 