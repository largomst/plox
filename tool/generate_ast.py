import sys
from pathlib import Path
from typing import List


def define_type(f, base_name: str, class_name: str, field_list: str):
    fields = ', '.join(
        [': '.join(reversed(field.strip().split(' '))) for field in field_list.split(', ')]
    )

    f.write(f'class {class_name}({base_name}):\n')
    f.write(f'    def __init__(self, {fields}):\n')
    for field in field_list.split(', '):
        name = field.split(' ')[1]
        f.write(f'        self.{name} = {name}\n')
    f.write('\n\n')


def define_ast(output_dir: str, base_name: str, types: List[str]):
    path = Path(output_dir) / f'{base_name}.py'
    with open(path, 'w', encoding='utf-8') as f:
        f.write('from abc import ABC, abstractmethod\n\n\n')
        f.write(f'class {base_name}(ABC):\n    pass\n\n\n')
        for type_ in types:
            class_name = type_.split(':')[0].strip()
            fields = type_.split(':')[1].strip()
            define_type(f, base_name, class_name, fields)


def main():
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: generate_ast <output directory>\n')
        exit(64)
    output_dir = sys.argv[1]
    define_ast(
        output_dir,
        'Expr',
        [
            'Binary   : Expr left, Token operator, Expr right',
            'Grouping : Expr expression',
            'Literal  : Object value',
            'Unary    : Token operator, Expr right',
        ],
    )


if __name__ == '__main__':
    main()
