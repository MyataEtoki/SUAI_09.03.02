#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <iostream>

// ������� ���������� ���������� ��������
void mergeSort(int* a, int left, int right) {
    if (left == right) return; // ������� ����������
    int mid = (left + right) / 2; // ���������� �������� ������������������
    // � ���������� �������� ������� ���������� ��� ������ ��������
    mergeSort(a, left, mid);
    mergeSort(a, mid + 1, right);
    int start_first_way = left;  // ������ ������� ����
    int start_second_way = mid + 1; // ������ ������� ����
    int* tmp = (int*)malloc(right * sizeof(int)); // �������������� ������
    for (int step = 0; step < right - left + 1; step++) // ��� ���� ��������� ��������������� �������
    {
        // ���������� � ����������� ������������������ ������� �� ��������� ���� �����
        // ��� ������� ������� ���� ���� start_second_way > right
        if ((start_second_way > right) || ((start_first_way <= mid) && (a[start_first_way] < a[start_second_way]))) {
            tmp[step] = a[start_first_way];
            start_first_way++;
        }
        else {
            tmp[step] = a[start_second_way];
            start_second_way++;
        }
    }
    // ������������ �������������� ������������������ � �������� ������
    for (int step = 0; step < right - left + 1; step++) {
        a[left + step] = tmp[step];
    }
}

#define SIZE 8
int main() {
    int a[SIZE] = {9,8,7,6,5,4,3,2};
    // ��������� �������� �������
    /*
    for (int i = 0; i < SIZE; i++)
    {
        a[i] = (rand() % 100);
        printf(" %d ", a[i]);
    } 
    std::cout <<std::endl; */
    clock_t cltimeStart = clock();
    mergeSort(a, 0, SIZE - 1); // �������� ������� ����������
    // ������� ��������������� ������
    clock_t cltimeEnd = clock();
    for (int i = 0; i < SIZE; i++) {
        printf(" %d ", a[i]);
    }
    
    double durationCL = ((double)cltimeEnd - cltimeStart) / (double) CLOCKS_PER_SEC;
    std::cout << std::endl << "SIZE: " << SIZE << std::endl << "TIME: " << durationCL;
    return 0;
}