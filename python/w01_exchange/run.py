
# import os
# CURRENTURL = os.path.dirname(__file__)
# import sys
# print(os.path.abspath(''))
# exit(0)


from __init__ import deal_e
from api.hb.hb_api import Hb_api #02@ m1 bts_usdt
from api.zb.zb_api import Zb_api
from api.ok.ok_api import Ok_api
LOCALS = locals()
from pprint import pprint

def main():
    api = Trade('ok')
    test(api)
    try:
        0 / 0
    except Exception:
        deal_e()


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
        api = LOCALS[exchange.capitalize()+'_api']()
        self.api = api
        self.exchange = exchange
    def __getattr__(self,name):
        data = getattr(self.api,name)
        data = dec(data)
        return data

def test(api):
    # data = api.kline('btc_usdt','1day',5) #dohlcv
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












