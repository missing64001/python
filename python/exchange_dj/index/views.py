from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .api.api import Trade,EXCHANGES
from threading import Thread
import time

# Create your views here.
def parent_views(request):
    return render(request, '01_parent.html')


def child_views(request):
    return render(request, '02_child.html')


def market_views(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/')
    symbol = request.GET['symbol']
    return HttpResponseRedirect('/depth/'+symbol)

def depth_views(request,symbol='btc_usdt'):
    '''
        data:
            title:{trades:[price,amout,date,color,type],asks:[price,amout],bids:[price,amout]}

    '''
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/')


    symbols = request.COOKIES.get('symbols',None)
    if symbols:
        symbol_lst = symbols.split(',')
        if symbol in symbol_lst:
            symbol_lst.remove(symbol)
        symbol_lst.insert(0,symbol)
    else:
        symbol_lst = [symbol,'ltc_usdt','bts_usdt','eos_usdt']

    symbol_lst_show = symbol_lst[1:8]




    data = {}

    threads = []

    for exchange in EXCHANGES:
        title = exchange+' '+symbol
        data[title] = {}

        th = Thread(target=get_data,args=(exchange,data,symbol))
        th.start()
        threads.append(th)

        th = Thread(target=get_trades,args=(exchange,data,symbol))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    # asks = [[1,2],[3,4]]
    # bids = [[1,2],[3,4]]

    dis = {'symbol_lst_show':symbol_lst_show,'data':data}
    res = render(request, 'depth.html',dis)
    res.set_cookie('symbols',','.join(symbol_lst))
    return res

def get_data(exchange,resdata,symbol):
    api = Trade(exchange)
    data = api.depth(symbol)
    if not data:
        return
    asks,bids = data
    asks = asks[::-1]
    title = exchange+' '+symbol
    resdata[title].update({'asks':asks,'bids':bids})

def get_trades(exchange,resdata,symbol):
    api = Trade(exchange)
    trades = api.trades(symbol)
    if not trades:
        return
    title = exchange+' '+symbol
    trades = [ (trade[3],trade[4],time.strftime("%H:%M:%S", time.localtime(trade[2])),
              '#ae4e54' if trade[5]=='sell' else '#589065' , trade[5]    )    for trade in trades]
    resdata[title].update({'trades':trades})
    # 