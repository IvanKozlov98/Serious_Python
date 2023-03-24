import numpy as np
import pickle
from numpy.lib.mixins import NDArrayOperatorsMixin


class SerializableMixin:
    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)


class PrettyPrintMixin:
    def __str__(self):
        return str(self.view(np.ndarray))
    
    def __repr__(self):
        return repr(self.view(np.ndarray))


class GetterSetterMixin:
    @property
    def shape(self):
        return self.view(np.ndarray).shape
    
    @property
    def dtype(self):
        return self.view(np.ndarray).dtype
    
    @property
    def ndim(self):
        return self.view(np.ndarray).ndim
    
    @property
    def size(self):
        return self.view(np.ndarray).size


class Matrix(NDArrayOperatorsMixin, np.ndarray, PrettyPrintMixin, GetterSetterMixin, SerializableMixin):
    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        return obj


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
    matrix_sum.save('artifacts/medium/matrix+.pkl')
    matrix_prod.save('artifacts/medium/matrix_mul.pkl')
    matrix_matmul.save('artifacts/medium/matrix@.pkl')

    # Test serialization
    matrix3 = Matrix.load('artifacts/medium/matrix+.pkl')
    print(matrix3)
