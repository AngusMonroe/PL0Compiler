from PL0Compiler import lexer
from PL0Compiler.parser import PCodeList, PCodeOpt, analyze
from PL0Compiler.exception import *
import sys


def _interpret(pcodes, in_):

    def base(l):  # find base l levels down
        t = base_pointer
        for i in range(l):
            t = stack[t]
        return t
    res = ''
    program_counter = 0
    base_pointer = 0
    stack = [0, 0, 0]
    '''
        .last stack.
        base_pointer -> last level pointer (Static Link), used to trace variable location in stack
        +1           -> last base pointer (Dynamic Link)
        +2           -> last program counter
        +3           -> variable1
        +4           -> variable2
        ...
        +3+var_cnt-1 -> variableN
        ...          -> for operation uses
        len(stack)   -> None
    '''
    # try:
    cn = 0
    while True:
        cn += 1
        if cn >= 1000:
            break
        print(program_counter)
        code = pcodes[program_counter]
        print(code)
        program_counter += 1
        if code.f == PCodeList.LIT:
            stack.append(code.a)
        elif code.f == PCodeList.OPR:
            if code.a == 0:  # return
                current_base = base_pointer
                program_counter = stack[base_pointer+2]  # reset program counter
                base_pointer = stack[base_pointer+1]
                stack[current_base:] = []
            elif code.a == 1:
                stack.append(-stack.pop())
            elif code.a == 2:
                stack.append(stack.pop() + stack.pop())
            elif code.a == 3:
                stack.append(-stack.pop() + stack.pop())
            elif code.a == 4:
                stack.append(stack.pop() * stack.pop())
            elif code.a == 5:
                y = stack.pop()
                x = stack.pop()
                stack.append(x // y)
            elif code.a == 6:
                stack.append(stack.pop() % 2)
            elif code.a == 7:
                stack.append(int(stack.pop() == stack.pop()))
            elif code.a == 8:
                stack.append(int(stack.pop() != stack.pop()))
            elif code.a == 9:
                stack.append(int(stack.pop() > stack.pop()))
            elif code.a == 10:
                stack.append(int(stack.pop() <= stack.pop()))
            elif code.a == 11:
                stack.append(int(stack.pop() < stack.pop()))
            elif code.a == 12:
                stack.append(int(stack.pop() >= stack.pop()))
        elif code.f == PCodeList.LOD:
            stack.append(stack[base(code.l)+code.a])
        elif code.f == PCodeList.STO:
            stack[base(code.l)+code.a] = stack.pop()
        elif code.f == PCodeList.CAL:
            stack.append(base(code.l))
            stack.append(base_pointer)
            stack.append(program_counter)
            base_pointer = len(stack) - 3
            program_counter = code.a
        elif code.f == PCodeList.INT:
            stack.extend((0,)*(code.a-3))  # because 3 spaces have been allocated in CAL
        elif code.f == PCodeList.JMP:
            program_counter = code.a
        elif code.f == PCodeList.JPC:
            if stack.pop() == 0:
                program_counter = code.a
        elif code.f == PCodeList.RED:
            if len(in_):
                stack[base(code.l) + code.a] = int(in_[0])
                in_ = in_[1:]
            elif __name__ == '__main__':
                print('[In] ', end='')
                stack[base(code.l)+code.a] = int(input())
            else:
                raise InterpreterError('Invalid input')
        elif code.f == PCodeList.WRT:
            print('[Out]', stack[len(stack)-1])
            res += '[Out]' + str(stack[len(stack)-1]) + '\n'
        if program_counter == 0:  # main returns
            break

    print('Program finished!')
    # except InterpreterError as e:
    #     e.ln = program_counter
    #     raise e
    # except Exception as e:
    #     raise InterpreterError(e, program_counter)  # though pc++ at the beginning, ln = pc+1
    return res


def interpret(data, inputs):
    pcode = []
    datas = data.split('\n')
    for line in datas:
        item = line.split(', ')
        if len(item) == 3:
            pcode.append(PCodeOpt(item[0], item[1], item[2]))
    in_ = inputs.split('\n')
    print(len(in_))
    print(len(pcode))
    ans = _interpret(pcode, in_)
    print(ans)
    return ans


def main(data):
    in_ = ['4', '14']
    # file = open('../data/pcode.txt', 'r', encoding='utf8')
    # data = file.read()
    # file.close()
    # pcode = []
    # datas = data.split('\n')
    # for line in datas:
    #     item = line.split(', ')
    #     pcode.append(PCodeOpt(item[0], item[1], item[2]))
    pcode = analyze(data)
    print(_interpret(pcode, in_))


if __name__ == '__main__':
    test_data = lexer.load_data('../data/wrong1.pl0')
    pc = analyze(test_data)
    for record in pc:
        print(str(record) + '\n')
    main(test_data)
