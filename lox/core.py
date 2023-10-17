import sys

from lox.error import error, had_error, had_runtime_error, report
from lox.interpreter import Interpreter
from lox.parser import Parser
from lox.scanner import Scanner, Token, TokenType
from lox.tool.ast_printer import AstPrinter

interpreter = Interpreter()


def run_file(path: str):
    with open(path, 'r') as f:
        data = f.read()
    run(data)
    # Indicate an error in the exit code
    if had_error:
        exit(65)
    if had_runtime_error:
        exit(70)


def run_prompt():
    while True:
        line = input('> ')
        if line == '':
            break
        run(line)
        global had_error
        had_error = False


def run(source: str):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    statements = parser.parse()

    if had_error:
        return

    interpreter.interpret(statements)


def main():
    if len(sys.argv) > 2:
        print('Usage: plox [scripts]')
        print(sys.argv)
        exit(64)
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()


if __name__ == '__main__':
    main()
