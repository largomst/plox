import sys

from lox.scanner import Scanner, Token, TokenType

had_error = False


def run_file(path: str):
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


def run(source: str):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    for token in tokens:
        print(token)


def main():
    if len(sys.argv) > 2:
        print('Usage: plox [scripts]')
        print(sys.argv)
        exit(64)
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
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
