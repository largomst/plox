import sys
from pathlib import Path
from typing import List


def define_type(f, base_name: str, class_name: str, field_list: str):
    fields = []
    for field in field_list.split(', '):
        type_, param = field.strip().split(' ')
        fields.append(f"{param}: '{type_}'")

    f.write(f'class {class_name}({base_name}):\n')
    f.write(f'    def __init__(self, {", ".join(fields)}):\n')
    for field in field_list.split(', '):
        name = field.split(' ')[1]
        f.write(f'        self.{name} = {name}\n')
    f.write('\n')
    f.write("    def accept(self, visitor: 'Visitor'):\n")
    f.write(f'        return visitor.visit{class_name}{base_name}(self)\n\n\n')


def define_visitor(f, base_name: str, types: List[str]):
    f.write('class Visitor(ABC):\n')
    for type_ in types:
        type_name = type_.split(':')[0].strip()
        f.write(f'    @abstractmethod\n')
        f.write(f"    def visit{type_name}{base_name}({base_name.lower()}: '{type_name}'):\n")
        f.write(f'        pass\n\n')


def define_ast(output_dir: str, base_name: str, types: List[str]):
    path = Path(output_dir) / f'{base_name}.py'
    with open(path, 'w', encoding='utf-8') as f:
        f.write('from abc import ABC, abstractmethod\n\n')
        f.write('from lox.scanner import Token\n\n\n')
        f.write(f'class {base_name}(ABC):\n')
        f.write(f'    @abstractmethod\n')
        f.write(f"    def accept(self, visitor: 'Visitor'):\n        pass\n\n\n")
        define_visitor(f, base_name, types)
        for type_ in types:
            class_name = type_.split(':')[0].strip()
            fields = type_.split(':')[1].strip()
            define_type(f, base_name, class_name, fields)
        f.write('\n')


def main():
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: generate_ast <output directory>\n')
        exit(64)
    output_dir = sys.argv[1]
    define_ast(
        output_dir,
        'Expr',
        [
            'Assign   : Token name, Expr value',
            'Binary   : Expr left, Token operator, Expr right',
            'Call     : Expr callee, Token paren, List[Expr] arguments',
            'Grouping : Expr expression',
            'Literal  : object value',
            'Logical  : Expr left, Token operator, Expr right',
            'Unary    : Token operator, Expr right',
            'Variable : Token name',
        ],
    )
    define_ast(
        output_dir,
        'Stmt',
        [
            'Block      : List[Stmt] statements',
            'Expression : Expr expression',
            'If         : Expr condition, Stmt thenBranch, Stmt elseBranch',
            'Print      : Expr expression',
            'Var        : Token name, Expr initializer',
            'While      : Expr condition, Stmt body',
        ],
    )


if __name__ == '__main__':
    main()
