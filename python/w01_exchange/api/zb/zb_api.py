
import json, hashlib,struct,time,sys
import urllib.request
from pprint import pprint
import sys
import time

import os
CURRENTURL = os.path.dirname(__file__)
class Zb_api:
	
    def __init__(self, mykey=None, mysecret=None):
        if mykey and mysecret:
            self.mykey,self.mysecret = mykey,mysecret
        else:
            filename = CURRENTURL+r'\key'
            with open(filename,'r',encoding='utf-8') as f:
                data = f.read()
            self.mykey,self.mysecret = data.split('\n')
        self.jm = ''

    def __fill(self, value, lenght, fillByte):
        if len(value) >= lenght:
            return value
        else:
            fillSize = lenght - len(value)
        return value + chr(fillByte) * fillSize

    def __doXOr(self, s, value):
        slist = list(s.decode('utf-8'))
        for index in range(len(slist)):
            slist[index] = chr(ord(slist[index]) ^ value)
        return "".join(slist)

    def __hmacSign(self, aValue, aKey):
        keyb   = struct.pack("%ds" % len(aKey), aKey.encode('utf-8'))
        value  = struct.pack("%ds" % len(aValue), aValue.encode('utf-8'))
        k_ipad = self.__doXOr(keyb, 0x36)
        k_opad = self.__doXOr(keyb, 0x5c)
        k_ipad = self.__fill(k_ipad, 64, 54)
        k_opad = self.__fill(k_opad, 64, 92)
        m = hashlib.md5()
        m.update(k_ipad.encode('utf-8'))
        m.update(value)
        dg = m.digest()
        
        m = hashlib.md5()
        m.update(k_opad.encode('utf-8'))
        subStr = dg[0:16]
        m.update(subStr)
        dg = m.hexdigest()
        return dg

    def __digest(self, aValue):
        value  = struct.pack("%ds" % len(aValue), aValue.encode('utf-8'))
        h = hashlib.sha1()
        h.update(value)
        dg = h.hexdigest()
        return dg

    def __api_call(self, path, params = ''):
        try:
            SHA_secret = self.__digest(self.mysecret)
            sign = self.__hmacSign(params, SHA_secret)
            self.jm = sign
            reqTime = (int)(time.time()*1000)
            params += '&sign=%s&reqTime=%d'%(sign, reqTime)
            url = 'https://trade.zb.cn/api/' + path + '?' + params
            req = urllib.request.Request(url)
            res = urllib.request.urlopen(req, timeout=10)
            doc = json.loads(res.read().decode('utf-8')) # .decode('gbk', 'ignore')
            return doc
        except Exception as ex:
            print(sys.stderr, 'zb request ex: ', ex)
            return None

    def __api_public_call(self,path,params=''):
        try:
            url = 'http://api.zb.cn/data/v1/' + path + '?' + params
            req = urllib.request.Request(url)
            res = urllib.request.urlopen(req, timeout=10)
            doc = json.loads(res.read().decode('utf-8')) # .decode('gbk', 'ignore')
            return doc
        except Exception as ex:
            print(sys.stderr, 'zb request public_ex: ', ex)
            return None

    def ticker(self,market):
        '''
            data = api.ticker('btc_usdt')
            http://api.zb.cn/data/v1/ticker?market=btc_usdt

            return
                {'date': '1535017230957',
                 'ticker': {'buy': '6416.6',
                            'high': '6690.39',
                            'last': '6422.33',
                            'low': '6260.48',
                            'sell': '6422.33',
                            'vol': '10808.1604'}}
        '''
        method = sys._getframe().f_code.co_name
        params = "market=%s"%market
        obj = self.__api_public_call(method, params)
        return obj

    def trades(self,market,since=0):
        '''
            data = api.trades('btc_usdt')
            # http://api.zb.cn/data/v1/trades?market=btc_usdt

            return
                [{'amount': '0.0139',
                  'date': 1535017270,
                  'price': '6417.26',
                  'tid': 175044082,
                  'trade_type': 'ask',
                  'type': 'sell'},
                 {'amount': '0.0067',
                  'date': 1535017270,
                  'price': '6417.0',
                  'tid': 175044083,
                  'trade_type': 'ask',
                  'type': 'sell'},
                 {'amount': '0.0064',
                  'date': 1535017270,
                  'price': '6411.89',
                  'tid': 175044084,
                  'trade_type': 'ask',
                  'type': 'sell'},
                  ..................
                  ]
        '''
        method = sys._getframe().f_code.co_name
        params = "market=%s&since=%s"%(market,since)
        data = self.__api_public_call(method, params)
        if data is None:
            print('trades 未接收到数据')
            time.sleep(20)
            return self.trades(market,since)
        else:
            return [(da['tid'],market,da['date'],da['price'],da['amount'],da['type']) for da in data]


    def depth(self,market):
        '''
            最多只用50的深度
            可以设置merge=0.01深度合并，但只有5档深度
            data = api.trades('btc_usdt')
            http://api.zb.cn/data/v1/depth?market=btc_usdt&size=1000

            return
                {'date': '1535017230957',
                 'ticker': {'buy': '6416.6',
                            'high': '6690.39',
                            'last': '6422.33',
                            'low': '6260.48',
                            'sell': '6422.33',
                            'vol': '10808.1604'}}
        '''
        method = sys._getframe().f_code.co_name
        params = "market=%s&size=50"%market
        obj = self.__api_public_call(method, params)
        obj = [obj['asks'][::-1],obj['bids']]
        return obj

    def markets(self):
        '''
            data = api.markets()
            # http://api.zb.cn/data/v1/markets

            return
                {'1st_btc': {'amountScale': 1, 'priceScale': 10},
                 '1st_qc': {'amountScale': 1, 'priceScale': 3},
                 '1st_usdt': {'amountScale': 1, 'priceScale': 4},
                 'aaa_qc': {'amountScale': 1, 'priceScale': 5},
                 'ada_btc': {'amountScale': 1, 'priceScale': 8},
                 'ada_qc': {'amountScale': 1, 'priceScale': 3},
                 ..............................................
                 }
        '''
        method = sys._getframe().f_code.co_name
        # params = "market=%s"%market
        obj = self.__api_public_call(method)
        return obj

    def kline(self,market,type,size=500):
        '''
            默认2.5小时线
            data = api.markets()
            http://api.zb.cn/data/v1/kline?market=btc_usdt
            
            type
                1min
                3min
                5min
                15min
                30min
                1day
                3day
                1week
                1hour
                2hour
                4hour
                6hour
                12hour
            since
                从这个时间戳之后的
            size
                返回数据的条数限制(默认为1000，如果返回数据多于1000条，那么只返回1000条)

            return
                {'data': [[1535013900000, 6430.62, 6431.48, 6419.39, 6425.41, 3.7509],
                          [1535014800000, 6426.62, 6438.72, 6419.39, 6436.2, 0.5397],
                          [1535015700000, 6421.35, 6428.27, 6394.16, 6399.06, 11.3492],
                          [1535016600000, 6395.25, 6429.64, 6395.25, 6428.43, 4.2593],
                          [1535017500000, 6416.32, 6424.05, 6399.67, 6399.67, 1.7022]],
                 'moneyType': 'USDT',
                 'symbol': 'btc'}
        '''
        method = sys._getframe().f_code.co_name
        params = "market=%s&type=%s&size=%s"%(market,type,size)
        obj = self.__api_public_call(method, params)
        # print(obj)
        return obj['data']







    # def query_account(self):
    #     try:
    #         params = "accesskey="+self.mykey+"&method=getAccountInfo"
    #         path = 'getAccountInfo'

    #         obj = self.__api_call(path, params)
    #         #print obj
    #         return obj
    #     except Exception as ex:
    #         print(sys.stderr, 'zb query_account exception,',ex)
    #         return None
            
    def getAccountInfo(self):
        '''
            data = api.getAccountInfo()
        '''
        try:
            method = sys._getframe().f_code.co_name
            params = "accesskey="+self.mykey+"&method="+method
            obj = self.__api_call(method, params)
            #print obj
            return obj
        except Exception as ex:
            print(sys.stderr, 'zb %s exception ,'%method,ex)
            return None
    


    def order(self,currency,price,amount,tradeType):
        '''
            data = api.order(9.2,'bts_usdt','0.053',1)
            
            https://trade.zb.cn/api/order?accesskey=youraccesskey&amount=1.502
            &currency=qtum_usdt&method=order&price=1.9001&tradeType=1
                &sign=请求加密签名串&reqTime=当前时间毫秒数

            return
                {'id': '2018082368732567', 'message': '操作成功', 'code': 1000}
        '''
        if tradeType == 'buy':
            tradeType = 1
        elif tradeType == 'sell':
            tradeType = 0
        try:
            method = sys._getframe().f_code.co_name
            params = "accesskey="+self.mykey+"&amount=%s&currency=%s&method=%s&price=%s&tradeType=%s"% \
            (amount,currency,method,price,tradeType)
            obj = self.__api_call(method, params)
            obj = obj['id']
            return obj
        except Exception as ex:
            print(sys.stderr, 'zb %s exception ,'%method,ex)
            return None

    def cancelOrder(self,id,currency):
        '''
            data = api.cancelOrder('bts_usdt','2018082368722076')
            
            https://trade.zb.cn/api/cancelOrder?accesskey=youraccesskey
            &currency=ltc_btc&id=201710111625&method=cancelOrder
                &sign=请求加密签名串&reqTime=当前时间毫秒数

            return
                {'message': '操作成功', 'code': 1000}
                {'message': '挂单没有找到', 'code': 3001}
                {'code': 1001, 'message': 'Error order id'}
        '''
        try:
            method = sys._getframe().f_code.co_name
            params = "accesskey="+self.mykey+"&currency=%s&id=%s&method=%s"% \
            (currency,id,method)
            obj = self.__api_call(method, params)
            print(obj)
            return obj['code']
        except Exception as ex:
            print(sys.stderr, 'zb %s exception ,'%method,ex)
            return None

    def getOrders(self,currency,pageIndex,tradeType):
        '''
            data = api.getOrders('bts_usdt',pageIndex=1,tradeType=1)
            超过10个订单需要翻页
            

            return
                [{'currency': 'bts_usdt', 'type': 1, 'trade_money': '0.00000', 'price': 0.0538, 'status': 3, 'total_amount': 9.2, 
                'fees': 0, 'id': '2018082368722076', 'trade_date': 1535008298044, 'trade_amount': 0.0}]
        '''
        try:
            method = sys._getframe().f_code.co_name
            params = "accesskey="+self.mykey+"&currency=%s&method=%s&pageIndex=%s&tradeType=%s"% \
            (currency,method,pageIndex,tradeType)
            obj = self.__api_call(method, params)
            #print obj
            return obj
        except Exception as ex:
            print(sys.stderr, 'zb %s exception ,'%method,ex)
            return None


    def getOrdersNew(self,currency,pageIndex,tradeType):
        '''
            data = api.getOrdersNew('bts_usdt',pageIndex=1,tradeType=1)
            超过100个订单需要翻页
            
            https://trade.zb.cn/api/getOrdersNew?accesskey=youraccesskey
            &currency=ltc_btc&method=getOrdersNew&pageIndex=1&pageSize=1&tradeType=1
                &sign=请求加密签名串&reqTime=当前时间毫秒数
            
            return
                [{'currency': 'bts_usdt', 'type': 1, 'trade_money': '0.00000', 'price': 0.0538, 'status': 3, 'total_amount': 9.2, 
                'fees': 0, 'id': '2018082368722076', 'trade_date': 1535008298044, 'trade_amount': 0.0}]
        '''
        try:
            method = sys._getframe().f_code.co_name
            params = "accesskey="+self.mykey+"&currency=%s&method=%s&pageIndex=%s&pageSize=100&tradeType=%s"% \
            (currency,method,pageIndex,tradeType)
            obj = self.__api_call(method, params)
            #print obj
            return obj
        except Exception as ex:
            print(sys.stderr, 'zb %s exception ,'%method,ex)
            return None


    def unfinished_orders_list(self,currency,pageIndex=1):
        '''
            data = api.getUnfinishedOrdersIgnoreTradeType('bts_usdt',pageIndex=1)
            超过100个订单需要翻页
            
            GET https://trade.zb.cn/api/getUnfinishedOrdersIgnoreTradeType?accesskey=youraccesskey
            &currency=ltc_btc&method=getUnfinishedOrdersIgnoreTradeType&pageIndex=1&pageSize=10
                &sign=请求加密签名串&reqTime=当前时间毫秒数
            
            return
                [{'currency': 'bts_usdt', 'type': 1, 'trade_money': '0.00000', 'price': 0.0538, 'status': 3, 'total_amount': 9.2, 
                'fees': 0, 'id': '2018082368722076', 'trade_date': 1535008298044, 'trade_amount': 0.0}]
        '''
        try:
            method = 'getUnfinishedOrdersIgnoreTradeType'
            params = "accesskey="+self.mykey+"&currency=%s&method=%s&pageIndex=%s&pageSize=10"% \
            (currency,method,pageIndex)
            obj = self.__api_call(method, params)
            #print obj
            return obj
        except Exception as ex:
            raise ex
            print(sys.stderr, 'zb %s exception ,'%method,ex)
            return None

    def getOrder(self,id,currency):
        '''
            data = api.getOrder('bts_usdt','2018082368722076')
            
            return
                {'status': 3, 'trade_money': '0.00000', 'total_amount': 9.2, 'price': 0.0538, 'currency': 'bts_usdt', 
                'type': 1, 'id': '2018082368722076', 'trade_amount': 0.0, 'trade_date': 1535008298044}
        '''
        try:
            method = sys._getframe().f_code.co_name
            params = "accesskey="+self.mykey+"&currency=%s&id=%s&method=%s"% (currency,id,method)
            obj = self.__api_call(method, params)
            #print obj
            return obj
        except Exception as ex:
            print(sys.stderr, 'zb %s exception ,'%method,ex)
            return None


    def getUserAddress(self,currency):
        '''
            获取用户充值地址
            data = api.getUserAddress('btc')
            
            https://trade.zb.cn/api/getUserAddress?accesskey=youraccesskey
            &currency=btc&method=getUserAddress
                &sign=请求加密签名串&reqTime=当前时间毫秒数

            return
                {'message': {'des': 'success', 'isSuc': True, 'datas': {'key': 'zbbts001_741580511583015302'}}, 'code': 1000}
        '''
        try:
            method = sys._getframe().f_code.co_name
            params = "accesskey="+self.mykey+"&currency=%s&method=%s"% (currency,method)
            obj = self.__api_call(method, params)
            #print obj
            return obj
        except Exception as ex:
            print(sys.stderr, 'zb %s exception ,'%method,ex)
            return None


    def getWithdrawAddress(self,currency):
        '''
            获取用户认证的提现地址
            data = api.getWithdrawAddress('btc')
            
            https://trade.zb.cn/api/getWithdrawAddress?accesskey=youraccesskey
            &currency=btc&method=getWithdrawAddress
                &sign=请求加密签名串&reqTime=当前时间毫秒数

            return
                {'message': {'des': 'success', 'isSuc': True, 'datas': {'key': 'zbbts001_741580511583015302'}}, 'code': 1000}
        '''
        try:
            method = sys._getframe().f_code.co_name
            params = "accesskey="+self.mykey+"&currency=%s&method=%s"% (currency,method)
            obj = self.__api_call(method, params)
            #print obj
            return obj
        except Exception as ex:
            print(sys.stderr, 'zb %s exception ,'%method,ex)
            return None



    def getWithdrawRecord(self,currency,pageIndex):
        '''
            获取数字资产充值记录
            data = api.getWithdrawRecord('bts',pageIndex=1)
            
            https://trade.zb.cn/api/getWithdrawRecord?accesskey=youraccesskey
            &currency=eth&method=getWithdrawRecord&pageIndex=1&pageSize=10
                &sign=请求加密签名串&reqTime=当前时间毫秒数
            
            return
                {'code': 1000,
                 'message': {'datas': {'list': [{'amount': 0.80352,
                                                 'fees': 3.0,
                                                 'id': 2018032623719,
                                                 'manageTime': 1522057180000,
                                                 'status': 2,
                                                 'submitTime': 1522053979000,
                                                 'toAddress': 'missing64006_my'}],
                                       'pageIndex': 1,
                                       'pageSize': 10,
                                       'totalCount': 1,
                                       'totalPage': 1},
                             'des': 'success',
                             'isSuc': True}}
        '''
        try:
            method = sys._getframe().f_code.co_name
            params = "accesskey="+self.mykey+"&currency=%s&method=%s&pageIndex=%s&pageSize=10"% \
            (currency,method,pageIndex)
            obj = self.__api_call(method, params)
            #print obj
            return obj
        except Exception as ex:
            print(sys.stderr, 'zb %s exception ,'%method,ex)
            return None

    def getChargeRecord(self,currency,pageIndex):
        '''
            data = api.getChargeRecord('bts',pageIndex=1)
            超过100个订单需要翻页
            
            https://trade.zb.cn/api/getChargeRecord?accesskey=youraccesskey
            &currency=btc&method=getChargeRecord&pageIndex=1&pageSize=10
                &sign=请求加密签名串&reqTime=当前时间毫秒数
            
            return
                {'code': 1000,
                 'message': {'datas': {'list': [{'address': 'zbbts_691775530831319606',
                                                 'amount': '2.00000000',
                                                 'confirmTimes': 40,
                                                 'currency': 'BTS',
                                                 'description': '确认成功',
                                                 'hash': '8587e378f166f750383096a96ea405170beb4ffb',
                                                 'id': 71837,
                                                 'itransfer': 0,
                                                 'status': 2,
                                                 'submit_time': '2018-02-05 23:58:47'},],
                                       'pageIndex': 1,
                                       'pageSize': 10,
                                       'total': 4},
                             'des': 'success',
                             'isSuc': True}}
        '''
        try:
            method = sys._getframe().f_code.co_name
            params = "accesskey="+self.mykey+"&currency=%s&method=%s&pageIndex=%s&pageSize=10"% \
            (currency,method,pageIndex)
            obj = self.__api_call(method, params)
            #print obj
            return obj
        except Exception as ex:
            print(sys.stderr, 'zb %s exception ,'%method,ex)
            return None

    def withdraw(self):
        pass

if __name__ == '__main__':



    api = zb_api()
    # data = api.order(9.2,'bts_usdt','0.053',1)
    # data = api.getOrdersNew('bts_usdt',pageIndex=1,tradeType=1)
    # data = api.getOrders('bts_usdt',pageIndex=1,tradeType=1)
    # data = api.getOrder('bts_usdt','2018082368722076')
    # data = api.cancelOrder('bts_usdt','2018082368722076')
    # data = api.getUnfinishedOrdersIgnoreTradeType('bts_usdt',pageIndex=1)
    # data = api.getUserAddress('btc')
    # data = api.getWithdrawAddress('bts')
    # data = api.getWithdrawRecord('bts',pageIndex=1)
    # data = api.getChargeRecord('bts',pageIndex=1)
    # data = api.ticker('btc_usdt')
    # data = api.markets()
    # data = api.trades('btc_usdt')
    # data = api.depth('btc_usdt')
    data = api.kline('btc_usdt')




    filename = 'read.txt'
    pprint(data)
    with open(filename,'w',encoding='utf-8') as f:
        f.write(str(data))
