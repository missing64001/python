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

def set_key():
    filename = CURRENTURL+r'\key'
    with open(filename,'r',encoding='utf-8') as f:
        data = f.readlines()
    data = [ da.strip() for da in data]
    set_key(*data)

class Hb_api():
    def __init__(self):
        set_key()


if __name__ == '__main__':
    main()