# PL0Compiler

## PL0Compiler Server 

http://www.angusmonroe.cn/interpreter
  
项目地址： https://github.com/AngusMonroe/PL0Compiler 

![屏幕快照 2018-12-24 下午11.13.45.png](https://i.loli.net/2018/12/24/5c20f7b990e56.png)

其他各模块地址

| 模块 | 地址 |
|----|----|
| 解释器 |  http://www.angusmonroe.cn/interpreter |
| 递归下降分析 | http://www.angusmonroe.cn/parser |
| 算符优先分析 | http://www.angusmonroe.cn/opa |
| 词法分析 | http://www.angusmonroe.cn/lexer |

## 文法

```
<程序> ::= <分程序>.
<分程序> ::= [<常量说明部分>][变量说明部分>][<过程说明部分>]<语句>
<常量说明部分> ::= const<常量定义>{,<常量定义>};
<常量定义> ::= <标识符>=<无符号整数>
<无符号整数> ::= <数字>{<数字>}
<标识符> ::= <字母>{<字母>|<数字>}
<变量说明部分>::= var<标识符>{,<标识符>};
<过程说明部分> ::= <过程首部><分程序>;{<过程说明部分>}
<过程首部> ::= procedure<标识符>;
<语句> ::= <赋值语句>|<条件语句>|<当型循环语句>|<过程调用语句>|<读语句>|<写语句>|<复合语句>|<重复语句>|<空>
<赋值语句> ::= <标识符>:=<表达式>
<表达式> ::= [+|-]<项>{<加法运算符><项>}
<项> ::= <因子>{<乘法运算符><因子>}
<因子> ::= <标识符>|<无符号整数>|'('<表达式>')'
<加法运算符> ::= +|-
<乘法运算符> ::= *|/
<条件> ::= <表达式><关系运算符><表达式>|odd<表达式>
<关系运算符> ::= =|<>|<|<=|>|>=
<条件语句> ::= if<条件>then<语句>[else<语句>]
<当型循环语句> ::= while<条件>do<语句>
<过程调用语句> ::= call<标识符>
<复合语句> ::= begin<语句>{;<语句>}end
<重复语句> ::= repeat<语句>{;<语句>}until<条件>
<读语句> ::= read'('<标识符>{,<标识符>}')'
<写语句> ::= write'('<标识符>{,<标识符>}')'
<字母> ::= a|b|...|X|Y|Z
<数字> ::= 0|1|2|...|8|9
```

## 系统结构

![图片 1.png](https://i.loli.net/2018/12/24/5c20f58d2344d.png)

## 目录结构 

```
 |- [dir] PL0Compiler (编译器主要代码)
	|- lexer.py (词法分析器代码)
	|- opa.py (算符优先分析代码)
	|- parser.py (递归下降分析代码)
	|- exception.py (错误处理代码)
	|- interpreter.py (解释器代码)
|- [dir] static (HTML代码)
|- [dir] templates (HTML代码)
|- [dir] doc (项目文档)
	|- [dir] 实验报告
	|- PL0文法.txt 
	|- symbol_list.txt (词语分类表)
|- [dir] data (测试文件)
|- app.py (应用入口) 
|- README.md
```

## 词法分析

对输入的代码或代码文件进行词法分析，可识别的词语类型包含以下几种： 

- BLANK: 空白字符 
- KEYWORD: 保留字 
- DELIMITER: 分隔符 
- OPERATOR: 运算符 
- IDENTIFIER: 变量 
- NUMBER: 常数(支持小数) 
- UNDEFINED_SYMBOL: 未声明字符 

## 符号表管理

符号表为list，其中元素为Record类对象，Record类结构如下：

| 属性 | 含义 |
|----|----|
| type |  类型，包括var、const、procedure |
| name | 标识符名 |
| value | 值 |
| level | 层次 |
| address | const的address为None，var的address为其偏移量，过程的address为其第一个PCode地址 |

## 递归下降法语义分析

![屏幕快照 2018-12-25 上午12.36.47.png](https://i.loli.net/2018/12/25/5c210b3387655.png)

![屏幕快照 2018-12-25 上午12.45.16.png](https://i.loli.net/2018/12/25/5c210d23b10c3.png)

##P-Code

P-code 语言：一种栈式机的语言。此类栈式机没有累加器和通用寄存器，有一个栈式存储器，有四个控制寄存器（指令寄存器 I，指令地址寄存器 P，栈顶寄存器 T和基址寄存器 B），算术逻辑运算都在栈顶进行。

指令格式：<操作码 f> <层次差 l> <参数 a>

| 指令  | 具体含义          |
| ------- |--------------------------- |
| LIT 0, a | 取常量a放到数据栈栈顶                         |
| OPR 0, a | 执行运算，a表示执行何种运算(+ - * /)，a为0时为return |
| LOD l, a | 取变量放到数据栈栈顶(相对地址为a,层次差为l)            |
| STO l, a | 将数据栈栈顶内容存入变量(相对地址为a,层次差为l)          |
| CAL l, a | 调用过程(入口指令地址为a,层次差为l)                |
| INT 0, a | 数据栈栈顶指针增加a                          |
| JMP 0, a | 无条件转移到指令地址a                         |
| JPC 0, a | 条件转移到指令地址a                          |

## 编译时符号表

| NAME   | KIND           | VAL/LEV     | ADDR      | SIZE |
| ------ | -------------- | ----------- | --------- | ---- |
| NAME：A | KIND:CONSTANT  | VAL:35      |           |      |
| NAME：B | KIND:CONSTANT  | VAL:49      |           |      |
| NAME：C | KIND:VARIABLE  | LEVEL:LEV   | ADDR:DX   |      |
| NAME：D | KIND:VARIABLE  | LEVEL:LEV   | ADDR:DX+1 |      |
| NAME：E | KIND:VARIABLE  | LEVEL:LEV   | ADDR:DX+2 |      |
| NAME：P | KIND:PROCEDURE | LEVEL:LEV   | ADDR:     |      |
| NAME：G | KIND:VARIABLE  | LEVEL:LEV+1 | ADDR:DX   |      |




## 异常处理

错误列表为list，其中元素为由Exception类继承而来的ParserError类对象，ParserError类结构如下：

| 属性 | 含义 |
|----|----|
| type |  错误类型 |
| message | 报错信息 |
| pos | 错误位置 |
| token | 出错token |

除书上给出的26种异常外，本系统还额外定义了程序非正常结束、重复声明、非法字符、字符类型错误等错误，总计处理了30种异常。

在这里针对这些异常，每一个我都编写了测试文件进行针对性的测试，测试文件放置在`PL0Compiler/data`目录下，比如id为1的异常对应的测试文件就是`e1.txt`以此类推。

```
'0': 'UndeclaredError with token "' + token + '"',  # 未定义错误
'1': 'Must be "=" instead of ":="',  # 应是=而不是:=
'2': 'Must be NUMBER after "="',  # =后应为数
'3': 'Must be "=" after IDENTIFIER',  # 标识符后应为=
'4': 'Must be IDENTIFIER after "' + token + '"',  # const,var,procedure后应为标识符
'5': 'Expected "' + token + '" but not found',  # 漏掉,或;
'6': 'Incorrect token after procedure declaration',  # 过程说明后的符号不正确
'7': 'Must be statement',  # 应为语句
'8': 'Incorrect token after statement in program',  # 程序体内语句部分后的符号不正确
'9': 'Must be "."',  # 应为.
'10': 'Expected ";" between statements',  # 语句之间漏;
'11': 'Undefined IDENTIFIER "' + token + '"',  # 标识符未声明
'12': 'Can not assign for const or procedure',  # 不可向常量或过程赋值
'13': 'Must be :=',  # 应为赋值运算符:=
'14': 'Must be IDENTIFIER after "call"',  # call后应为标识符
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
'25': 'Unexpected end of program',  # 程序非正常结束
'26': 'Duplicate symbol',  # 重复声明
'27': 'Unidentified character',  # 非法字符
'28': 'Unexpected symbol type',  # 字符类型错误
'30': 'Too big number',  # 这个数太大
'35': 'Other error',  # 其他错误
'40': 'Must be "("'  # 应为左括号
```

## 解释器（compiler/interpreter.py）

解释器的核心是一个栈，利用栈的上边进行表达式计算，用栈的内部实现运行栈。栈内存放的东西如下表所示

| 名称/偏移量       | 说明                         |
| ------------ | -------------------------- |
| 之前的栈         |                            |
| base_pointer | SL                         |
| +1           | DL                         |
| +2           | 之前的程序运行位置（program counter） |
| +3           | 变量1                        |
| +4           | 变量2                        |
| ...          |                            |
| +3+变量总数-1    | 变量N                        |
| ...          | 用于表达式计算                    |

SL用来追踪变量地址，DL用来记录上一个记录区的起始地址。如下图所示

![img](http://images.cnitblog.com/blog/464052/201312/27170831-bdf316b252044b2bba11a0abbe1cb680.png)



## Requirement

- Python 3.6
- Flask

## Usage 

`python3 app.py`

访问`0.0.0.0:8082/interpreter`

![IMG_2227.JPG](https://i.loli.net/2018/12/25/5c211746a4488.jpg)

## 实验感想

其实本来一开始在学期初的时候就立志不肝，尽早的保质保量完成实验，在一开始词法分析和算符优先分析两次实验的时候确实也是这样，早点动手做按部就班的完成了，然后就有点飘了，感觉编译的实验不过如此嘛，也没想象中那么难。于是在最后一次实验就差点翻车。

实验一开始我认为这次实验的难点主要在于递归下降分析生成P-code，然而花了两天就写差不多了，于是就跑去肝了数据挖掘和数管网管的ddl，等到距离编译ddl还有五天的时候才开始动手写错误处理，结果发现需要处理的异常个数和精度远超我想象，本来我觉得像pycharm那样只抛出一个错误就停止运行时比较符合程序员的使用习惯的，毕竟平时debug都是一处处的改，像codeblocks那样一次性抛出所有错误很容易导致后面的错是由于前面的错误导致的，从而产生大量的无意义报错，反而影响程序员debug，但由于实验要求是尽可能多的报出程序中所有的错误，这就涉及到如何在发现一个错误之后进行一定的skip后继续进行编译，这个skip还要设置得当，不能太大跳过过多正确代码，也不能太小没有将错误部分完全跳过。

在这里我的处理方法是每遇到一处错误就将这一行全部调过，可以算是一种稍稍有点大的skip，但本着宁可多跳一点也要保证跳过了全部错误代码的原则还是按照这个思路进行的实现。

此外，理解Pcode也是一个比较困难的地方，如果不能正确理解，就很难生成正确的Pcode代码，我在去年学长的工程的基础上输入了一些简单的例子对其生成的PCode进行理解，分析每类指令的作用，以及什么时候需要什么指令操作，只有对PCode有深刻理解了以后才能事半功倍。

BTW，最终能完整的实现一个编译器还是很有成就感的，也算是一个完整上线的项目了，1.4k python代码，2.2k html代码，希望以后也能对编程保有热情吧~

![屏幕快照 2018-12-25 上午1.42.10.png](https://i.loli.net/2018/12/25/5c211a7fd308c.png)