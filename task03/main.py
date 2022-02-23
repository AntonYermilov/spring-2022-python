import numpy as np
from pathlib import Path

from src.simple_matrix import SimpleMatrix
from src.matrix import Matrix, HashableMatrix


def find_collision():
    rnd = np.random.RandomState(seed=0)
    hashes = {}

    i, j = 0, 0
    while True:
        m = HashableMatrix(rnd.randint(0, 10, (5, 5)))
        h = hash(m)
        if h in hashes:
            j = hashes[h]
            break
        hashes[h] = i
        i += 1

    rnd = np.random.RandomState(seed=0)

    m1, m2 = None, None
    for k in range(i + 1):
        m1 = rnd.randint(0, 10, (5, 5))
        if k == j:
            m2 = m1

    m3, m4 = np.ones((5, 5), dtype=int), np.ones((5, 5), dtype=int)

    a, c, b, d = HashableMatrix(m1), HashableMatrix(m2), HashableMatrix(m3), HashableMatrix(m4)

    assert (hash(a) == hash(c)) and (a != c) and (b == d) and ((a @ b) == (c @ d)).matrix.all()
    assert ((m1 @ m3) != (m2 @ m4)).all()

    return a, b, c, d


def easy():
    rnd = np.random.RandomState(seed=0)

    a = SimpleMatrix(rnd.randint(0, 10, (10, 10)))
    b = SimpleMatrix(rnd.randint(0, 10, (10, 10)))

    Path('artifacts', 'easy', 'matrix+.txt').write_text(str(a + b))
    Path('artifacts', 'easy', 'matrix*.txt').write_text(str(a * b))
    Path('artifacts', 'easy', 'matrix@.txt').write_text(str(a @ b))


def medium():
    rnd = np.random.RandomState(seed=0)

    a = Matrix(rnd.randint(0, 10, (10, 10)))
    b = Matrix(rnd.randint(0, 10, (10, 10)))

    (a + b).dump('artifacts/medium/matrix+.txt')
    (a * b).dump('artifacts/medium/matrix*.txt')
    (a @ b).dump('artifacts/medium/matrix@.txt')


def hard():
    a, b, c, d = find_collision()
    a.dump('artifacts/hard/A.txt')
    b.dump('artifacts/hard/B.txt')
    c.dump('artifacts/hard/C.txt')
    d.dump('artifacts/hard/D.txt')
    (a @ b).dump('artifacts/hard/AB.txt')
    (Matrix(c.matrix) @ Matrix(d.matrix)).dump('artifacts/hard/CD.txt')
    Path('artifacts/hard/hashes.txt').write_text(f'{hash(a @ b)} {hash(c @ d)}')


def main():
    easy()
    medium()
    hard()


if __name__ == '__main__':
    main()
