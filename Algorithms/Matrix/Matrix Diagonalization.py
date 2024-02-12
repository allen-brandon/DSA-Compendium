from numpy import array, round, diag
from numpy.linalg import eig, matrix_power, matrix_rank
def diagonalize(matrix):
    if len(matrix) != len(matrix[0]):
        raise ValueError("Tried to diagonalize a non-square matrix")
    if matrix_rank(matrix) != len(matrix):
        raise ValueError("Tried to diagonalize a rank deficient matrix")
    diagonal, basis = eig(matrix)
    inv_basis = matrix_power(basis, -1)
    return (basis, diagonal, inv_basis)

#Apply transformation T to vector V, K times 
def transform(V, T, K, mod=None):
    basis, dia, inv_basis = diagonalize(T)
    dia = diag([pow(ei, K, mod) for ei in dia])
    res = V @ basis @ dia @ inv_basis
    return round(res).astype(int)

### Diagonalization vs. Naive Multiplication ###
## Works for any matrix length;
## 
# from random import randint
# vec = [1,3,5,1]
# trans = [[4, 2, 1, 3], [4, 1, 3, 3], [3, 3, 2, 3], [3, 1, 2, 1]]
# eff = matrix_power(trans, 8)
# print(trans)
# print(eff)
# print(vec @ eff)
# print(transform(vec, trans, 8))