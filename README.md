# ColabNotifier

It's a Telegram bot to track your Colab notebooks.

To automatically send message on start of notebook use:
```
from google.colab import output
import requests

notebook_name = requests.get('http://172.28.0.2:9000/api/sessions').json()[0]['name']
browser = output.eval_js('window.navigator.userAgent')

p = {'browser': browser, 'notebook_name': notebook_name, }
requests.post('<YOUR_SERVER_URL>/add', params=p)
```
