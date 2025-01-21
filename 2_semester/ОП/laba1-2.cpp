#include <iostream>
#include <cmath> 
using namespace std;

int main() {
	float N;
	cout << "Input N: ";
	cin >> N;
	int x;
	cout << "Input x: ";
	cin >> x;
	float answer = 0.0;
	float K;
	int i = 2;
	do {
		K = pow(x, N) - float(pow(x, i));
		answer = answer + (((i * i) + x) * (K + ((i - 1) / float(pow(x, i - 1)))));
		i += 2;
	} while (i <= N);
	cout << answer;
	return 0;
}
