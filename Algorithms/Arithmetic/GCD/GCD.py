#Iterative
def gcd(a, b):
    while b:
        a, b = b, a%b
    return a
# print(gcd(10, 12))
# print(gcd(10, 11))
# print(gcd(57894543261657, 5049318654315))