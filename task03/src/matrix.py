import numpy as np
from numbers import Number
from pathlib import Path


# noinspection PyAttributeOutsideInit
class _MatrixPropertyMixin:
    @property
    def matrix(self) -> np.ndarray:
        return self._matrix

    @matrix.setter
    def matrix(self, matrix):
        self._matrix = np.asarray(matrix)


# noinspection PyUnresolvedReferences
class _MatrixReprMixin:
    def __str__(self) -> str:
        return '[\n' + '\n'.join(map(lambda row: f' {list(row)},', self.matrix)) + '\n]'


class _MatrixDumpMixin:
    def dump(self, path: str) -> None:
        Path(path).write_text(str(self))


# noinspection PyUnresolvedReferences,PyArgumentList
class _MatrixOpsMixin(np.lib.mixins.NDArrayOperatorsMixin):
    _HANDLED_TYPES = (np.ndarray, Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (_MatrixOpsMixin,)):
                return NotImplemented

        inputs = tuple(x.matrix if isinstance(x, _MatrixOpsMixin) else x for x in inputs)
        if out:
            kwargs['out'] = tuple(x.matrix if isinstance(x, _MatrixOpsMixin) else x for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)


# noinspection PyUnresolvedReferences
class _MatrixHashMixin:
    def __hash__(self) -> int:
        """
        Polynomial hash modulo 10**9+7. Hashes matrix dimensions and all matrix elements.
        :return: hash
        """
        base, p = 31, 10**9+7

        h = 0
        for dim in self.matrix.shape:
            h = (dim + base * h) % p
        for row in self.matrix:
            for el in row:
                h = (el + base * h) % p
        return int(h)


class Matrix(_MatrixPropertyMixin, _MatrixOpsMixin, _MatrixReprMixin, _MatrixDumpMixin):
    def __init__(self, matrix):
        self._matrix = np.asarray(matrix)
        if len(self._matrix.shape) != 2:
            raise ValueError(f'expected rectangular matrix, but found matrix with {len(self._matrix.shape)} dimensions')


class HashableMatrix(Matrix, _MatrixHashMixin):
    _cache: dict[tuple[int, int], 'HashableMatrix'] = {}

    __hash__ = _MatrixHashMixin.__hash__

    def __matmul__(self, other) -> 'HashableMatrix':
        if self.matrix.shape[1] != self.matrix.shape[0]:
            raise ValueError('2nd dimension of first matrix does not match 1st dimension of second matrix')

        h1, h2 = hash(self), hash(other)
        if (h1, h2) in self._cache:
            return self._cache[(h1, h2)]

        result = HashableMatrix(self.matrix @ other.matrix)
        self._cache[(h1, h2)] = result

        return result
