from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .api.api import Trade,EXCHANGES
from threading import Thread
import time
import json

TIMES = 0        # run times
Th = None        # is run threading
SYMBOLS = {}      # the market name for threading
SLEEP_TIME = 3   # the sleep time for threading
DATA = {}



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

def ajax_get_views(request,symbol):
    if not request.user.is_authenticated:
        return 
    date = int(time.time())
    SYMBOLS[symbol] = date
    # for title in DATA.copy():
    #     exchange,symbol,type = title.split()
    #     if symbol != SYMBOL:
    #         del DATA[title]
    
    for sym in SYMBOLS.copy():
        if date-10 > SYMBOLS[sym]:
            del SYMBOLS[sym]

    data = {}
    for da in DATA.copy():
        if da.split()[1] not in SYMBOLS:
            del DATA[da]
        elif da.split()[1] == symbol:
            data[da] = DATA[da]


     # time.strftime("%H:%M:%S", time.localtime())
    res =  HttpResponse(json.dumps({'date':date,'data':data}), content_type="application/json")
    # print(len(DATA))
    # DATA = {}
    return res

def depth_views(request,symbol='btc_usdt'):
    global Th
    if not Th:
        th = Thread(target=while_run)
        th.start()
        
        Th = th

    global SYMBOL
    SYMBOL = symbol
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

    # threads = []

    for exchange in EXCHANGES:
        title = exchange+'_'+symbol
        data[title] = {}

    #     th = Thread(target=get_openorder,args=(exchange,data,symbol))
    #     th.start()
    #     threads.append(th)

    #     th = Thread(target=get_trades,args=(exchange,data,symbol))
    #     th.start()
    #     threads.append(th)

    # for th in threads:
    #     th.join()

    # asks = [[1,2],[3,4]]
    # bids = [[1,2],[3,4]]

    dis = {'symbol_lst_show':symbol_lst_show,'data':data}
    res = render(request, 'depth.html',dis)
    res.set_cookie('symbols',','.join(symbol_lst))
    return res

def get_openorder(exchange,symbol):
    api = Trade(exchange)
    data = api.depth(symbol)
    if not data:
        return
    asks,bids = data
    asks = asks[::-1]
    title = exchange+' '+symbol
    # resdata[title].update({'asks':asks,'bids':bids})
    DATA.update({exchange+' '+symbol+' asks':asks,
                 exchange+' '+symbol+' bids':bids,
        })

def get_trades(exchange,symbol):
    api = Trade(exchange)
    trades = api.trades(symbol)
    if not trades:
        return
    title = exchange+' '+symbol
    trades = [ (trade[3],trade[4],time.strftime("%H:%M:%S", time.localtime(trade[2])),
              '#ae4e54' if trade[5]=='sell' else '#589065' , trade[5]    )    for trade in trades]
    DATA.update({exchange+' '+symbol+' trades':trades})
    #

def while_run():
    global TIMES
    while True:
        TIMES += 1
        
        print('----------SYMBOLS----------')
        print(len(SYMBOLS),len(DATA))
        for symbol in SYMBOLS.copy():
            time.sleep(SLEEP_TIME)
            for exchange in EXCHANGES:
                data={}
                th = Thread(target=get_trades,args=(exchange,symbol))
                th.start()
                get_the_threading_num(th)
                th = Thread(target=get_openorder,args=(exchange,symbol))
                th.start()
                th_len = get_the_threading_num(th)
        # print('the %sth run, sum of the ths is %s'%(TIMES,th_len),end='\r')
        # print(DATA.keys())


def get_the_threading_num(th,ths=[]):
    for t in ths.copy():
        if not t.is_alive():
            ths.remove(t) 
    ths.append(th)
    return len(ths)
    