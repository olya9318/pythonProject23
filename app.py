import os

from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def do_cmd(cmd, value, data):
    if cmd == 'filter':
        result = list(filter(lambda record: value in record, data))
    elif cmd == 'map':
        col_num = int(value)
        result = list(map(lambda record: record.split()[col_num], data))
    elif cmd == 'unique':
        result = list(set(data))
    elif cmd == 'sort':
        reverse = (value == 'desc')
        result = sorted(data, reverse=reverse)
    elif cmd == 'limit':
        result = data[:int(value)]
    else:
        raise BadRequest
    return result


def do_query(params):
    with open(os.path.join(DATA_DIR, params["file_name"])) as f:
        file_data = f.readlines()
    res = file_data
    if 'cmd1' in params.keys():
        res = do_cmd(params['cmd1'], params['value1'], res)
    if 'cmd2' in params.keys():
        res = do_cmd(params['cmd2'], params['value2'], res)
    if 'cmd3' in params.keys():
        res = do_cmd(params['cmd3'], params['value3'], res)
    return res


@app.route("/perform_query", methods=["POST"])
def perform_query():
    data = request.json
    file_name = data["file_name"]
    if not os.path.exists(os.path.join(DATA_DIR, file_name)):
        raise BadRequest

    return jsonify(do_query(data))


if __name__ == "__main__":
    app.run(debug=True)
