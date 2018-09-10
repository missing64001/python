from flask import Flask
from api.api import Trade
import json



app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/kline',methods=['GET','POST'],endpoint='kline')
def kline():
    data = Trade('ok').kline('btc_usdt','1day',5)
    return json.dumps(data)

if __name__ == '__main__':
    app.run()

print(__name__)