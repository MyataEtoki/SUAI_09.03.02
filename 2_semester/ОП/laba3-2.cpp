#include <iostream>
#include <vector>
#include <cmath>
using namespace std;

// �������� �� ������� �� ����� ������� �� ������� ���� NxM
bool isValidMove(int x, int y, int N, int M) {
    return (x >= 0 && y >= 0 && x < N && y < M);
}

// ���������� ����������� ����������� ��������� 2-� �����
vector<pair<int, int>> findShortestIntersection(int a1, int b1, int a2, int b2, vector<vector<int>>& T1, vector<vector<int>>& T2, int N, int M, int moves, int& recursion_counter) {
    static vector<pair<int, int>> path1, path2, shortestIntersection;
    static int minMoves = INT_MAX;//��� ����� ����������� - ��� ����� ������� �����
    recursion_counter++;
    if (recursion_counter >= 965) { cout << "Recursion's depth is too big" << endl; }
    if (a1 == a2 && b1 == b2 && moves < minMoves) { //�������� �� 2 ������ ���������� ���������, 
        // � ��� ���� ���������� ����� ������, ��� ������� ����������� ���������� ����� �� �����������
        minMoves = moves; //���������� ����� ����������� ���-�� �����
        shortestIntersection = path1; //� ���������� ����
        return shortestIntersection;
    }

    if (moves >= minMoves) {//���� ��� ����� ��� ������, ��� ����������� ��� ���������, �� ������ ���� �� ����� ���� ������ ���
        return shortestIntersection; //���������� �����������
    }

    for (const auto& move1 : T1) { //����, � ������� ������������ ��� ��������� ���� ��� ������ ������ �� ������� � ������ T1.
        int new_a1 = a1 + move1[0]; //����� ���������� ��� ������ ������ ����� ���������� ����.
        int new_b1 = b1 + move1[1]; //move1 - ���� �� ��� �������� � ������� ����
        //cout << move1[0] << " " << move1[1] << endl;
        cout << "Resursion number(from end) - " << recursion_counter << " Point 1 - " << new_a1 << ";" << new_b1 << " minMoves - " << minMoves << endl;
        if (isValidMove(new_a1, new_b1, N, M)) { //�� ������� �� ����� ������� �� ������� �����
            path1.push_back({ new_a1, new_b1 }); //����������� ����� ������� 1 ������ � �� ����
            for (const auto& move2 : T2) { //����, � ������� ������������ ��� ��������� ���� ��� ������ ������ �� ������� � ������ T2.
                int new_a2 = a2 + move2[0]; //����� ���������� ��� ������ ������ ����� ���������� ����.
                int new_b2 = b2 + move2[1];
                cout << "Resursion number(from end) - " << recursion_counter << " Point 2 - " << new_a2 << ";" << new_b2 << " minMoves - " << minMoves << endl;
                if (isValidMove(new_a2, new_b2, N, M)) { //�� ������� �� ����� ������� �� ������� �����
                    path2.push_back({ new_a2, new_b2 });
                    findShortestIntersection(new_a1, new_b1, new_a2, new_b2, T1, T2, N, M, moves + 1, recursion_counter); //������� ���� 2-� ����� � ������������ ������������
                    path2.pop_back(); //����� � ���������� ������� � ���� 2 ������

                }
            }
            path1.pop_back(); //����� � ���������� ������� � ���� 1 ������
        }
    }

    return shortestIntersection;
}

int main() {
    int N = 4, M = 4, a1 = 0, a2 = 0, b1 = 3, b2 = 1, recursion_counter = 0;
    vector<vector<int>> T1{ {2, -1}, {-2, 1}, {1, 2}, {-1, -2} };
    vector<vector<int>> T2{ {2, -1}, {-2, 1}, {1, 2}, {-1, -2} };
    vector<pair<int, int>> shortestIntersection = findShortestIntersection(a1, a2, b1, b2, T1, T2, N, M, 0, recursion_counter);

    // cout << "Kratchayshee peresechenie 2-h figur: ";
    for (const auto& point : shortestIntersection) {
        cout << "[" << point.first << "," << point.second << "] ";
    }

    return 0;
}