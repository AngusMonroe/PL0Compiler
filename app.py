from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import sys
import json
from PL0Compiler import opa

app = Flask(__name__)

PORT = 5014

rules = opa.load_data('data/opa.txt')


@app.route("/lexer")
def show_lexer():
    return render_template('lexer.html')


@app.route("/opa")
def show_opa():
    global rules
    rules = opa.load_data('data/opa.txt')
    return render_template('opa.html')


@app.route("/")
@app.route("/compiler")
def show_compiler():
    return render_template('compiler.html')


@app.route("/api/v1/lexer", methods=['POST'])
def api_lexer():
    from PL0Compiler import lexer
    data = request.get_json()
    print(data['string'])
    res = lexer.analyze(data['string'])[0]
    # print(res)
    ans = 'Value\tType\tToken\n'
    for token in res:
        ans += token[2] + '\t' + token[1] + '\t' + token[0] + '\n'
    return json.dumps({'data': ans})


@app.route("/api/v1/opa", methods=['POST'])
def api_opa():
    global rules
    data = request.get_json()
    print(data)
    if data['grammar']:
        rules = data['grammar'].split('\n')
    opa.load_rules(rules)
    if opa.judge_grammar():
        # print_table(priority_tab)
        ans = opa.analyze(data['string'])
    else:
        ans = 'Not OPG grammar'
    return json.dumps({'data': ans})


@app.route("/api/v1/compiler", methods=['POST'])
def api_compiler():
    from PL0Compiler import parser
    parser.init()
    data = request.get_json()
    print(data['string'])
    try:
        pcode = parser.main(data['string'])
        ans = ''
        for ln, record in enumerate(pcode):
            ans += str(record.f) + ', ' + str(record.l) + ', ' + str(record.a) + '\n'
    except Exception:
        ans = 'Error!'
    return json.dumps({'data': ans})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)
