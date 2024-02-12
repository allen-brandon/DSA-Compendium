#include <vector> // Include the necessary header file

int findMajority(std::vector<int>& arr) {
    int c = 0, x;
    for (auto y: arr) {
        if (!c) x=y;
        c+=((x==y)<<1)-1;
    }
    return x;
};