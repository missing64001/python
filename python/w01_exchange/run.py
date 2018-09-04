
import os
CURRENTURL = os.path.dirname(__file__)
import sys
sys.path.insert(1,CURRENTURL)

from api.hb.hb_api import Hb_api
from pprint import pprint

api = Hb_api()

# data = api.kline('btc_usdt','1day',5)
# data = api.depth('btc_usdt')
# data = api.trades('btc_usdt')
# data = api.order('bts_usdt',1,1,'sell')
# data = api.getOrder(11621969025)
# data = api.unfinished_orders_list('bts_usdt')
# data = api.cancelOrder(11621969025)

pprint(data)















