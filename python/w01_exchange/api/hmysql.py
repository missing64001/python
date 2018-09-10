import sys 
import os
import os
sys.path.insert(1,os.path.abspath(os.path.dirname(__file__)+'\\..'))
from __init__ import Mysql

from pprint import pprint
import time,datetime

def main():

    global MYSQL
    global EXCHANGE
    EXCHANGE = 'ok'
    MYSQL = Mysql('localhost','w01_exchange','w01_exchange',db='w01_exchange')



    # trades: exchange symbol id date,price,amount,famount,type,fee,fee_symbol,isapi

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


    famount int default 0,
    famount_p tinyint default 0,
    fee int default 0,
    fee_p tinyint default 0,
    fee_symbol varchar(10) default null,
    type tinyint not null, -- 1 buy 2 sell
    isapi tinyint default 1
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



