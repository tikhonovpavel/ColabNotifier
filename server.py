from flask import Flask
from tinydb import TinyDB
import datetime
from flask import request, jsonify
import threading

import bot
from utils import load_config

config = load_config()
db = TinyDB(config['database_path'])
table = db.table('log')

app = Flask(__name__)


@app.route('/')
def index():
    return ''


def get_list():
    result = []

    for x in table:
        if 'timestamp' not in x:
            continue

        x['timestamp'] = datetime.datetime.fromtimestamp(x['timestamp']).strftime("%Y-%m-%d, %H:%M:%S")
        result.append(x)
        print(x)

    return result


@app.route('/notify', methods=['GET', 'POST'])
def notify():
    message = request.args.get('message', None)

    bot.notify(message)

    return jsonify({'ok': True})


@app.route('/add', methods=['GET', 'POST'])
def add():
    table.insert({'count': len(list(table)) + 1,
                  'timestamp': datetime.datetime.now().timestamp(),
                  'browser': request.args.get('browser'),
                  'notebook_name': request.args.get('notebook_name')})

    return jsonify(get_list())


if __name__ == "__main__":
    threading.Thread(target=bot.start_bot).start()
    app.run(host='0.0.0.0', port=80)
