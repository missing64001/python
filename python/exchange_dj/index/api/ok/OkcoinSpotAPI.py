#!/usr/bin/python
# -*- coding: utf-8 -*-
#用于访问OKCOIN 现货REST API
from HttpMD5Util import buildMySign,httpGet,httpPost

class OKCoinSpot:

    def __init__(self,url,apikey,secretkey):
        self.__url = url
        self.__apikey = apikey
        self.__secretkey = secretkey

    #获取OKCOIN现货行情信息
    def ticker(self,symbol = ''):
        TICKER_RESOURCE = "/api/v1/ticker.do"
        params=''
        if symbol:
            params = 'symbol=%(symbol)s' %{'symbol':symbol}
        return httpGet(self.__url,TICKER_RESOURCE,params)

    #获取OKCOIN现货市场深度信息
    def depth(self,symbol = ''):
        DEPTH_RESOURCE = "/api/v1/depth.do"
        params=''
        if symbol:
            params = 'symbol=%(symbol)s' %{'symbol':symbol}
        return httpGet(self.__url,DEPTH_RESOURCE,params) 

    #获取OKCOIN现货历史交易信息
    #

    def trades(self,symbol = '',since=0):
        TRADES_RESOURCE = "/api/v1/trades.do"
        params=''
        if symbol:
            params = 'symbol=%(symbol)s&since=%(since)s' %{'symbol':symbol,'since':since}
        return httpGet(self.__url,TRADES_RESOURCE,params)
    
    #获取用户现货账户信息
    def userinfo(self):
        USERINFO_RESOURCE = "/api/v1/userinfo.do"
        params ={}
        params['api_key'] = self.__apikey
        params['sign'] = buildMySign(params,self.__secretkey)
        return httpPost(self.__url,USERINFO_RESOURCE,params)

    #现货交易
    def trade(self,symbol,price,amount,tradeType):
        '''
            return '{"error_code":1007}' 没有交易对
            return '{"error_code":1002}' 数量不够
            {"result":true,"order_id":864345207}
        '''


        TRADE_RESOURCE = "/api/v1/trade.do"
        params = {
            'api_key':self.__apikey,
            'symbol':symbol,
            'type':tradeType
        }
        if price:
            params['price'] = price
        if amount:
            params['amount'] = amount
            
        params['sign'] = buildMySign(params,self.__secretkey)
        return httpPost(self.__url,TRADE_RESOURCE,params)

    #现货批量下单
    def batchTrade(self,symbol,tradeType,orders_data):
        BATCH_TRADE_RESOURCE = "/api/v1/batch_trade.do"
        params = {
            'api_key':self.__apikey,
            'symbol':symbol,
            'type':tradeType,
            'orders_data':orders_data
        }
        params['sign'] = buildMySign(params,self.__secretkey)
        return httpPost(self.__url,BATCH_TRADE_RESOURCE,params)

    #现货取消订单
    def cancelOrder(self,symbol,orderId):
        CANCEL_ORDER_RESOURCE = "/api/v1/cancel_order.do"
        params = {
             'api_key':self.__apikey,
             'symbol':symbol,
             'order_id':orderId
        }
        params['sign'] = buildMySign(params,self.__secretkey)
        return httpPost(self.__url,CANCEL_ORDER_RESOURCE,params)

    #现货订单信息查询
    def orderinfo(self,symbol,orderId):
        ORDER_INFO_RESOURCE = "/api/v1/order_info.do"
        params = {
             'api_key':self.__apikey,
             'symbol':symbol,
             'order_id':orderId
        }
        params['sign'] = buildMySign(params,self.__secretkey)
        return httpPost(self.__url,ORDER_INFO_RESOURCE,params)

    #现货批量订单信息查询
    def ordersinfo(self,symbol,orderId='',tradeType=0):
        '''
            |api_key|String|是|用户申请的apiKey|
            |type|Integer|是|查询类型 0:未完成的订单 1:已经完成的订单|
            |symbol|String|是|币对如ltc_btc|
            |order_id|String|是|订单ID(多个订单ID中间以","分隔,一次最多允许查询50个订单)|
            |sign|String|是|请求参数的签名|
        '''
        ORDERS_INFO_RESOURCE = "/api/v1/orders_info.do"
        params = {
             'api_key':self.__apikey,
             'symbol':symbol,
             'order_id':orderId,
             'type':tradeType
        }
        params['sign'] = buildMySign(params,self.__secretkey)
        return httpPost(self.__url,ORDERS_INFO_RESOURCE,params)

    #现货获得历史订单信息
    def orderHistory(self,symbol,status=0,currentPage=1,pageLength=200):
        ORDER_HISTORY_RESOURCE = "/api/v1/order_history.do"
        params = {
           'api_key':self.__apikey,
           'symbol':symbol,
           'status':status,
           'current_page':currentPage,
           'page_length':pageLength
        }
        params['sign'] = buildMySign(params,self.__secretkey)
        return httpPost(self.__url,ORDER_HISTORY_RESOURCE,params)















    
