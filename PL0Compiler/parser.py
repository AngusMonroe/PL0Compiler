from PL0Compiler import lexer, opa
from enum import Enum

tokens = []  # token表，与lex.py中相同，其中元素格式为{'type': type, 'value': value}
cur_token = None  # 现在正在处理的token，元素格式为{'type': type, 'value': value}
cur_lv = -1
sym_table = []  # 符号表，其中元素为Record对象
PCode = []  # 最终生成的PCode，其中元素为PCodeOpt对象


class Record:  # 单条符号表
    """ Record is the element in SymTable
    type is var, const or procedure
    name is an identifier
    value is value for const, level for var and procedure
    address is None for const, offset for var and first pcode address for procedure
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


def next_token():  # 处理下一个token
    global cur_token
    try:
        cur_token = next(iter(tokens))
    except StopIteration:
        raise Exception
        # raise ParserError('unexpected end of program', self.lexer.pos)


def check_token(token):
    if token['type'] is None:
        b = token['value'] == cur_token['value']
    elif token['value'] is None:
        b = token['type'] == cur_token['type']
    else:
        b = token == cur_token
    if not b:
        raise Exception
        # raise ParserError('Expecting "%s" but current token is "%s"' % (str(token.value), str(self.current_token.value)),
        #                   self.lexer.pos)


def insert_table(record):  # 向符号表中插入一个Record对象
    for existing_record in sym_table[::-1]:  # 检查是否重复
        if record.level != existing_record.level:
            break
        if record.name == existing_record.name and record.type == existing_record.type:
            raise Exception
            # raise DuplicateSymbol('Duplicate symbol name: %s' % record.name)
    sym_table.append(record)


def block(dx):
    global cur_lv
    cur_lv += 1
    PCode.append(PCodeOpt(PCodeList.JMP, 0, 0))
    if cur_token['value'] == 'const':
        record = Record('const', None, None, 0)
        check_token(token={'type': None, 'value': 'const'})
        next_token()
        while True:
            check_token(token={'type': 'IDENTIFIER', 'value': None})
            record.name = cur_token['value']
            next_token()
            check_token(token={'type': None, 'value': '='})
            next_token()
            check_token(token={'type': 'NUMBER', 'value': None})
            record.value = int(cur_token['value'])
            insert_table(record)
            next_token()
            if cur_token['value'] == ',':
                next_token()
            else:
                break
        check_token(token={'type': None, 'value': ';'})
        next_token()
    if cur_token['value'] == 'var':
        record = Record('var', None, None, cur_lv)
        check_token(token={'type': None, 'value': 'var'})
        next_token()
        while True:
            check_token(token={'type': 'IDENTIFIER', 'value': None})
            record.name = cur_token['value']
            record.address = dx
            dx += 1
            insert_table(record)
            next_token()
            if cur_token['value'] == ',':
                next_token()
            else:
                break
        check_token(token={'type': None, 'value': ';'})
        next_token()
        return dx
    if cur_token['value'] == 'procedure':
        record = Record('procedure', None, None, cur_lv)
        while cur_token['value'] == 'procedure':
            next_token()
            check_token(token={'type': 'IDENTIFIER', 'value': None})
            record.name = cur_token['value']
            insert_table(record)
            next_token()
            check_token(token={'type': None, 'value': ';'})
            next_token()
            block(3)
            check_token(token={'type': None, 'value': ';'})
            next_token()
    PCode[len(PCode)].a = len(PCode)  # fill back the JMP inst
    sym_table[len(sym_table) - 1].address = len(PCode)  # this value will be used by call
    PCode.append(PCodeOpt(PCodeList.INT, 0, dx))
    statement()
    PCode.append(PCodeOpt(PCodeList.OPR, 0, 0))
    cur_lv -= 1
    sym_table[len(sym_table):] = []


def analyze():
    record = Record()
    insert_table(record)
    block(3)


def main():
    global tokens
    test_data = lexer.load_data('../data/pl0.txt')
    for token in lexer.analyze(test_data)[1]:  # 初始化tokens
        tokens.append(token)
    next_token()
    analyze()

if __name__ == '__main__':
    main()
