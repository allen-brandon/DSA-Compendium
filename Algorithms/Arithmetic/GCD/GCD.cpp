//Iterative
// int gcd(int a, int b) {
//     int temp;
//     while (b != 0) {
//         std::swap(a, b);
//         b = b%a;
//     }
//     return a;
// }

//Recursive
// int gcd(int a, int b) {
//     if (a == b) return a;
//     return gcd(b, a%b);
// }