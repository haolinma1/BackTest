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
    side: int8
    tick_price:float64
    tick_size:float64
    order_type:int8
    time_in_force:int8
    qty:float64
    def __init__(self,qty, order_id, side, tick_price, tick_size, order_type,time_in_force=GTC):
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
    
    @property
    def limit(self):
        # compatibility <= 1.3
        return self.maker
    
    @property
    def price(self):
        return self.tick_price*self.tick_size
    
    @property
    def qty(self):
        return self._qty
    
class limit_order(Order):
    pass

class market_order(Order):
    pass



    def __repr__(self):
        return f"Order({self.order_id}, {self.symbol}, {self.side}, {self.price}, {self.qty}, {self.time})"