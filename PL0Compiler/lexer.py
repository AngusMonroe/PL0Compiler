
import re
import copy
from PL0Compiler.exception import *

patterns = {
    'BLANK': '\s',
    'KEYWORD': 'const|var|procedure|if|then|else|while|do|call|begin|end|repeat|until|read|write|odd',
    'DELIMITER': '\.|\(|\)|,|;',
    'OPERATOR': '\+|-|\*|/|:=|=|<>|<=|<|>=|>',
    'IDENTIFIER': '[A-Za-z][A-Za-z0-9]*',
    'NUMBER': '\d+(\.\d+)?',
    'UNDEFINED_SYMBOL': '.'
}


def load_data(file_path):
    file = open(file_path, 'r', encoding='utf8')
    data = file.read()
    file.close()
    return data


def analyze(data):
    e = ErrorTable()
    tokens = []
    res = []
    pos = [1, 1]
    while data:
        token = None
        for pattern in patterns.items():
            aim = re.match(pattern[1], data)
            if aim and (token is None or len(aim.group(0)) > len(token[0])):
                token = [aim.group(0), pattern[0]]  # token[token, tag]
        # print(token)

        # 记录token位置
        if token[0] == '\n':
            pos[0] += 1
            pos[1] = 1
        pos[1] += len(token[0])

        data = data.replace(token[0], '', 1)  # 将已匹配到的token删去
        # print(data)

        if token[1] == 'UNDEFINED_SYMBOL':
            e.table.append(LexerError(message='Unidentified character', pos=(pos[0], pos[1]), token=token[0]))  # 非法字符异常
            continue

        if token[1] != 'BLANK':
            if token[0].isdecimal():  # 将整数转换为二进制
                token.append(str(bin(int(token[0]))))
            else:
                token.append(token[0])
            res.append(token)
            tokens.append({'type': token[1], 'value': token[0], 'pos': (pos[0], pos[1])})
    return res, tokens, e


if __name__ == '__main__':
    test_data = load_data('../data/right.pl0')
    print(analyze(test_data)[1])

