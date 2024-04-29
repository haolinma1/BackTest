import numpy as np
from numba import float64, int64, int8, boolean
from numba.experimental import jitclass
from numba.typed import Dict, List
from numba.types import DictType, ListType, Tuple

BUY = 1
SELL = -1

NONE = 0
NEW = 1
EXPIRED = 2
FILLED = 3
CANCELED = 4
PARTIALLY_FILLED = 5
MODIFY = 6
REJECTED = 7

GTC = 0  # Good 'till cancel
GTX = 1  # Post only
FOK = 2  # Fill or kill
IOC = 3  # Immediate or cancel



@jitclass
class Order:
    order_id: int64
    qty:float64
    side: int8
    local_timestamp:int64
    exchange_timestamp:int64
    tick_price:float64
    tick_size:float64
    order_type:int8
    time_in_force:int8
    status:int8
    marker:boolean
    executed_size:float64
    executed_tick_price:float64
    def __init__(self,qty, order_id, side, tick_price, tick_size, order_type,marker=False,time_in_force=GTC):
        self.order_id = order_id
        self.qty = qty
        self.side = side
        self.local_timestamp = 0
        self.exchange_timestamp = 0
        self.tick_price = tick_price
        self.tick_size = tick_size
        self.order_type = order_type
        self.time_in_force = time_in_force
        self.status = NEW
        self.marker = marker
        self.executed_size = None
        self.executed_tick_price=None   

    @property
    def marker(self):
        return self.marker

    @property
    def order_id(self):
        return self.order_id     

    @property
    def price(self):
        return self.tick_price*self.tick_size
    
    @property
    def qty(self):
        return self.qty
    
    @property
    def executed_price(self):
        if self.executed_tick_price is None:
            raise ValueError("Order not executed")
        return self.executed_tick_price*self.tick_size
    
order_ty = Order.class_type.instance_type
order_tup_ty = Tuple((order_ty, int64))

@jitclass
class OrderBus:
    order_list: ListType(order_tup_ty)
    orders: DictType(int64, int64)
    frontmost_timestamp: int64
    def __init__(self):
        self.orderList=List.empty_list(order_tup_ty)
        self.orders=Dict.empty(int64, int64)
        self.frontmost_timestamp=0
    
    def append(self,order,timestamp):
        timestamp=int(timestamp)
        if len(self.order_list)>0:
            _,last_timestamp=self.order_list[-1]
            if timestamp<last_timestamp:
                timestamp=last_timestamp
        
        self.order_list.append((order,timestamp))

        if order.order_id in self.orders:
            self.orders[order.order_id]+=1
        else:
            self.orders[order.order_id]=1

        if self.frontmost_timestamp<=timestamp:
            self.frontmost_timestamp=timestamp 
    
    def get_timestamp(self,order_id):
        for order,timestamp in self.order_list:
            if order.order_id==order_id:
                return timestamp
        raise ValueError("Order not found")
    
    def delate_order(self,key):
        order,_=self.order_list[key]
        del self.orders[key]
        self.orders[order.order_id]-=1
        if self.orders[order.order_id]==0:
            del self.orders[order.order_id]
      
    def __getitem__(self,key):
        if self.order_list:
            return self.order_list[key]
        else:
            return None
    
    def __getlen__(self):
        return len(self.order_list)

    def __contains__(self,order_id):
        return order_id in self.orders
    
    

    

    
