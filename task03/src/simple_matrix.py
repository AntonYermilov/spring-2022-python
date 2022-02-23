class SimpleMatrix:
    def __init__(self, matrix):
        assert len(matrix) > 0, 'expected non-empty matrix'
        assert len(matrix[0]) > 0, 'expected matrix with non-empty rows'
        assert all(map(lambda row: len(row) == len(matrix[0]), matrix)), 'all rows must be the same size'

        self._n, self._m = len(matrix), len(matrix[0])
        self._matrix = matrix

    @property
    def n(self) -> int:
        """
        :return: number of rows
        """
        return self._n

    @property
    def m(self) -> int:
        """
        :return: number of columns
        """
        return self._m

    def __getitem__(self, key: tuple[int, int]) -> float:
        i, j = key
        return self._matrix[i][j]

    def __setitem__(self, key: tuple[int, int], value: float) -> None:
        i, j = key
        self._matrix[i][j] = value

    def __add__(self, other: 'SimpleMatrix') -> 'SimpleMatrix':
        assert self.n == other.n and self.m == other.m, 'matrices must be the same size'
        result = SimpleMatrix([[0] * self.m for _ in range(self.n)])
        for i in range(self.n):
            for j in range(self.m):
                result[i, j] = self[i, j] + other[i, j]
        return result

    def __mul__(self, other: 'SimpleMatrix') -> 'SimpleMatrix':
        assert self.n == other.n and self.m == other.m, 'matrices must be the same size'
        result = SimpleMatrix([[0] * self.m for _ in range(self.n)])
        for i in range(self.n):
            for j in range(self.m):
                result[i, j] = self[i, j] * other[i, j]
        return result

    def __matmul__(self, other: 'SimpleMatrix') -> 'SimpleMatrix':
        assert self.m == other.n, '2nd dimension of first matrix does not match 1st dimension of second matrix'
        result = SimpleMatrix([[0] * other.m for _ in range(self.n)])
        for i in range(self.n):
            for j in range(other.m):
                for k in range(self.m):
                    result[i, j] += self[i, k] * other[k, j]
        return result

    def __str__(self):
        return '[\n' + '\n'.join(map(lambda row: f' {list(row)},', self._matrix)) + '\n]'
