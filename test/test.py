
import numpy as np
import dotenv
import os
import numpy as np
from numba import float64, int64, int8, boolean
from numba.experimental import jitclass
from numba.typed import Dict, List
from numba.types import DictType, ListType, Tuple
dotenv.load_dotenv()
# data_path is the folder path to store the data


@jitclass
class Test:
    side:int64
    def __init__(self):
        self.side=1

order_ty = Test.class_type.instance_type
order_tup_ty = Tuple((order_ty, int64))
@jitclass
class Order:
    orderlist:ListType(order_tup_ty)
    def __init__(self) -> None:
        self.orderlist=List.empty_list(order_tup_ty)
    
    def getOrderList(self):
        return self.orderlist
    
    def append(self,test_instance,value):
        self.orderlist.append((test_instance, value))
    def __getitem__(self,key):
        if self.orderlist:
            return self.orderlist[key]
        else:
            return None

class Ask:
    def __init__(self):
        self.order_dict={}
    
    def load(self,asks_list):
        i=0
        while i< len(asks_list):
            self.order_dict[asks_list[i]]=asks_list[i+1]
            i+=2

def main():
    file_path = 'C:/Users/haolin/Desktop/backtest/data/example/BTCUSDT_20240427_books5.npz'
    data=np.load(file_path)
    # while i< len(test_list):
    #     asks_dict[test_list[i]]=test_list[i+1]
    #     i+=2 
        
    # print(asks_dict)
    # print(data['asks_list_array'])
    orderbook_depth=int(file_path.split('.')[-2][-1])
    snapshot=[]
    num_rows=len(data['local_timestamp'])


    i=0
    while i<len(data['asks_list_array']):
        asks_list=data['asks_list_array'][i:i+orderbook_depth*2]
        ask=Ask()
        ask.load(asks_list)
        snapshot.append(ask)
        print(i/10)        
        i+=orderbook_depth*2
    


    
        
    

if __name__ == '__main__':
    main()