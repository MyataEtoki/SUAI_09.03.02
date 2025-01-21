#include <SFML/Graphics.hpp>
#include <iostream>
#include <vector>
#include <cstdlib>
#include <queue>

using namespace std;
/*
struct Island { // ���������� ��� �������(������� ������ ������� �� ���������� �������������)
    int x;
    int y;
};

struct Dragon { // ������ ��� ��������� �������
    int x;
    int y;
};

// ������� ��� ������� ���������� ����� ����� �������
double calculateDistance(int x1, int y1, int x2, int y2) {
    return sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2));
}

// ������� ��� ������ ���������� �������
Island findNearestIsland(Dragon dragon, Island* islands, int numIslands) {
    double minDistance = std::numeric_limits<double>::max();
    Island nearestIsland;

    for (int i = 0; i < numIslands; i++) {
        double distance = calculateDistance(dragon.x, dragon.y, islands[i].x, islands[i].y);
        if (distance < minDistance) {
            minDistance = distance;
            nearestIsland = islands[i];
        }
    }

    return nearestIsland;
}

void markIsland(vector<vector<int>>& map, vector<vector<bool>>& visited, int x, int y) {
    // ��������� ������� ����� � ���������� ������
    if (x < 0 || y < 0 || x >= map[0].size() || y >= map.size() || visited[y][x] || map[y][x] == 0) {
        return;
    }

    visited[y][x] = true;

    // ���������� ��������� �������� ������
    markIsland(map, visited, x + 1, y);
    markIsland(map, visited, x - 1, y);
    markIsland(map, visited, x, y + 1);
    markIsland(map, visited, x, y - 1);
}

void generateMap(vector<vector<int>>& map, int width, int height, int numIslands) {
    vector<Island> islands;

    for (int i = 0; i < numIslands; i++) {
        int x = rand() % width;
        int y = rand() % height;

        map[y][x] = 1;
        Island island = { x, y };
        islands.push_back(island);
    }
}

int main() {
    setlocale(LC_ALL, "Russian");
    int width, height, numIslands, index;
    char direction;

    cout << "������� ������ � ������ �����: ";
    cin >> width >> height;
    cout << "������� ���������� ������ ��� ��������: ";
    cin >> numIslands;

    cout << "������� ����������� � ������ ������, � ������� ��������� ������ [N/S/E/W + �����]: ";
    cin >> direction >> index;
    
    // ����������� ��������� ��������� �������
    Dragon dragon;
    dragon.x = 0;
    dragon.y = 0;

    if (direction == 'W') {
        dragon.y = index;
    }
    else if (direction == 'E') {
        dragon.y = index;
        dragon.x = width - 1;
    }
    else if (direction == 'S') {
        dragon.x = index;
        dragon.y = height - 1;
    }
    else if (direction == 'N') {
        dragon.x = index;
    }
    else {
        cout << "������������ �����������. ����������� N/S/E/W." << endl;
    }

    vector<vector<int>> map(height, vector<int>(width));
    generateMap(map, width, height, numIslands);

    vector<vector<bool>> visited(height, vector<bool>(width, false));
    
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            if (map[y][x] == 1 && !visited[y][x]) {
                markIsland(map, visited, x, y);
            }
        }
    }

    // ��� ��������� ����� � �������������� SFML
    sf::RenderWindow window(sf::VideoMode(width * 10, height * 10), "Generated Map");

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        window.clear(sf::Color::White);

        // ������ ������� �� �����
        sf::RectangleShape islandShape(sf::Vector2f(10, 10));
        islandShape.setFillColor(sf::Color::Green);


        window.clear();

        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                if (map[y][x] == 1) {
                    islandShape.setPosition(x * 10, y * 10); // ������������ ��� �����������
                    window.draw(islandShape);
                }
            }
        }

        // ������ �������
        sf::RectangleShape dragonShape(sf::Vector2f(10, 10));
        dragonShape.setPosition(dragon.x*10, dragon.y*10);
        dragonShape.setFillColor(sf::Color::Red);
        window.draw(dragonShape);

        window.display();
    }

    return 0;
}*/