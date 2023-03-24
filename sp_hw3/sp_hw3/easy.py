import numpy as np


class Matrix:
    def __init__(self, array):
        self.array = array
    
    def __add__(self, other):
        if self.array.shape != other.array.shape:
            raise ValueError("Matrices have different shapes!")
        return Matrix(self.array + other.array)
    
    def __mul__(self, other):
        if self.array.shape != other.array.shape:
            raise ValueError("Matrices have different shapes!")
        return Matrix(self.array * other.array)
    
    def __matmul__(self, other):
        if self.array.shape[1] != other.array.shape[0]:
            raise ValueError("Matrices have incompatible shapes for matrix multiplication!")
        return Matrix(self.array @ other.array)


if __name__ == '__main__':
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
