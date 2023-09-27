import sys


def run_file(path):
    with open(path, 'r') as f:
        data = f.read()
    run(data)


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


if __name__ == '__main__':
    main()
