#include <iostream>
#include <vector>
#include <chrono>

using namespace std;
using namespace chrono;

//считаем максимальную прибыль
double calcMaxProfit(const vector<double>& sellPrices, const vector<double>& buyPrices, int currentIndex, bool haveMoney, double currentProfit) {
    //если текущий день - последний, фиксируем прибыль
    if (currentIndex == sellPrices.size()) {
        return currentProfit;
    }

    //если валюта присутствуют
    if (haveMoney) {
        return max(
            //переходим в следующий день
            calcMaxProfit(sellPrices, buyPrices, currentIndex + 1, false, currentProfit + sellPrices[currentIndex]), //продаем и обновляем прибыль(увеличилась), валюты нет
            calcMaxProfit(sellPrices, buyPrices, currentIndex + 1, true, currentProfit) //или ничего не делаем, ещё валюта есть
        );
    }

    //если валюты нет
    else {
        return max(
            //переходим в следующий день
            calcMaxProfit(sellPrices, buyPrices, currentIndex + 1, true, currentProfit - buyPrices[currentIndex]), //покупаем 
            //и обновляем прибыль(уменьшилась на цену покупки), валюта теперь есть
            calcMaxProfit(sellPrices, buyPrices, currentIndex + 1, false, currentProfit) //или ничего не делаем, валюты всё ещё нет
        );
    }
}

//считаем время и выводим прибыль
void calcMaxProfitAndTime(const vector<double>& sellPrices, const vector<double>& buyPrices) {
    auto startTime = high_resolution_clock::now();

    double totalProfit = calcMaxProfit(sellPrices, buyPrices, 0, false, 0);

    auto stopTime = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stopTime - startTime);

    cout << "Максимальная прибыль: " << totalProfit << endl;
    cout << "Время работы программы: " << duration.count() << " микросекунд " << endl;
}

int main() {
    setlocale(LC_ALL, "Russian");
    //индекс в массиве - номер дня, дни считаются с 0.
    vector<double> sellPrices = { 10, 25, 39, 14, 3, 21, 36, 9, 18, 27}; //цены продажи
    vector<double> buyPrices = { 5, 18, 31, 9, 23, 36, 12, 26, 39, 7 }; //цены покупки

    calcMaxProfitAndTime(sellPrices, buyPrices);

    return 0;
}