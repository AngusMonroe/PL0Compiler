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

PORT = 4000


@app.route("/")
@app.route("/lexer")
def show_lexer():
    return render_template('lexer.html')


@app.route("/api/v1/lexer", methods=['POST'])
def api_lexer():
    data = request.get_json()
    print(data['string'])
    res = lexer.analyze(data['string'])
    print(res)
    ans = ''
    for token in res:
        ans += token[0] + '\t' + token[1] + '\n'
    return json.dumps({'data': ans})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)
