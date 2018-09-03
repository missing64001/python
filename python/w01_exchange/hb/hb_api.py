# 有效期 90天
import os
from HuobiServices import *
CURRENTURL = os.path.dirname(__file__)
from pprint import pprint







def main():
    print(CURRENTURL)
    filename = CURRENTURL+r'\key'
    with open(filename,'r',encoding='utf-8') as f:
        data = f.readlines()
    data = [ da.strip() for da in data]
    set_key(*data)
    # data = get_symbols()
    # pprint(data)
    data = get_balance()
    data = data['data']['list']
    for da in data:
        if da['balance'] != '0':
            print(da['balance'])
        else:
            print('1',end='')



if __name__ == '__main__':
    main()