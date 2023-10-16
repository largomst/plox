import sys

had_error = False
had_runtime_error = False


class LoxRuntimeError(RuntimeError):
    def __init__(self, token: 'Token', message: str):
        super().__init__(message)
        self.token = token


def error(line: int, message: str):
    report(line, '', message)


def report(line: int, where: str, message: str):
    sys.stderr.write(f'[line {line}] Error{where}: {message}\n')
    global had_error
    had_error = True


def runtime_error(error: LoxRuntimeError):
    # sys.stderr.write(str(error) + '\n[line] ' + str(error.token.line) + ']')
    sys.stderr.write(f'{error}\n[line {error.token.line}]\n')
    global had_runtime_error
    had_runtime_error = True
