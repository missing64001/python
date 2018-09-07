# 有效期 90天
import os
CURRENTURL = os.path.dirname(__file__)
from pprint import pprint
import sys
sys.path.insert(1,CURRENTURL)

from HuobiServices import *




def main():
    
    set_keys()
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

    def kline(self,symbol,type,size=500):
        data = get_kline(_symbol_t(symbol),type,size)
        data = data['data']
        data = [[da['id'],da['open'],da['high'],da['low'],da['close'],da['amount']] for da in data]
        return data

    def depth(self,symbol):
        symbol = _symbol_t(symbol)
        data = get_depth(symbol)
        return (data['tick']['asks'],data['tick']['bids'])

    def trades(self,symbol):
        '''
            {'ch': 'symbol.btcusdt.trade.detail',
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
        symbol_b = symbol
        symbol = _symbol_t(symbol)
        data = get_trades(symbol)
        data = data['data']
        res_datas = []
        for da in data:
            tid = da['id']
            date = int(da['ts']/1000)
            type = None
            total = 0
            amount = 0
            for d in da['data']:
                if not type:
                    type = d['direction']
                else:
                    if type != d['direction']:
                        raise ValueError(type + '___' + d['direction'])
                total += d['price'] * d['amount']
                amount += d['amount']
            price = total / amount
            # res_datas.append({'tid':tid,'date':date,'type':type,'amount':amount,'price':price})
            res_datas.append((tid,symbol_b,date,price,amount,type))
        return res_datas

    def balance(self):
        data = get_balance()

        data = data['data']['list']
        data = filter( lambda x:x['balance'] != '0',data)
        data = list(data)
        data_free = { da['currency']:da['balance'] for da in data if da['type'] == 'trade'}
        data_freezed = { da['currency']:da['balance'] for da in data if da['type'] == 'frozen'}
        return data_free,data_freezed

    def order(self,symbol,price,amount,type):
        '''
            {'data': '11621969025', 'status': 'ok'}
        '''
        symbol = _symbol_t(symbol)
        if type == 'sell':
            type = 'sell-limit'
        elif type == 'buy':
            type = 'buy-limit'
        data = send_order(symbol, price , amount, type)
        data = data['data']
        return data

    def getOrder(self,id,symbol=None):
        '''
            {'data': {'account-id': 4813361,
                      'amount': '1.000000000000000000',
                      'canceled-at': 0,
                      'created-at': 1536043361830,
                      'field-amount': '0.0',
                      'field-cash-amount': '0.0',
                      'field-fees': '0.0',
                      'finished-at': 0,
                      'id': 11621969025,
                      'price': '1.000000000000000000',
                      'source': 'api',
                      'state': 'submitted',
                      'symbol': 'btsusdt',
                      'type': 'sell-limit'},
             'status': 'ok'}
        '''
        data = order_info(id)
        return data
    def unfinished_orders_list(self,symbol):
        symbol = _symbol_t(symbol)
        data = orders_list(symbol)
        data = data['data']
        return data

    def cancelOrder(self,id,symbol=None):
        '''
            {'data': '11621969025', 'status': 'ok'}
        '''
        data = cancel_order(id)
        print(data)
        if str(id) == str(data['data']):
            return 1000
        return 3001

if __name__ == '__main__':
    main()