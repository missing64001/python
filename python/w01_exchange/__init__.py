
import sys
import os
CURRENTURL = os.path.dirname(__file__)


paths = [r'F:\my',]
for path in paths:
    if os.path.exists(path):
        sys.path.insert(1,path)
        break
else:
    raise ValueError('not find my model in ',paths)

from F00_myfn.h08_deal_except import deal_e



def des(fun,args):
    def inn():
        fun(args)
    return inn

deal_e = des(deal_e,CURRENTURL)