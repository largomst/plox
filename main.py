import sys
from dataclasses import dataclass
from enum import Enum, auto

had_error = False

TokenType = Enum(
    'TokenType',
    """
    # Single-character tokens.
    LEFT_PAREN RIGHT_PAREN LEFT_BRACE RIGHT_BRACE COMMA DOT MINUS PLUS SEMICOLON SLASH STAR
    # One or two character tokens.
    BANG BANG_EQUAL EQUAL EQUAL_EQUAL GREATER GREATER_EQUAL
    # Literals.
    IDENTIFIER STRING NUMBER
    # Keywords.
    AND CLASS ELSE FALSE FUN FOR IF NIL OR PRINT RETURN SUPER THIS TRUE VAR WHILE
    EOF
""",
)


@dataclass
class Token:
    type: TokenType
    lexme: str
    literal: object
    line: int

    def __str__(self):
        return f'{self.type} {self.lexeme} {self.literal}'


def run_file(path):
    with open(path, 'r') as f:
        data = f.read()
    run(data)
    # Indicate an error in the exit code
    if had_error:
        exit(65)


def run_prompt():
    while True:
        line = input('> ')
        if line == '':
            break
        run(line)
        global had_error
        had_error = False


def run(source):
    pass
    # scanner = Scanner(source)
    # tokens = scanner.scan_tokens()
    # for token in tokens:
    #     print(token)


def main():
    if len(sys.argv) > 1:
        print('Usage: plox [scripts]')
        exit(64)
    elif len(sys.argv) == 1:
        run_file(sys.argv[0])
    else:
        run_prompt()


def error(line: int, message: str):
    report(line, '', message)


def report(line: int, where: str, message: str):
    sys.stderr.write(f'[line {line}] Error{where}: {message}\n')
    global had_error
    had_error = True


if __name__ == '__main__':
    main()
