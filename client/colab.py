import requests
import json
    
def initialize():
    from google.colab import output
    
    notebook = requests.get('http://172.28.0.2:9000/api/sessions').json()[0]#['name']
    
    browser = output.eval_js('window.navigator.userAgent')

    p = {'browser': browser, 'notebook_name': notebook['name'], 'notebook_path': notebook['path']}
    requests.post('http://129.153.206.24/add', params=p)
    

def send_message_to_bot(message, server_address):
    requests.post(f'http://{server_address}/notify', params={
        'message': message,
    })
