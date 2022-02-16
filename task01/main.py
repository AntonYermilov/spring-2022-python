from pathlib import Path
from simple_ast_drawer import draw_ast


def main():
    source_path = Path('code_examples', 'fib.py')
    image_path = Path('artifacts', 'ast.png')
    draw_ast(source_path, image_path)


if __name__ == '__main__':
    main()
