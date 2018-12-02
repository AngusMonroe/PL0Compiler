from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from PL0Compiler import lexer, opa
import sys
import json

app = Flask(__name__)

PORT = 5000

rules = opa.load_data('data/opa.txt')


@app.route("/lexer")
def show_lexer():
    return render_template('lexer.html')


@app.route("/")
@app.route("/opa")
def show_opa():
    global rules
    rules = opa.load_data('data/opa.txt')
    return render_template('opa.html')


@app.route("/api/v1/lexer", methods=['POST'])
def api_lexer():
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
    ans = ''
    if opa.judge_grammar():
        # print_table(priority_tab)
        ans = opa.analyze(data['string'])
    else:
        ans = 'Not OPG grammar'
    return json.dumps({'data': ans})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)
