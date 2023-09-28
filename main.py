import sys

had_error = False


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
