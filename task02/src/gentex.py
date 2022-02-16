import tempfile
from typing import Any
from pathlib import Path

from functools import reduce
import operator

import simple_ast_drawer


def matrix2tex(matrix: list[list[Any]]) -> str:
    n = len(matrix)
    assert n > 0, 'Expected non-empty matrix'

    m = max(map(len, matrix))
    assert m > 0, 'Expected at least one non-empty row'

    return \
        f'\\begin{{tabular}}{{|{"|".join("c" for _ in range(m))}|}} \\hline \n' + \
        reduce(
            operator.add,
            map(
                lambda repr: f'{repr}\\\\ \\hline \n',
                map(
                    lambda row: reduce(lambda x, y: f'{x} & {y}', row),
                    map(lambda row: row + [''] * (m - len(row)), matrix)
                )
            )
        ) + \
        '\\end{tabular}'


def generate_image(image_path: Path):
    code = 'def fib(n):\n' \
           '    f = [0, 1]\n' \
           '    while len(f) < n:\n' \
           '        f.append(f[-1] + f[-2])\n' \
           '    return f[:n]\n'

    with tempfile.NamedTemporaryFile('w') as fp:
        print(code, file=fp)
        fp.flush()
        simple_ast_drawer.draw_ast(Path(fp.name), image_path)


def image2tex(image_path: Path) -> str:
    return \
        f'\\begin{{center}}\n' \
        f'\\includegraphics[width=1.0\\textwidth]{{{image_path.absolute()}}}\n' \
        f'\\end{{center}}'


def create_document(objects: list[str]) -> str:
    return \
        '\\documentclass[12pt,a4paper]{article}\n' \
        '\\usepackage{graphicx}\n' \
        '\\begin{document}\n' + \
        reduce(operator.add, map(lambda obj: f'{obj}\n', objects)) + \
        '\\end{document}'


def save_document(document: str, path: Path):
    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    with path.open('w') as fp:
        fp.write(document)


def main():
    matrix = [
        [1, 2, 3],
        ['a', 'b', 'test test test test test test'],
        [0.1, 2, 'x', 'hello world']
    ]

    image_path = Path('artifacts', 'image.png')
    generate_image(image_path)

    document = create_document([
        matrix2tex(matrix),
        image2tex(image_path)
    ])

    document_path = Path('artifacts', 'main.tex')
    save_document(document, document_path)


if __name__ == '__main__':
    main()
