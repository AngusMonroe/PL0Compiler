class CompilerError(Exception):
    def __init__(self, message='Compiler Error', pos=(0, 0)):
        self.message = message
        self.pos = pos

    def __str__(self):
        return '{} at line {}, position {}.'.format(
            self.message, self.pos[0], self.pos[1])


class LexerError(CompilerError):
    def __init__(self, message='Lexer Error', pos=(0, 0), token=None):
        self.message = message
        self.pos = pos
        self.token = token

    def __str__(self):
        return '{} with token "{}" at line {}, position {}.'.format(
            self.message, self.token, self.pos[0], self.pos[1])


class ParserError(CompilerError):
    def __init__(self, type_=0, pos=(0, 0), token=''):
        swicher = {  # 定义一个map，相当于定义case：func()
            '0': 'UndeclaredError with token "' + token + '"',  # 未定义错误
            '1': 'Must be "=" instead of ":="',  # 应是=而不是:=
            '2': 'Must be NUMBER after "="',  # =后应为数
            '3': 'Must be "=" after IDENTIFIER',  # 标识符后应为=
            '4': 'Must be IDENTIFIER after ' + token,  # const,var,procedure后应为标识符
            '5': 'Expected "' + token + '" but not found',  # 漏掉,或;
            '6': 'Incorrect token after procedure declaration',  # 过程说明后的符号不正确
            '7': 'Must be statement',  # 应为语句
            '8': 'Incorrect token after statement in program',  # 程序体内语句部分后的符号不正确
            '9': 'Must be "."',  # 应为.
            '10': 'Expected ";" between statements',  # 语句之间漏;
            '11': 'Undefined IDENTIFIER "' + token + '"',  # 标识符未声明
            '12': 'Can not assign for const or procedure',  # 不可向常量或过程赋值
            '13': 'Must be :=',  # 应为赋值运算符:=
            '14': 'Must be IDENTIFIER after call',  # call后应为标识符
            '15': 'Can not call const or variable "' + token + '"',  # 不可调用常量或变量
            '16': 'Must be "then"',  # 应为then
            '17': 'Must be ";" or "end"',  # 应为;或end
            '18': 'Must be "do"',  # 应为do
            '19': 'Incorrect token after statement',  # 语句后的符号不正确
            '20': 'Must be RELATIONAL_OPERATOR',  # 应为关系运算符
            '21': 'There could not be procedure IDENTIFIER in expression',  # 表达式内不可有过程标识符
            '22': 'Expected ")" but not found',  # 漏右括号
            '23': 'Incorrect token after factor',  # 因子后不可为此符号
            '24': 'Expression could not begin with "' + token + '"',  # 表达式不能以此符号开始
            '30': 'Too big number',  # 这个数太大
            '40': 'Must be "("'  # 应为左括号
        }
        self.type = type_
        self.message = swicher[str(type_)]
        self.pos = pos
        self.token = token

    def __str__(self):
        return 'ERROR[{}]: {} at line {}, position {}.'.format(
            self.type, self.message, self.pos[0], self.pos[1])


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
