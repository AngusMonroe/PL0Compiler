class CompilerError(Exception):
    def __init__(self, message='Compiler Error', pos=(0, 0)):
        self.message = message
        self.pos = pos

    def __str__(self):
        return '{} at line {}, position {}.\n'.format(
            self.message, self.pos[0], self.pos[1])


class LexerError(CompilerError):
    def __init__(self, message='Lexer Error', pos=(0, 0), token=None):
        self.message = message
        self.pos = pos
        self.token = token

    def __str__(self):
        return '{} with token "{}" at line {}, position {}.\n'.format(
            self.message, self.token, self.pos[0], self.pos[1])


class ParserError(CompilerError):
    def __init__(self, message='Parser Error', pos=(0, 0), token=None):
        self.message = message
        self.pos = pos
        self.token = token

    def __str__(self):
        return '{} with token "{}" at line {}, position {}.\n'.format(
            self.message, self.token, self.pos[0], self.pos[1])


class DuplicateSymbol(ParserError):
    def __init__(self, message='Duplicate symbol', pos=(0, 0)):
        self.message = message
        self.pos = pos


class UndefinedSymbol(ParserError):
    def __init__(self, message='Undefined symbol', pos=(0, 0)):
        self.message = message
        self.pos = pos


class WrongSymbolType(ParserError):
    def __init__(self, message='Unexpected symbol type', pos=(0, 0)):
        self.message = message
        self.pos = pos


class InterpreterError(CompilerError):
    def __init__(self, message='Interpreter error', ln=0):
        self.message = message
        self.ln = ln


class ErrorTable:
    """ A table to store Errors. By properly using get and enter, duplications are avoided
    """
    def __init__(self):
        self.table = []

    def __getitem__(self, item):
        return self.table[item]

    def __setitem__(self, key, value):
        self.table[key] = value

    def __len__(self):
        return len(self.table)
