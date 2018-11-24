
grammar = []
V = set()
V_n = set()
V_t = set()
priority_tab = dict()
map = {'1': '>', '0': '=', '-1': '<'}


def load_data(file_path):
    file = open(file_path, 'r', encoding='utf8')
    data = file.read().split('\n')
    file.close()
    return data


def load_rules(rules):  # 计算V，V_n和V_t
    for rule in rules:
        item = rule.split('->')  # item[0]为左侧短语，item[0]为右侧短语
        for r_item in item[1].split('|'):
            grammar.append({'left': item[0], 'right': r_item})  # 将形如"左短语->右短语"的文法保存为{left, right}的dict
    for rule in grammar:
        for v in rule['right']:
            V.add(v)
        V_n.add(rule['left'])
    for v in V:
        if v not in V_n:
            V_t.add(v)


def cal_first_vt():  # 计算FIRSTVT
    stack = []
    first_vt = []
    for rule in grammar:
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
            for r in grammar:
                if r['right'][0] == v and (r['left'], b) not in first_vt:
                    first_vt.append((r['left'], b))
                    stack.append((r['left'], b))
    return first_vt


def cal_last_vt():  # 计算LASTVT
    stack = []
    last_vt = []
    for rule in grammar:
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
            for r in grammar:
                if r['right'][-1] == v and (r['left'], b) not in last_vt:
                    last_vt.append((r['left'], b))
                    stack.append((r['left'], b))
    return last_vt


def print_table(dict):  # 输出优先级矩阵
    list_V_t = list(V_t)
    table = [([''] * len(list_V_t)) for i in range(len(list_V_t))]

    for pos in dict.keys():
        if pos[0] in V_t and pos[1] in V_t:
            table[list_V_t.index(pos[0])][list_V_t.index(pos[1])] = map[str(dict[pos])]
    ans = ' '
    for token in list_V_t:
        ans += '\t' + token
    ans += '\n'
    for i, line in enumerate(table):
        ans += list_V_t[i]
        for word in line:
            ans += '\t' + word
        ans += '\n'
    print(ans)


def judge_grammar():
    first_vt = cal_first_vt()
    last_vt = cal_last_vt()

    try:
        for rule in grammar:
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


def sub(string, p, c):
    new = []
    for s in string:
        new.append(s)
    new[p] = c
    return ''.join(new)


def reduction(seg):
    for i in range(len(seg)):
        if seg[i] in V_n:
            seg = sub(seg, i, '%')
    for rule in grammar:  # 对seg进行规约
        tmp = ''
        for i in range(len(rule['right'])):
            if rule['right'][i] in V_n:
                tmp += '%'
            else:
                tmp += rule['right'][i]
        if seg == tmp:
            return rule['left']


def analyze(data):
    flag = True
    identifier = grammar[0]['left']
    template = \
        '{step:>4}    {stack:{program_length}}    {priority:^8}    {cur_sym:^7}    {remaining:{program_length}}' \
        .replace('{program_length}', str(max(8, len(data))))
    stack = []
    cur = 0
    step = 1
    ans = template.format(step='STEP', stack='STACK', priority='PRIORITY', cur_sym='CUR_SYM', remaining='REMAINS') + '\n'
    while cur <= len(data):
        priority = -1

        if cur == len(data):  # 表达式处理完毕
            if len(stack) == 1 and stack[-1] == identifier:  # stack中仅剩余一个值
                ans +=template.format(step=step, stack=''.join(stack), priority='END', cur_sym='', remaining='') + '\n'
                break
            else:  # 仍可继续规约
                cur_sym = ''
                priority = 1
        else:
            cur_sym = data[cur]
            try:
                for i in range(len(stack) - 1, -1, -1):  # 倒序遍历stack，步长为-1
                    if stack[i] in V_t:  # 找到终结符，查优先级矩阵获得其优先级
                        priority = priority_tab[(stack[i], cur_sym)]
                        break
            except Exception:
                flag = False

        if not flag:
            break

        ans += template.format(
            step=step,
            stack=''.join(stack),
            priority='?' if priority is None else map[str(priority)],
            cur_sym=cur_sym,
            remaining=data[min(len(data), cur + 1):]) + '\n'

        if step == 20:
            break

        if priority == 1:  # 进行规约
            seg = ''  # 待规约字符串
            a = None  #
            while True:  # 找到规约字符串
                if stack[-1] in V_t:  # 栈顶元素是终结符
                    if a and priority_tab[(stack[-1], a)] == -1:  # 栈顶元素优先级大于待入栈元素
                        break
                    else:
                        a = stack[-1]
                seg = stack.pop() + seg
                if len(stack) == 0:
                    break

            res = reduction(seg)

            if res:  # 将规约得到的非终结符入栈
                stack.append(res)
            else:
                flag = False
                # print('Error at {}'.format(cur))
                break
        elif priority == 0 or priority == -1:  # 进行移入
            stack.append(cur_sym)
            cur += 1
        else:
            flag = False
            # print('Error at {}'.format(cur))
            break

        step += 1
    if flag:
        return ans
    else:
        return ans + '\n' + 'Error at {}'.format(cur)

if __name__ == '__main__':
    data = 'i+i*(i+i)'
    rules = load_data('../data/opa.txt')
    load_rules(rules)
    if judge_grammar():
        # print_table(priority_tab)
        print(analyze(data))
