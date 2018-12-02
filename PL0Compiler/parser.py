from PL0Compiler import lexer, opa

tokens = []
cur_token = None
sym_table = []


class Record:
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


def next_sym():
    cur_token = next(iter(tokens))
    record = Record()
    print(record)


def main():
    test_data = lexer.load_data('../data/pl0.txt')
    for token in lexer.analyze(test_data)[1]:  # 初始化tokens
        tokens.append(token)
    next_sym()

if __name__ == '__main__':
    main()
