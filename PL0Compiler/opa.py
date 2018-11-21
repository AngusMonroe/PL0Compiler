
gramma = []
V = set()
V_n = set()
V_t = set()
priority_tab = dict()


def load_data(file_path):
    file = open(file_path, 'r', encoding='utf8')
    data = file.read().split('\n')
    file.close()
    return data


def load_rules(rules):
    for rule in rules:
        item = rule.split('->')  # item[0]为左侧短语，item[0]为右侧短语
        for r_item in item[1].split('|'):
            gramma.append({'left': item[0], 'right': r_item})  # 将形如"左短语->右短语"的文法保存为{left, right}的dict
    identifier = gramma[0]['left']
    for rule in gramma:
        for v in rule['right']:
            V.add(v)
        V_n.add(rule['left'])
    for v in V:
        if v not in V_n:
            V_t.add(v)


def cal_first_vt():
    stack = []
    first_vt = []
    for rule in gramma:
        b = None
        if rule['right'][0] in V_t:
            b = rule['right'][0]
        if len(rule['right']) >= 2 and rule['right'][0] in V_n and rule['right'][1] in V_t:
            b = rule['right'][1]
        if b and (rule['left'], b) not in first_vt:
            first_vt.append((rule['left'], b))
            stack.append((rule['left'], b))
        while len(stack) > 0:
            v, b = stack.pop(-1)
            for r in gramma:
                if r['right'][0] == v and (r['left'], b) not in first_vt:
                    first_vt.append((r['left'], b))
                    stack.append((r['left'], b))
    return first_vt


def cal_last_vt():
    stack = []
    last_vt = []
    for rule in gramma:
        b = None
        if rule['right'][-1] in V_t:
            b = rule['right'][-1]
        if len(rule['right']) >= 2 and rule['right'][-1] in V_n and rule['right'][-2] in V_t:
            b = rule['right'][-2]
        if b and (rule['left'], b) not in last_vt:
            last_vt.append((rule['left'], b))
            stack.append((rule['left'], b))
        while len(stack) > 0:
            v, b = stack.pop(-1)
            for r in gramma:
                if r['right'][-1] == v and (r['left'], b) not in last_vt:
                    last_vt.append((r['left'], b))
                    stack.append((r['left'], b))
    return last_vt


def judge_gramma():
    first_vt = cal_first_vt()
    last_vt = cal_last_vt()
    print(first_vt)
    print(last_vt)

    try:
        for rule in gramma:
            right = rule['right']
            for i in range(len(right) - 1):
                if right[i] in V_t and right[i + 1] in V_t:
                    if (right[i], right[i + 1]) in priority_tab and priority_tab[(right[i], right[i + 1])] != 0:
                        raise Exception('Not OPG')
                    else:
                        priority_tab[(right[i], right[i + 1])] = 0
                if i < len(right) - 2 and right[i] in V_t and right[i + 1] in V_n and right[i + 2] in V_t:
                    if (right[i], right[i + 2]) in priority_tab and priority_tab[(right[i], right[i + 2])] != 0:
                        raise Exception('Not OPG')
                    else:
                        priority_tab[(right[i], right[i + 2])] = 0
                if right[i] in V_t and right[i + 1] in V_n:
                    for x, b in first_vt:
                        if x == right[i + 1]:
                            if (right[i], b) in priority_tab and priority_tab[(right[i], b)] != -1:
                                raise Exception('Not OPG')
                            else:
                                priority_tab[(right[i], b)] = -1
                if right[i] in V_n and right[i + 1] in V_t:
                    for x, a in last_vt:
                        if x == right[i]:
                            if (a, right[i + 1]) in priority_tab and priority_tab[(a, right[i + 1])] != 1:
                                raise Exception('Not OPG')
                            else:
                                priority_tab[(a, right[i + 1])] = 1
        return True
    except Exception:
        print('Not OPG')
        return False


def analyze(data):
    print(priority_tab)
    pass


if __name__ == '__main__':
    data = 'i+i*(i+i)'
    rules = load_data('../data/opa.txt')
    load_rules(rules)
    if judge_gramma():
        analyze(data)
