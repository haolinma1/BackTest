from numba import float64, int64
from numba.experimental import jitclass
from numba.types import DictType
from numba.typed import Dict
import numpy as np
import os
@jitclass
class SnapShot():
    local_timestamp:int64
    asks_dict:DictType(float64, float64)
    bids_dict:DictType(float64, float64)
    exchange_timestamp:int64

    def __init__(self,local_timestamp,exchange_timestamp ):
        self.local_timestamp = local_timestamp
        self.asks_dict = Dict.empty(float64, float64)
        self.bids_dict = Dict.empty(float64, float64)
        self.exchange_timestamp = exchange_timestamp

    def load_asks(self,asks):
        """
        ask is a list like [6.32685e+04 3.00000e-03 6.32688e+04 2.00000e+00 6.32689e+04 3.73200e+00
                    6.32690e+04 3.03200e+00 6.32696e+04 3.05000e+00] that is a books5 order book asks
        Args:
            asks (list):
        """        
        i=0
        while i< len(asks):
            self.asks_dict[asks[i]]=asks[i+1]
            i+=2
    
    def load_bids(self,bids):
        i=0
        while i< len(bids):
            self.bids_dict[bids[i]]=bids[i+1]
            i+=2

snapshot_ty=SnapShot.class_type.instance_type
@jitclass
class Cache():
    data:ListType(snapshot_ty)
    def __init__(self):
        self.data=List.empty_list(snapshot_ty)
    
    def load(self,file_path):
        """
        load the data from the npz file, we got four arrays,
        asks_list_array, bids_list_array, local_timestamp, exchange_timestamp

        Args:
            file_path (string): the path to the npz file
        """
        data=np.load(file_path)
        local_timestamp=data['local_timestamp']
        exchange_timestamp=data['exchange_timestamp']
        num_rows=len(local_timestamp)
        orderbook_depth=int(file_path.split('.')[-2][-1])

        for i in range(num_rows):
            snapshot=SnapShot(local_timestamp[i],exchange_timestamp[i])
            self.data.append(snapshot)

        i=0
        while i<len(data['asks_list_array']):
            asks_list=data['asks_list_array'][i:i+orderbook_depth*2]
            bids_list=data['bids_list_array'][i:i+orderbook_depth*2]
            self.data[i/10].load_asks(asks_list)
            self.data[i/10].load_bids(bids_list)
            i+=orderbook_depth*2

@jitclass
class DataReadr():
    """
    we have two class for this module, one the data reader and one is the cache, we will have a cache in the data reader,
    and when we load one file data, we store the data into the cache and run it, after we finish running this file, we need 
    to clear the cache and load the next file.
    """
    pass
    