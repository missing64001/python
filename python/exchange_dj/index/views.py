from django.shortcuts import render
from .api.api import Trade


# Create your views here.
def parent_views(request):

    
    return render(request, '01_parent.html')


def child_views(request):
    return render(request, '02_child.html')

def depth_views(request,symbol):
    exchange = 'hb'
    api = Trade(exchange)
    asks,bids = api.depth(symbol)
    asks = asks[::-1]
    title = exchange+' '+symbol


    # asks = [[1,2],[3,4]]
    # bids = [[1,2],[3,4]]
    return render(request, 'depth.html',locals())