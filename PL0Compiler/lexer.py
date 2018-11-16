
import re

patterns = {
    'BLANK': '\s',
    'KEYWORD': 'const|var|procedure|if|then|else|while|do|call|begin|end|repeat|until|read|write|odd',
    'DELIMITER': '\.|\(|\)|,|;',
    'OPERATOR': '\+|-|\*|/|:=|=|<>|<=|<|>=|>',
    'IDENTIFIER': '[A-Za-z][A-Za-z0-9]*',
    'NUMBER': '\d+(\.\d+)?',
    'UNDEFINED_SYMBOL': '.'
}


def analyze(file_path):
    file = open(file_path, 'r', encoding='utf8')
    data = file.read()
    file.close()
    tokens = []
    while data:
        token = None
        for pattern in patterns.items():
            aim = re.match(pattern[1], data)
            if aim and (token is None or len(aim.group(0)) > len(token[0])):
                token = [aim.group(0), pattern[0]]  # token[token, tag]
        # print(token)
        data = re.sub(token[0], '', data, count=1)
        # print(data)
        if token[1] != 'BLANK':
            tokens.append(token)
    return tokens


if __name__ == '__main__':
    print(analyze('../data/test.txt'))
