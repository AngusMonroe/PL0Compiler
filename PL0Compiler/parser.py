from PL0Compiler import lexer, opa
from enum import Enum
from copy import deepcopy

tokens = []  # token表，与lex.py中相同，其中元素格式为{'type': type, 'value': value}
token_num = -1  # 现在正在处理的token下标
cur_token = None  # 现在正在处理的token，元素格式为{'type': type, 'value': value}
cur_lv = -1
sym_table = []  # 符号表，其中元素为Record对象
PCode = []  # 最终生成的PCode，其中元素为PCodeOpt对象
plus_operator = ['+', '-']  # 加减操作符
multiply_operator = ['*', '/']  # 乘除操作符
relational_operator = ['=', '<>', '<=', '<', '>=', '>']  # 关系操作符


class Record:  # 单条符号表
    """ Record is the element in SymTable
    type is var, const or procedure
    name is an identifier
    value is value for const, level for var and procedure
    address is None for const, offset for var and first PCode address for procedure
    size is None as it is not used in my program
    """
    def __init__(self, type_=None, name=None, value=None, level=None, address=None, size=0):
        self.type = type_
        self.name = name
        self.value = value
        self.level = level
        self.address = address
        self.size = size

    def __str__(self):
        return '{' + '\ntype: {}\nname: {}\nvalue: {}\nlevel: {}\naddress: {}\nsize: {}\n'.format(
            self.type, self.name, self.value, self.level, self.address, self.size) + '}'


class PCodeList(Enum):  # PCode指令集
    LIT = 1  # 取常量a放到数据栈栈顶
    OPR = 2  # 执行运算，a表示执行何种运算(+ - * /)
    LOD = 3  # 取变量放到数据栈栈顶(相对地址为a,层次差为l)
    STO = 4  # 将数据栈栈顶内容存入变量(相对地址为a,层次差为l)
    CAL = 5  # 调用过程(入口指令地址为a,层次差为l)
    INT = 6  # 数据栈栈顶指针增加a
    JMP = 7  # 无条件转移到指令地址a
    JPC = 8  # 条件转移到指令地址a
    RED = 9  # 读数据，存入变量
    WRT = 10  # 写数据，将栈顶值输出

    def __str__(self):
        return self.name


class PCodeOpt:  # 单条PCode指令
    def __init__(self, f=None, l=None, a=None):
        self.f = f
        self.l = l
        self.a = a

    def __str__(self):
        return '(f: {}, l: {}, a: {})'.format(self.f, self.l, self.a)


def print_PCode():
    for pcode in PCode:
        print(pcode)


def print_sym_table():
    for record in sym_table:
        print(record)


def next_token():  # 处理下一个token
    global token_num
    token_num += 1
    if token_num >= len(tokens):
        raise Exception
        # raise ParserError('unexpected end of program', self.lexer.pos)
    # try:
    #     tokens[token_num] = next(iter(tokens))
    # except StopIteration:
    #     raise Exception
    #     # raise ParserError('unexpected end of program', self.lexer.pos)


def check_token(token):
    flag = False
    if token['type'] is None:
        if token['value'] == tokens[token_num]['value']:
            flag = True
    elif token['value'] is None:
        if token['type'] == tokens[token_num]['type']:
            flag = True
    else:
        if token == tokens[token_num]:
            flag = True
    if not flag:
        print(token)
        print(tokens[token_num])
        print(tokens[token_num - 1])
        print_PCode()
        raise Exception
        # raise ParserError('Expecting "%s" but current token is "%s"' % (str(token.value), str(self.current_token.value)),
        #                   self.lexer.pos)


def insert_table(record):  # 向符号表中插入一个Record对象
    for existing_record in sym_table:  # 检查是否重复
        if record.level != existing_record.level:
            break
        if record.name == existing_record.name and record.type == existing_record.type:
            raise Exception
            # raise DuplicateSymbol('Duplicate symbol name: %s' % record.name)

    sym_table.append(deepcopy(record))
    # print(deepcopy(record))
    
    
def find_sym(name, type_=None):  # 查询符号表
    for record in sym_table:
        if record.name == name:
            if type_ and record.type != type_:
                raise Exception
                # raise WrongSymbolType('Unexpected symbol type, expecting %s' % type_)
            else:
                return record
    # print_PCode()
    print_sym_table()
    # print(tokens[token_num])
    raise Exception
    # raise UndefinedSymbol('Undefined symbol: %s' % name)


def factor():
    if tokens[token_num]['type'] == 'IDENTIFIER':
        record = find_sym(tokens[token_num]['value'], None)
        if record.type == 'const':
            PCode.append(PCodeOpt(PCodeList.LIT, 0, record.value))
        elif record.type == 'var':
            PCode.append(PCodeOpt(PCodeList.LOD, cur_lv - record.level, record.address))
        elif record.type == 'procedure':
            raise Exception
            # raise ParserError('Wrong variable type')
        next_token()
    elif tokens[token_num]['type'] == 'NUMBER':
        PCode.append(PCodeOpt(PCodeList.LIT, 0, int(tokens[token_num]['value'])))
        next_token()
    else:
        check_token(token={'type': None, 'value': '('})
        next_token()
        expression()
        check_token(token={'type': None, 'value': ')'})
        next_token()


def term():
    factor()
    while tokens[token_num]['value'] in multiply_operator:
        op = tokens[token_num]['value']
        next_token()
        factor()
        if op == '*':
            PCode.append(PCodeOpt(PCodeList.OPR, 0, 4))
        else:
            PCode.append(PCodeOpt(PCodeList.OPR, 0, 5))


def expression():
    if tokens[token_num]['value'] in plus_operator:  # unary operator
        op = tokens[token_num]['value']
        next_token()
        term()
        if op == '-':
            PCode.append(PCodeOpt(PCodeList.OPR, 0, 1))
    else:
        term()
    while tokens[token_num]['value'] in plus_operator:  # binary operator
        op = tokens[token_num]['value']
        next_token()
        term()
        if op == '+':
            PCode.append(PCodeOpt(PCodeList.OPR, 0, 2))
        else:
            PCode.append(PCodeOpt(PCodeList.OPR, 0, 3))


def condition():
    if tokens[token_num]['value'] == 'odd':
        next_token()
        expression()
        PCode.append(PCodeOpt(PCodeList.OPR, 0, 6))
    else:
        expression()
        check_token(token={'type': 'OPERATOR', 'value': None})
        op = tokens[token_num]['value']
        next_token()
        expression()
        if op == '=':
            PCode.append(PCodeOpt(PCodeList.OPR, 0, 7))
        elif op == '<>':
            PCode.append(PCodeOpt(PCodeList.OPR, 0, 8))
        elif op == '<':
            PCode.append(PCodeOpt(PCodeList.OPR, 0, 9))
        elif op == '>=':
            PCode.append(PCodeOpt(PCodeList.OPR, 0, 10))
        elif op == '>':
            PCode.append(PCodeOpt(PCodeList.OPR, 0, 11))
        elif op == '<=':
            PCode.append(PCodeOpt(PCodeList.OPR, 0, 12))

    
def statement():
    if tokens[token_num]['type'] == 'IDENTIFIER':
        record = find_sym(tokens[token_num]['value'], 'var')
        next_token()
        check_token(token={'type': None, 'value': ':='})
        next_token()
        expression()
        PCode.append(PCodeOpt(PCodeList.STO, cur_lv - record.level, record.address))

    elif tokens[token_num]['value'] == 'if':
        next_token()
        condition()
        check_token(token={'type': None, 'value': 'then'})
        next_token()
        pcode_len1 = len(PCode)
        PCode.append(PCodeOpt(PCodeList.JPC, 0, 0))
        statement()  # then statement
        pcode_len2 = len(PCode)
        PCode.append(PCodeOpt(PCodeList.JMP, 0, 0))
        if tokens[token_num]['value'] == 'else':
            next_token()
            PCode[pcode_len1].a = len(PCode)
            statement()  # else statement
        else:
            PCode[pcode_len1].a = len(PCode)
        PCode[pcode_len2].a = len(PCode)

    elif tokens[token_num]['value'] == 'while':
        pcode_len1 = len(PCode)
        next_token()
        condition()
        pcode_len2 = len(PCode)
        PCode.append(PCodeOpt(PCodeList.JPC, 0, 0))
        check_token(token={'type': None, 'value': 'do'})
        next_token()
        statement()
        PCode.append(PCodeOpt(PCodeList.JMP, 0, pcode_len1))
        PCode[pcode_len2].a = len(PCode)

    elif tokens[token_num]['value'] == 'call':
        next_token()
        check_token(token={'type': 'IDENTIFIER', 'value': None})
        record = find_sym(tokens[token_num]['value'], 'procedure')
        PCode.append(PCodeOpt(PCodeList.CAL, cur_lv - record.level, record.address))
        next_token()

    elif tokens[token_num]['value'] == 'begin':
        next_token()
        statement()
        while tokens[token_num]['value'] == ';':
            next_token()
            statement()
        check_token(token={'type': None, 'value': 'end'})
        next_token()

    elif tokens[token_num]['value'] == 'repeat':
        next_token()
        pcode_len = len(PCode)
        statement()
        while tokens[token_num]['value'] == ';':
            next_token()
            statement()
        check_token(token={'type': None, 'value': 'until'})
        next_token()
        condition()
        PCode.append(PCodeOpt(PCodeList.JPC, 0, pcode_len))

    elif tokens[token_num]['value'] == 'read':
        next_token()
        check_token(token={'type': None, 'value': '('})
        next_token()
        while True:
            check_token(token={'type': 'IDENTIFIER', 'value': None})
            record = find_sym(tokens[token_num]['value'], 'var')
            PCode.append(PCodeOpt(PCodeList.RED, cur_lv - record.level, record.address))
            next_token()
            if tokens[token_num]['value'] != ',':
                break
            else:
                next_token()
        check_token(token={'type': None, 'value': ')'})
        next_token()

    elif tokens[token_num]['value'] == 'write':
        next_token()
        check_token(token={'type': None, 'value': '('})
        next_token()
        while True:
            expression()
            PCode.append(PCodeOpt(PCodeList.WRT, 0, 0))
            if tokens[token_num]['value'] != ',':
                break
            else:
                next_token()
        check_token(token={'type': None, 'value': ')'})
        next_token()


def block(dx):
    global cur_lv
    cur_lv += 1
    pcode_len = len(PCode)
    sym_table_len = len(sym_table)
    PCode.append(PCodeOpt(PCodeList.JMP, 0, 0))
    if tokens[token_num]['value'] == 'const':  # 对const关键字进行处理
        record = Record('const', None, None, 0)
        check_token(token={'type': None, 'value': 'const'})  # 读一个const
        next_token()
        while True:  # 可以同时声明多个常量
            check_token(token={'type': 'IDENTIFIER', 'value': None})  # 读一个变量名
            record.name = tokens[token_num]['value']
            next_token()
            check_token(token={'type': None, 'value': '='})  # 读一个=
            next_token()
            check_token(token={'type': 'NUMBER', 'value': None})  # 读一个数字
            record.value = int(tokens[token_num]['value'])
            insert_table(record)  # 插入记录
            next_token()
            if tokens[token_num]['value'] == ',':  # 如果下一个token是逗号，则忽略
                next_token()
            else:
                break
        check_token(token={'type': None, 'value': ';'})  # 读一个;
        next_token()
    if tokens[token_num]['value'] == 'var':  # 对var关键字进行处理
        record = Record('var', None, None, cur_lv)
        check_token(token={'type': None, 'value': 'var'})  # 读一个var
        next_token()
        while True:  # 可以同时声明多个var变量
            check_token(token={'type': 'IDENTIFIER', 'value': None})  # 读一个变量名
            record.name = tokens[token_num]['value']
            record.address = dx  # 保存其位置
            dx += 1
            insert_table(record)
            next_token()
            if tokens[token_num]['value'] == ',':  # 如果下一个token是逗号，则忽略
                next_token()
            else:
                break
        check_token(token={'type': None, 'value': ';'})  # 读一个;
        next_token()
    if tokens[token_num]['value'] == 'procedure':  # 对procedure关键字进行处理
        record = Record('procedure', None, None, cur_lv)
        while tokens[token_num]['value'] == 'procedure':
            next_token()
            check_token(token={'type': 'IDENTIFIER', 'value': None})  # 读一个标识符
            record.name = tokens[token_num]['value']
            insert_table(record)
            next_token()
            check_token(token={'type': None, 'value': ';'})  # 读一个;
            next_token()
            block(3)
            check_token(token={'type': None, 'value': ';'})  # 读一个;
            next_token()
    PCode[pcode_len].a = len(PCode)  # fill back the JMP inst
    sym_table[sym_table_len - 1].address = len(PCode)  # this value will be used by call
    PCode.append(PCodeOpt(PCodeList.INT, 0, dx))
    statement()
    PCode.append(PCodeOpt(PCodeList.OPR, 0, 0))
    cur_lv -= 1
    sym_table[sym_table_len:] = []


def analyze():
    record = Record()
    insert_table(record)
    block(3)
    check_token(token={'type': None, 'value': '.'})


def main(data):
    global tokens
    for token in lexer.analyze(data)[1]:  # 初始化tokens
        tokens.append(token)
    next_token()
    analyze()
    return PCode

if __name__ == '__main__':
    test_data = lexer.load_data('../data/pl0.txt')
    main(test_data)
    for ln, line in enumerate(PCode):
        print(line)
