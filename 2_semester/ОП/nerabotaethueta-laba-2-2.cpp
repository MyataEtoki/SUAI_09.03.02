#include <iostream>
#include <math.h>
#include <iostream>
#include <vector>
#include <string>
#include <set>
using namespace std;
/*
void hash(string str, vector<int> &hashs) {
    int p = 3, m = 10, n = 0;
    int hash=0;
    for(int i=0; i<str.size();i++) {
        hash+= str[i]*pow(p, n);       
        n++;
    }
    hash = hash%m;
    hashs.push_back(hash); // в итоге имеем массив хэшей
} */

int hashs(string str) {
    int p = 3, m = 10, n = 0;
    int hash=0;
    for(int i=0; i<str.size();i++) {
        hash+= str[i]*pow(p, n);
        n++;
    }
    return hash%m;
}


void generateCombinations(vector<string>& result, const string& s) {
    int n = s.size();
    for (int i = 0; i < (1 << n); ++i) { // 1<<n - 2 в степени n
        string comb;
        for (int j = 0; j < n; ++j) {
            if (i & (1 << j)) {
                comb += s[j];
                //cout << comb << " - " << (i & (1 << j)) << endl;
            }
        }
        result.push_back(comb);
    }
}

int main() {
    string S = "aabc";
    vector<string> combinations;
    vector<int> hashs_for_comb;
    vector<string> results;
    set<int> indexes_of_equal_hashs;
    int flag = 0;
    
    generateCombinations(combinations, S);
    
    for (const auto& comb : combinations) { // проход по всем элементам вектора combinations. Для каждого элемента текущий элемент сохраняется в переменной comb
        cout << comb <<" - " << hashs(comb) << endl;
        results.push_back(comb);
        hashs_for_comb.push_back(hashs(comb));
    }
    cout << "___" << endl;
    for (int i = 1; i < hashs_for_comb.size(); i++) {
        for (int t = 1; t < hashs_for_comb.size() - 1; t++) {
            indexes_of_equal_hashs.insert(i);
            if (hashs_for_comb[i] == hashs_for_comb[t]) {
                
                indexes_of_equal_hashs.insert(t);
                flag = true;
            }
        }
        if (flag == true) {
            cout << hashs_for_comb[i] << ":";
            for (int n : indexes_of_equal_hashs) {
                cout << results[n] << " ";
            }
            cout << endl;
            flag = false;
        }
        if (flag == false) {
            for (int n : indexes_of_equal_hashs) {
                indexes_of_equal_hashs.erase(n);
            }
        }
        
    }
    return 0;
}