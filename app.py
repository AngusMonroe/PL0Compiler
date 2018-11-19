from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from PL0Compiler import lexer
import sys
import json

app = Flask(__name__)

PORT = 5000


@app.route("/")
@app.route("/lexer")
def show_lexer():
    return render_template('lexer.html')


@app.route("/api/v1/lexer", methods=['POST'])
def api_lexer():
    data = request.get_json()
    print(data['string'])
    res = lexer.analyze(data['string'])
    # print(res)
    ans = ''
    for token in res:
        ans += token[2] + '\t' + token[1] + '\t' + token[0] + '\n'
    # ans = []
    # for token in res:
    #     ans.append({'value': token[2], 'type': token[1], 'token': token[0]})
    return json.dumps({'data': ans})
    # return render_template('lexer.html', temp=res)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)
