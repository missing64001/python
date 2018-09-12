import sys 
import os
# sys.path.insert(1,os.path.abspath(os.path.dirname(__file__)+'\\..'))
# from __init__ import Mysql

from pprint import pprint
import time,datetime

def main():


    global MYSQL
    global EXCHANGE
    EXCHANGE = 'ok'
    MYSQL = Mysql('localhost','w01_exchange','w01_exchange',db='w01_exchange')
    # trades: exchange symbol id date,price,amount,famount,type,fee,fee_symbol,isapi


    dic = {
        'exchange':'ok',
        'symbol':'btc_usdt',
        'id':3333,
        'date':1111111,
        'price':12424.345,
        'amount':324.34,
        'type':'sell',
    }
    save_order_info(dic)
    return 





    trades_sql_s="""
    -- drop table if exists trades;
    create table if not exists trades(
    exchange tinyint not null, -- 1 ok 2 zb 3 hb
    symbol varchar(20) not null,
    id bigint not null,
    date int not null,
    price int not null,
    price_p tinyint not null,
    amount int not null,
    amount_p tinyint not null,
    type tinyint not null, -- 1 buy 2 sell


    famount int default 0,
    famount_p tinyint default 0,
    fee int default 0,
    fee_p tinyint default 0,
    fee_symbol varchar(10) default null,
    isapi tinyint default 1,
    isfinished tinyint default 0
    );
    ALTER TABLE trades
    ADD UNIQUE KEY(exchange,symbol,id);
    """

    # charge_and_withdraw: exchange symbol id date amount 

    charge_and_withdraw_sql_s="""
    -- drop table if exists charge_and_withdraw;
    create table if not exists charge_and_withdraw(
    exchange tinyint not null, -- 1 ok 2 zb 3 hb
    symbol varchar(20) not null,
    id bigint not null,
    date int not null,
    amount int not null,
    amount_p tinyint not null,
    isalive tinyint default 1
    );
    ALTER TABLE trades
    ADD UNIQUE KEY(exchange,symbol,id);
    """
    
    mysql_exec_sqls = [trades_sql_s,charge_and_withdraw_sql_s]
    for sql_s in mysql_exec_sqls:
        MYSQL.exec(sql_s)
TYPE_T = {
    'buy':1,1:'buy',
    'sell':2,2:'sell'
}

EXCHANGE_T = {
    'ok':1,1:'ok',
    'zb':2,2:'zb',
    'hb':3,3:'hb',
}




def save_order_info(dic):  
    # exchange  symbol  id  date  price  price_p  amount  amount_p  type
    dic['price'],dic['price_p'] = split_precision(dic['price'])
    dic['amount'],dic['amount_p'] = split_precision(dic['amount'])
    dic['exchange'] = EXCHANGE_T[dic['exchange']]
    dic['type'] = TYPE_T[dic['type']]

    fields = []
    values = []
    [fields.append(f) or values.append(dic[f])  for f in dic]
    fields = str(tuple(fields)).replace("'",' ')
    values = str(tuple(values))

    print(fields,values)
    sql_s = 'INSERT INTO trades%s values%s' % (fields,values)

    try:
        MYSQL.exec(sql_s)
    except Exception as e:
        if 'Duplicate' in str(e):
            print(exchange,symbol,id,'Duplicate')
        else:
            raise e


def split_precision(f):
    f = str(f)
    if 'e' in f:
        flst=f.split('e-')
        f = flst[0]
        extra_precision = int(flst[1])
    else:
        extra_precision = 0

    flst = f.split('.')
    if len(flst)==1:
        precision = 0
    else:
        precision = len(flst[1])
    amount = ''.join(flst).lstrip('0')
    if len(amount) - 8 >0:
        extra_precision -= len(amount) - 8

    length_zero = len(amount)-len(amount.lstrip('0'))
    amount = amount[:8+length_zero]
    return int(amount),-(precision+extra_precision+length_zero)

def join_precision(amount,precision):
    return amount * 10 ** (precision)


if __name__ == '__main__':
    main()
else:
    MYSQL = Mysql('localhost','w01_exchange','w01_exchange',db='w01_exchange')
'''
create user "w01_exchange"@"%" identified by "w01_exchange";
grant all privileges on w01_exchange.* to 'w01_exchange'@'%' with grant option;
create database w01_exchange;
'''

'''
select 
table_schema as '数据库',
table_name as '表名',
table_rows as '记录数',
truncate(data_length/1024/1024, 2) as '数据容量(MB)',
truncate(index_length/1024/1024, 2) as '索引容量(MB)'
from information_schema.tables
where table_schema='w01_exchange'
order by data_length desc, index_length desc;
'''


'''
select datetime,num,type,totle,volume,totle/volume as average_price
from 

(select 
CAST(date/100 AS signed) as datetime,
count(tid) as num,
type,
sum(price*power(10,-price_precision)*amount*power(10,-amount_precision)) as totle,
sum(amount*power(10,-amount_precision)) as volume
from zb_histroy where symbol = "btc_usdt"  
group by CAST(date/100 AS signed),type 
order by CAST(date/100 AS signed),type) t
;
'''



