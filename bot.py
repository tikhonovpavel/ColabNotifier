import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from tinydb import TinyDB
import datetime

from utils import load_config

config = load_config()
DEFAULT_MESSAGE = 'Done'

db = TinyDB(config['database_path'])
table = db.table('log')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def get_list():
    result = []

    for x in table:
        if 'timestamp' not in x:
            continue

        x['timestamp'] = datetime.datetime.fromtimestamp(x['timestamp']).strftime("%Y-%m-%d, %H:%M:%S")
        result.append(x)
        print(x)

    return result


def get_browser(raw_browser):
    if 'Opera' in raw_browser or 'OPR' in raw_browser:
        return 'Opera'
    elif 'YaBrowser' in raw_browser:
        return 'Yandex Browser'
    elif 'Chrome' in raw_browser:
        return 'Chrome'
    elif 'Safari' in raw_browser:
        return 'Safari'
    elif 'Firefox' in raw_browser:
        return 'Firefox'
    elif 'Edg' in raw_browser:
        return 'Edge'
    elif 'IE' in raw_browser:
        return 'Internet Explorer'
    else:
        return raw_browser
    

def prepare_list(notebook_name, n):
    result = []
    candidates = get_list()
    candidates = [c for c in candidates if
                  not notebook_name or (notebook_name in (c.get('notebook_name') if c.get('notebook_name') else ''))]
    for x in candidates[-n:]:
        try:
            result.append(f"Notebook name: {x['notebook_name']}")
            result.append(f"Time: {x['timestamp']}")
            result.append(f"Browser: {get_browser(x['browser'])}")
            result.append('')
            result.append('')
        except Exception as err:
            print(err)
            print(x)
            continue

    return result


def notify(message=None):
    Updater(config['bot_token']).bot.sendMessage(chat_id=config['trusted_user_id'],
                                                 text=message if message else DEFAULT_MESSAGE)


def listall_command(update: Update, context: CallbackContext) -> None:
    print('listall')
    print(context.args)
    notebook_name = context.args[0] if len(context.args) > 0 else None

    if update.effective_user.id != config['trusted_user_id']:
        return

    result = prepare_list(notebook_name, 0)
    if len(result) > 0:
        update.message.reply_text('\n'.join(result))
    else:
        update.message.reply_text('Zero results')


def list_command(update: Update, context: CallbackContext) -> None:
    print('list')
    print(context.args)
    notebook_name = context.args[0] if len(context.args) > 0 else None

    if update.effective_user.id != config['trusted_user_id']:
        return

    result = prepare_list(notebook_name, config['max_message_length'])
    if len(result) > 0:
        update.message.reply_text('\n'.join(result))
    else:
        update.message.reply_text('Zero results')


def start_bot() -> None:
    updater = Updater(config['bot_token'])

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("list", list_command))
    dispatcher.add_handler(CommandHandler("listall", listall_command))

    updater.start_polling()
    updater.idle()
