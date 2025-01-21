#include <iostream>
#include <fstream>
#include <vector>
using namespace std;

int main() {
	int number, i;
	int size_of_array_A;
	vector<int> array_A;
	int size_of_array_B;
	vector<int> array_B;
	int size_of_array_I;
	vector<int> array_I;
	int Helper; // переносит числа

	// считываем данные
	ifstream input_file;
	input_file.open("input_file.txt");
	input_file >> size_of_array_A;
	for (i = 0; i < size_of_array_A; i += 1) {
		input_file >> number;
		array_A.push_back(number);
	}
	input_file >> size_of_array_B;
	for (i = 0; i < size_of_array_B; i += 1) {
		input_file >> number;
		array_B.push_back(number);
	}
	input_file >> size_of_array_I;
	for (i = 0; i < size_of_array_I; i += 1) {
		input_file >> number;
		array_I.push_back(number);
	}
	// перекладывание из А в Helper, из Б в А, из Helper в Б
	for (i = 0; i < size_of_array_I-1; i += 1) { // если просто size_of_array_I - будет ошибка out of range 
		Helper = array_A[array_I[i]];
		array_A[array_I[i]] = array_B[array_I[i]];
		array_B[array_I[i]] = Helper;

	}
	// запись в выходной файл
	ofstream output_file;
	output_file.open("output_file.txt");
	output_file << size_of_array_A << endl;
	for (i = 0; i < size_of_array_A; i += 1) {
		output_file << array_A[i] << " ";
	}
	output_file << endl;
	output_file << size_of_array_B << endl;
	for (i = 0; i < size_of_array_B; i += 1) {
		output_file << array_B[i] << " ";
	}
	output_file << endl;
}