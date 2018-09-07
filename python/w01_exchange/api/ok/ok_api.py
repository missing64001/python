



import json, hashlib,struct,time,sys
import urllib.request
import urllib.parse as parse
from pprint import pprint
import sys

import os
CURRENTURL = os.path.dirname(__file__)
sys.path.insert(1,CURRENTURL)
# print(CURRENTURL)
from OkcoinSpotAPI import OKCoinSpot

class Ok_api:
	
    def __init__(self, mykey=None, mysecret=None):
        if mykey and mysecret:
            self.mykey,self.mysecret = mykey,mysecret
        else:
            filename = CURRENTURL+r'\key'
            with open(filename,'r',encoding='utf-8') as f:
                data = f.read()
            self.mykey,self.mysecret = data.split('\n')
            self.mykey = self.mykey.strip()
            self.mysecret = self.mysecret.strip()

        okcoinRESTURL = 'www.okb.com'
        # print(self.mykey,self.mysecret)
        self.okcoinSpot = OKCoinSpot(okcoinRESTURL,self.mykey,self.mysecret)

    def __api_public_call(self,path,params=''):
        headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36 Maxthon/5.1.3.2000',
        }
        try:
            url = 'https://www.okb.com/api/v1/' + path + params
            req = urllib.request.Request(url,headers=headers)
            res = urllib.request.urlopen(req, timeout=10)
            doc = json.loads(res.read().decode('utf-8')) # .decode('gbk', 'ignore')
            return doc
        except Exception as ex:
            print(sys.stderr, 'ok request public_ex: ', ex)
            return None

            



    def trades(self,symbol='btc_usdt',since=0):
        '''
            return (tid,symbol,date,price,amount,type)
        '''

        try:
            data = self.okcoinSpot.trades(symbol,since)
            lst = [da['tid'] for da in data]
            return [(da['tid'],symbol,da['date'],da['price'],da['amount'],da['type']) for da in data]
        except Exception as e:
            # raise e
            print('ok_api_ trades' ,e)
            return []

    def kline(self,symbol,type,size=500):
        '''
            symbol
            type
            size
            since

            https://www.okb.com/api/v1/kline.do
        '''
        try:
            path = 'kline.do?'
            params = "symbol=%s&type=%s&size=%s" %(symbol,type,size)
            obj = self.__api_public_call(path, params)
            # print (obj)
            return obj
        except Exception as ex:
            print(sys.stderr, 'ok %s exception ,'%path,ex)
            return None

    def depth(self,symbol = ''):
        data = self.okcoinSpot.depth(symbol)
        return [data['asks'][::-1],data['bids']]


    def balance(self):
        data = self.okcoinSpot.userinfo()



        data_free = data['info']['funds']['free']
        data_freezed = data['info']['funds']['freezed']
        data = filter( lambda x:data_free[x] != '0',data_free)
        data_free = { da:data_free[da]     for da in data_free if data_free[da] != '0'}
        data_freezed = { da:data_freezed[da] for da in data_freezed if data_freezed[da] != '0'}
        return data_free,data_freezed

        
    def order(self,symbol,price,amount,type):
        data = self.okcoinSpot.trade(symbol,price,amount,type)
        return data

    def getOrder(self,id,symbol=None):
        '''
            {'orders': [{'amount': 1,
                         'avg_price': 0,
                         'create_date': 1536112711000,
                         'deal_amount': 0,
                         'order_id': 864345207,
                         'orders_id': 864345207,
                         'price': 10.0,
                         'status': 0,
                         'symbol': 'eos_usdt',
                         'type': 'sell'}],
             'result': True}
        '''
        data = self.okcoinSpot.orderinfo(symbol,id)
        return data






    def unfinished_orders_list(self,symbol):
        '''{'currency_page': 1,
             'orders': [{'amount': 1,
                         'avg_price': 0,
                         'create_date': 1536112711000,
                         'deal_amount': 0,
                         'order_id': 864345207,
                         'orders_id': 864345207,
                         'price': 10.0,
                         'status': 0,
                         'symbol': 'eos_usdt',
                         'type': 'sell'}],
             'page_length': 200,
             'result': True,
             'total': 1}



             [{'amount': 1,
               'avg_price': 0,
               'create_date': 1536112711000,
               'deal_amount': 0,
               'deal_money': 0,
               'order_id': 864345207,
               'price': 10.0,
               'type': 'sell'}]
        '''
        def deal_order_data(data,lst):
            resl = []
            for da in data:
                d = {}
                for l in lst:
                    d[l] = da[l]
                resl.append(d)
            return resl

        data = self.okcoinSpot.orderHistory(symbol)
        data = data['orders']
        data = deal_order_data(data,['amount','price','deal_amount','avg_price','create_date','order_id','type'])
        [da.update({'deal_money':da['deal_amount']*da['avg_price']}) for da in data]
        return data


    def cancelOrder(self,id,symbol):
        '''
            {'orders': [{'amount': 1,
                         'avg_price': 0,
                         'create_date': 1536112711000,
                         'deal_amount': 0,
                         'order_id': 864345207,
                         'orders_id': 864345207,
                         'price': 10.0,
                         'status': 0,
                         'symbol': 'eos_usdt',
                         'type': 'sell'}],
             'result': True}
        '''
        data = self.okcoinSpot.ordersinfo(symbol,id)
        return data
    # 
    # 
if __name__ == '__main__':
    print(1)
    api = ok_api()
    data = api.trades('eos_btc',211342002)



    print(list(data))