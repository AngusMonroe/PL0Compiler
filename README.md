# PL0Compiler

## PL0Compiler Server

http://166.111.5.228:5014/

![x887.11.52.png](https://i.loli.net/2018/11/17/5bf012597b16c.png)

![x888.57.40.png](https://i.loli.net/2018/11/17/5bf0121528b77.png)

## Algorithm

A lexical analysis of the input code or code file, the types of identifiable words include the following:

- `BLANK`: blank symbol
- `KEYWORD`: reserved word
- `DELIMITER`: delimiter
- `OPERATOR`: operator
- `IDENTIFIER`: identifier
- `NUMBER`: constant(Support for decimals)
- `UNDEFINED_SYMBOL`: undefined symbol

For the above several word types, the regular expressions are summarized and matched:

- BLANK: `\s`
- KEYWORD: `const|var|procedure|if|then|else|while|do|call|begin|end|repeat|until|read|write|odd`
- DELIMITER: `\.|\(|\)|,|;`
- OPERATOR: `\+|-|\*|/|:=|=|<>|<=|<|>=|>`
- IDENTIFIER: `[A-Za-z][A-Za-z0-9]*`
- NUMBER: `\d+(\.\d+)?`
- UNDEFINED_SYMBOL: `.`

## File Orgnization

```
|- [dir] PL0Compiler (Main code of compiler)
	|- lexer.py (Lexical analyzer code)
|- [dir] static (HTML code)
|- [dir] templates (HTML code)
|- [dir] doc (Project documentation)
	|- PL0文法.txt 
	|- symbol_list.txt (Symbol list)
|- [dir] data (Test files)
|- app.py (Project entrance) 
|- README.md
```

## Usage

### Input

```
var a = 2;
```

### Output

| value | type | original string |
| --- | --- | ---- |
| var | KEYWORD | var |
| a	 |IDENTIFIER | a |
| =	 |OPERATOR | = |
| 10 |	NUMBER | 2 |
| ; | DELIMITER | ; |
