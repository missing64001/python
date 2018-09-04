
import os
CURRENTURL = os.path.dirname(__file__)
import sys
sys.path.insert(1,CURRENTURL)

from api.hb.hb_api import Hb_api
from pprint import pprint

hb_api = Hb_api()
# data = hb_api.kline('btc_usdt','1day',5)
# data = hb_api.depth('btc_usdt')
data = hb_api.trades('btc_usdt')
# pprint(data)















