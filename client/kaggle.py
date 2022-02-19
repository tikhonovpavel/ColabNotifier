import json
import requests


def initialize(wandb_run_id, notebook_name, browser, **config):

    """
    Example:
    
    wandb_run_id = '...'
    notebook_name = '...',
    browser = '...',
    source_lang = 'en',
    target_lang = 'ru',
    learning_rate = 0.0001,
    momentum = 0.5,
    training_steps = 10000,
    batch_size=2
    """
    result = {**locals(), **config}
    json.dump(result, open('config.json', 'w'))


def send_message_to_bot(message, server_address):
    config = json.load(open('config.json', 'r'))
    
    postfix = f"\n\n**{config['notebook_name']}**\n*{config['browser']}*\n*{config['source_lang']} to {config['target_lang']}*"
    
    requests.post(f'http://{server_address}/notify', params={
        'message': message + postfix,
    })
