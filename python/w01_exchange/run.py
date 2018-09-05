
import os
CURRENTURL = os.path.dirname(__file__)
import sys
sys.path.insert(1,CURRENTURL)

from api.hb.hb_api import Hb_api
from api.zb.zb_api import Zb_api
from api.ok.ok_api import Ok_api
from pprint import pprint



def main():
    api = Ok_api()
    test(api)
    exit()
    api = Zb_api()
    test(api)

# 11629784439
# 11629565010
def test(api):
    # data = api.kline('btc_usdt','1day',5) #dohlcv
    # data = api.depth('btc_usdt')
    # data = api.trades('btc_usdt');data = (len(data),data[0])
    # data = api.order('eos_usdt',10,1,'sell')
    # data = api.unfinished_orders_list('eos_usdt')
    # data = api.getOrder(864345207,'eos_usdt')
    # data = api.cancelOrder('864345207','eos_usdt')
    pprint(data)



if __name__ == '__main__':
    main()












