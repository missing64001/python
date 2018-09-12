from pprint import pprint
import sys 
import os
# sys.path.insert(1,os.path.abspath(os.path.dirname(__file__)+'\\..'))
from .import_myfn import deal_e





CURRENTURL = os.path.dirname(__file__)



APIS = {}
path = CURRENTURL
paths = {d:CURRENTURL+'/'+d for d in os.listdir(CURRENTURL) 
            if os.path.isdir(CURRENTURL+'/'+d) and d != '__pycache__'}
for exchange in paths:
    if exchange == 'err':
        continue

    # pprint(sys.path)
    sys.path.insert(1,CURRENTURL)
    # print('api.{0}.{0}_api'.format(exchange))
    m = __import__('{0}.{0}_api'.format(exchange))
    APIS[exchange] = getattr(m,(exchange+'_api'))
    APIS[exchange] = getattr(APIS[exchange],(exchange+'_api').capitalize())


def main():
    api = Trade('hb')
    test(api)
    # try:
    #     0 / 0
    # except Exception:
    #     deal_e()


def dec(fun):
    def inn(*args,**kw):
        try:
            data = fun(*args,**kw)
        except Exception:
            deal_e()
            data = None
        return data
    return inn

class Trade(object):
    def __init__(self, exchange):
        api = APIS[exchange]()
        self.api = api
        self.exchange = exchange
    def __getattr__(self,name):
        data = getattr(self.api,name)
        data = dec(data)
        return data

def test(api):
    data = api.kline('btc_usdt','1day',5) #dohlcv
    # data = api.depth('btc_usdt')
    # data = api.trades('btc_usdt');data = (len(data),data[0])
    # data = api.balance()
    # data = api.order('bts_usdt',1,1,'sell') #price,amount
    # data = api.unfinished_orders_list('bts_usdt')
    # data = api.getOrder(864345207,'eos_usdt')
    # data = api.cancelOrder('864345207','eos_usdt')
    # data = [   api.cancelOrder(da['id'],'bts_usdt')   for da in data ]
    pprint(data)

if __name__ == '__main__':
    main()












