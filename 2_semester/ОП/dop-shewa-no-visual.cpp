#include <iostream>
#include <vector>
#include <cmath>

// ��������� ��� �������� ��������� ������
struct Point {
    int x, y;

    Point(int x, int y) : x(x), y(y) {}
};

// ������� ��� �������� ���������� ����� ����� �������
double distance(const Point& p1, const Point& p2) {
    return sqrt(pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2));
}

// ������� ��� ���������� ���������� �������
Point findNearestIsland(const Point& currentPos, std::vector<std::vector<char>>& grid) {
    Point nearestIsland(-1, -1);
    double minDistance = std::numeric_limits<double>::infinity();

    for (int i = 0; i < grid.size(); ++i) {
        for (int j = 0; j < grid[0].size(); ++j) {
            if (grid[i][j] == '1') {
                Point island(i, j);
                double dist = distance(currentPos, island);
                if (dist < minDistance) {
                    minDistance = dist;
                    nearestIsland = island;
                }
            }
        }
    }

    return nearestIsland;
}

// ������� ��� ������ ������������� ������� � �����
void printDragonAndMap(int dragonSize, Point currentPos, std::vector<std::vector<char>>& map) {
    std::cout << "�������������� �������:" << std::endl;
    std::cout << "������ �������: " << dragonSize << std::endl;
    std::cout << "������� ��������� �������: (" << currentPos.x << ", " << currentPos.y << ")" << std::endl;

    std::cout << "����� ����� �������� �������:" << std::endl;
    for (int i = 0; i < map.size(); ++i) {
        for (int j = 0; j < map[0].size(); ++j) {
            std::cout << map[i][j] << " ";
        }
        std::cout << std::endl;
    }
}

// �������� ������� ��� �������� �������
void dragonActions(int dragonSize, Point dragonStart, std::vector<std::vector<char>>& grid) {
    Point currentPos = dragonStart;

    while (true) {
        Point nearestIsland = findNearestIsland(currentPos, grid);

        if (nearestIsland.x == -1) {
            std::cout << "������ �������� �����." << std::endl;
            break;
        }

        double distanceToIsland = distance(currentPos, nearestIsland);

        currentPos = nearestIsland;

        grid[currentPos.x][currentPos.y] = '0'; // ���������� �������
        dragonSize++; // ���������� ������� �������

        std::cout << "������ ��������� ������ �� ������� (" << currentPos.x << ", " << currentPos.y << ")." << std::endl;
    }

    // ����� ���������� �������� �������
    printDragonAndMap(dragonSize, currentPos, grid);
}

int main() {
    setlocale(LC_ALL, "Russian");
    std::vector<std::vector<char>> map = {
        {'1', '0', '0', '0', '0'},
        {'1', '0', '1', '1', '1'},
        {'0', '0', '0', '1', '0'},
        {'0', '1', '1', '0', '0'},
        {'0', '0', '0', '0', '0'}
    };

    // ��������� ������ �������
    int dragonSize = 5;
    Point dragonStart(0, 0);

    dragonActions(dragonSize, dragonStart, map);

    return 0;
}