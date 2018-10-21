from enum import Enum

from graph import Graph
 
class Matrix(object):
    _mat = None
    _n_rows = None
    _n_cols = None
    
    _n_elems = None

    class TensorType(Enum):
        scalar = 0
        vector = 1
        matrix = 2
        pass
    _tensor_type = None

    def __init__(self):
        
        pass

    @classmethod
    def from_2d_array(self, arr2d):
        n_cols = None 
        for i in arr2d:
            if n_cols is None:
                n_cols = len(i)
                continue
            assert len(i) == n_cols, 'The 2d array provided has not a constant number of colums in each of its rows'

        m = Matrix()
        m._mat = arr2d
        m._n_rows = len(arr2d)
        m._n_cols = len(arr2d[0])
        m._tensor_type = self.TensorType.matrix

        return m    

    @classmethod
    def col_vector(self, arr):
        mat = [
            [el]
            for el in arr
        ]

        m = Matrix.from_2d_array(mat)
        m._n_elems = len(arr)
        m._tensor_type = self.TensorType.vector

        return m

    @classmethod
    def row_vector(self, arr):
        mat = [
            [el for el in arr]
        ]

        m = Matrix.from_2d_array(mat)
        m._n_elems = len(arr)
        m._tensor_type = self.TensorType.vector

        return m


    @classmethod
    def zero(self, n_rows, n_cols):        
        mat = [
            [0 for j in range(n_cols)]
            for i in range(n_rows)
        ]

        return Matrix.from_2d_array(mat)


    @classmethod
    def identity(self, n_rows):
        mat = [
            [1 if i == j else 0 for j in range(n_rows)]
            for i in range(n_rows)
        ]

        return Matrix.from_2d_array(mat)


    @classmethod
    def dot(self, a, b):
        assert (a._tensor_type, b._tensor_type) == (self.TensorType.vector, self.TensorType.vector), 'Can\'t perform dot product on a non-vector'
        assert a._n_elems == b._n_elems, 'The number of elements must be equal on both vectors'

        if a._n_rows > 1:
            a = a.transpose()
        
        if b._n_cols > 1:
            b.transpose()

        return (a * b)._mat[0][0]

    
    def transpose(self):
        mat = [
            [self._mat[i][j] for i in range(self._n_rows)]
            for j in range(self._n_cols)
        ]

        return Matrix.from_2d_array(mat)


    def __mul__(self, other):
        assert self._n_cols == other._n_rows, 'The number of colums of the first factor must be equal to the number of rows of the second'

        mat = []
        for i in range(self._n_rows):
            row = []
            for j in range(other._n_cols):
                _sum = 0
                for k in range(self._n_cols):
                    _sum += self._mat[i][k] * other._mat[k][j]
                row.append(_sum)
            mat.append(row)
            

        return Matrix.from_2d_array(mat)

    def __add__(self, other):
        assert (self._n_rows, self._n_cols) == (other._n_rows, other._n_cols), 'The shapes of the two matrices must be equal'

        mat = [
            [self._mat[i][j] + other._mat[i][j] for j in range(self._n_cols)]
            for i in range(self._n_rows)
        ]

        return Matrix.from_2d_array(mat)


    def __sub__(self, other):
        assert (self._n_rows, self._n_cols) == (other._n_rows, other._n_cols), 'The shapes of the two matrices must be equal'

        mat = [
            [self._mat[i][j] - other._mat[i][j] for j in range(self._n_cols)]
            for i in range(self._n_rows)
        ]

        return Matrix.from_2d_array(mat)

    def __neg__(self):
        mat = [
            [-self._mat[i][j] for j in range(self._n_cols)]
            for i in range(self._n_rows)
        ]

        return Matrix.from_2d_array(mat)


    def __eq__(self, other):
        if (self._n_rows, self._n_cols) != (other._n_rows, other._n_cols):
            return False
        
        for i in range(self._n_rows):
            for j in range(self._n_cols):
                if self._mat[i][j] != other._mat[i][j]:
                    return False
        
        return True

    def __ne__(self, other):
        return not self.__eq__(other)


    def __str__(self):
        res = '\n[\n'
        for row in self._mat:
            res += '\t['

            first = True
            for el in row:
                if first:
                    res += str(el)
                    first = False
                    continue
                res += ', ' + str(el)
            res += ']\n'
        res += ']'

        return res

    

    def get_reduction_permutation_matrix(self):
        assert self._n_rows == self._n_cols, 'The matrix must be square'

        adj_mat = [
            [None if el == 0 else el for el in row]
            for row in self._mat
        ]

        g = Graph(adj_mat)
        if g.is_strongly_connected():
            return Matrix.identity(self._n_rows)
        

        reachables = [i for i in range(g._n_nodes)]

        for i in range(g._n_nodes):
            (dists, prevs) = g.dijkstra(i)
            
            for j in reachables:
                if dists[j] is None:
                    reachables.remove(j)
        

        identity = Matrix.identity(g._n_nodes)._mat
        perm_mat = []
        for i in reachables:
            perm_mat.append(identity[i])
        
        for i in range(g._n_nodes):
            if i not in reachables:
                perm_mat.append(identity[i])

        return Matrix.from_2d_array(perm_mat).transpose()


    def reduce(self):
        prem_mat = self.get_reduction_permutation_matrix()
        return prem_mat.transpose() * self * prem_mat


    pass


A = Matrix.from_2d_array([
    [-4, 0, -1, 0],
    [2, 7, 8, -3],
    [0, 0, 2, 0],
    [1, 77, -12, 33]
])

# print(A)
# print(A.get_reduction_permutation_matrix())
# print(A.reduce())


# v = Matrix.col_vector([1, 2, 3])


# a = Matrix.col_vector([1.0, 0.25])
# b = Matrix.col_vector([0.5, 1.0])

# print(Matrix.dot(a, b))