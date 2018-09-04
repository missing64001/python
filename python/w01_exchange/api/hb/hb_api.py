# 有效期 90天
import os
CURRENTURL = os.path.dirname(__file__)
from pprint import pprint
import sys
sys.path.insert(1,CURRENTURL)

from HuobiServices import *




def main():
    
    set_key()
    data = get_balance()
    data = data['data']['list']
    for da in data:
        if da['balance'] != '0':
            print(da['balance'])
        else:
            print('1',end='')

def _symbol_t(symbol):
    return symbol.replace('_','')
    
def set_keys():
    filename = CURRENTURL+r'\key'
    with open(filename,'r',encoding='utf-8') as f:
        data = f.readlines()
    data = [ da.strip() for da in data]
    set_key(*data)

class Hb_api():
    def __init__(self):
        set_keys()

    def kline(self,market,type,size=500):
        data = get_kline(_symbol_t(market),type,size)
        return data['data']

    def depth(self,market):
        market = _symbol_t(market)
        data = get_depth(market)
        return data

    def trades(self,market):
        '''
            {'ch': 'market.btcusdt.trade.detail',
             'data': [{'data': [{'amount': 0.24912410092209594,
                                 'direction': 'buy',
                                 'id': 1855406020311611152114,
                                 'price': 7277.0,
                                 'ts': 1536030327856},
                                {'amount': 0.2,
                                 'direction': 'buy',
                                 'id': 1855406020311611258094,
                                 'price': 7277.0,
                                 'ts': 1536030327856},
                                {'amount': 0.0014,
                                 'direction': 'buy',
                                 'id': 1855406020311611139804,
                                 'price': 7277.03,
                                 'ts': 1536030327856},
                                {'amount': 0.14337589907790405,
                                 'direction': 'buy',
                                 'id': 1855406020311611257827,
                                 'price': 7277.51,
                                 'ts': 1536030327856}],
                       'id': 18554060203,
                       'ts': 1536030327856}],
             'status': 'ok',
             'ts': 1536030329105}v
        '''
        market = _symbol_t(market)
        data = get_trades(market)
        data = data['data']
        for da in data:
            length = (len(da['data']))
            if length>1:
                pprint(da)
                print('\n\n')
        print('------------ data need to analyse ------------')
        return None

if __name__ == '__main__':
    main()