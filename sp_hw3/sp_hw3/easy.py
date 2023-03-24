import numpy as np


class Matrix:
    b = 32416190071
    cached_muls = dict()

    def __init__(self, array):
        self._array = array
    
    @property
    def array(self):
        return self._array

    @array.setter
    def array(self, value):
        self._array = value

    def __add__(self, other):
        if self._array.shape != other._array.shape:
            raise ValueError("Matrices have different shapes!")
        return Matrix(self._array + other._array)
    
    def __mul__(self, other):
        if self._array.shape != other._array.shape:
            raise ValueError("Matrices have different shapes!")
        return Matrix(self._array * other._array)
    
    def __matmul__(self, other):
        if self._array.shape[1] != other._array.shape[0]:
            raise ValueError("Matrices have incompatible shapes for matrix multiplication!")
        hash_other = hash(other)
        if hash_other not in Matrix.cached_muls:
            res = Matrix(self._array @ other._array)
            Matrix.cached_muls[hash_other] = res
        return Matrix.cached_muls[hash_other]

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Matrix) and np.array_equal(self._array, __value._array)

    def __hash__(self):
        """
        hash(a) = (a1 + .. + an) % const, where const - big prime number
        """
        return int(np.sum(self._array) % Matrix.b)

def hard_example():
    A = Matrix(np.array([np.arange(10)]))
    C = Matrix(np.array([9 - np.arange(10)]))
    B = Matrix(np.array([(10 + np.arange(10))]).T)
    D = Matrix(np.array([(10 + np.arange(10))]).T)
    AB = A @ B
    CD = C @ D
    assert (hash(A) == hash(C)) and (A != C) and (B == D) #and (AB != CD)
    np.savetxt('artifacts/hard/A.txt', A.array, fmt='%d')
    np.savetxt('artifacts/hard/B.txt', B.array, fmt='%d')
    np.savetxt('artifacts/hard/C.txt', C.array, fmt='%d')
    np.savetxt('artifacts/hard/D.txt', D.array, fmt='%d')
    np.savetxt('artifacts/hard/AB.txt', AB.array, fmt='%d')
    np.savetxt('artifacts/hard/CD.txt', C.array @ D.array, fmt='%d')
    np.savetxt('artifacts/hard/hash.txt', np.array([hash(AB), hash(CD)]), fmt='%d')
    

def easy_example():
     # Generate two matrices
    np.random.seed(0)
    matrix1 = Matrix(np.random.randint(0, 10, (10, 10)))
    matrix2 = Matrix(np.random.randint(0, 10, (10, 10)))

    # Perform matrix operations
    matrix_sum = matrix1 + matrix2
    matrix_prod = matrix1 * matrix2
    matrix_matmul = matrix1 @ matrix2

    # Write results to files
    np.savetxt('artifacts/easy/matrix+.txt', matrix_sum.array, fmt='%d')
    np.savetxt('artifacts/easy/matrix_mul.txt', matrix_prod.array, fmt='%d')
    np.savetxt('artifacts/easy/matrix@.txt', matrix_matmul.array, fmt='%d')


if __name__ == '__main__':
    easy_example()
    hard_example()
