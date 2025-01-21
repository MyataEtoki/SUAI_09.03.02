#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define N 12
int bacteria( int K1, int K2, int D, int T, int Pm, int Pp) {
    int field[N][N];
    int days = 0;
    int num_bacteria = rand() % (K2 - K1 + 1) + K1;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            field[i][j] = 0;
        }
    }
    for (int d = 0; d < D; d++) {
        days++;
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                if (field[i][j] == 0) {
                    field[i][j] = rand() % (num_bacteria * 2) + 1;
                }
            }
        }
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                if (field[i][j] == 1) {
                    if (rand() % 100 < Pp ) {
                        int neighbor[8][2];
                        int n;
                        for (n = 0; n < 8; n++) {
                            neighbor[n][0] = i + 1;
                            neighbor[n][1] = j + 1;
                        }
                        for (int k = 0; k < n; k++) {
                            if (field[neighbor[k][0]][neighbor[k][1]] == 0) {
                                field[neighbor[k][0]][neighbor[k][1]] = rand() % (num_bacteria * 2) + 1;
                            }
                        }
                    }
                }
                else if (field[i][j] > 1 && rand() % 100 < Pm ) {
                    field[i][j] = 0;
                }
            }
        }
    }
    return days;
}

int main() {
    srand(time(NULL));
    // int N = 12;
    int K1 = 1;
    int K2 = 10;
    int D = 7;
    int T = 14;
    int Pp = 0.05;
    int Pm = 0.02;
    for (int i = 0; i < 10000; i++) {
        int days = bacteria(K1, K2, D, T, Pp, Pm);
        printf("%d\n", days);
    }
    return 0;
}