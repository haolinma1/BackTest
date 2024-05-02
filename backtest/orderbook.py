from numba import float64, int64
import numba
from numba.experimental import jitclass
from numba.types import DictType, unicode_type, ListType
from numba.typed import Dict, List
import numpy as np
import os
import re



class SnapShot():
    def __init__(self, exchange_timestamp):
        self.asks_dict = {}
        self.bids_dict = {}
        self.exchange_timestamp = exchange_timestamp

    def load_asks(self, asks):
        """
        ask is a list like [6.32685e+04 3.00000e-03 6.32688e+04 2.00000e+00 6.32689e+04 3.73200e+00
                    6.32690e+04 3.03200e+00 6.32696e+04 3.05000e+00] that is a books5 order book asks
        Args:
            asks (list):
        """
        i = 0
        while i < len(asks):
            self.asks_dict[asks[i]] = asks[i+1]
            i += 2

    def load_bids(self, bids):
        i = 0
        while i < len(bids):
            self.bids_dict[bids[i]] = bids[i+1]
            i += 2

    def print_snapshot(self):

        print("exchange_timestamp:", self.exchange_timestamp)
        print("asks_dict:", self.asks_dict)
        print("bids_dict:", self.bids_dict)
        print("-----------------------------")
        print("\n")






class Cache():
    def __init__(self):
        self.data = []

    def load(self, data_,orderbook_depth):
        """
        load the data from the npz file, we got four arrays,
        asks_list_array, bids_list_array, exchange_timestamp
        
        Args:
            file_path (string): the path to the npz file
        """

        exchange_timestamp = data_['exchange_timestamp']
        num_rows = len(exchange_timestamp)
        for i in range(num_rows):
            snapshot = SnapShot( exchange_timestamp[i])
            self.data.append(snapshot)

        i = 0
        while i < len(data_['asks_list_array']):
            asks_list = data_['asks_list_array'][i:i+orderbook_depth*2]
            bids_list = data_['bids_list_array'][i:i+orderbook_depth*2]
            self.data[int(i/10)].load_asks(asks_list)
            self.data[int(i/10)].load_bids(bids_list)
            i += orderbook_depth*2

    def clear(self):
        del self.data[:]


def extract_date_time(file_list):
    # Assuming date time format is YYYYMMDD
    match = re.search(r'(\d{8})', file_list)
    if match:
        return match.group(1)
    else:
        return None


class OrderBook():
    """
    run the order book simulation
    """

    def __init__(self):
        self.cache = Cache()

    def run(self):
        """
        run the order book simulation
        """
        if self.cache.data:
            for snapshot in self.cache.data:
                snapshot.print_snapshot()
    
    def get_order_book(self,data_path):
        """
        this function will get the run function from the init

        Args:
            data_path (_type_): the string to folder path
            run_func (_type_): the run function to analyze or run the algo
        Returns:
            _type_: _description_
        """        
        file_paths = []
        for file in os.listdir(data_path):
            if file.endswith('.npz'):
                file_paths.append(os.path.join(data_path, file))
        for file in file_paths:
            data = np.load(file)
            orderbook_depth = int(file.split('.')[-2][-1])
            # to ensure the memory is good enough for the order book depth
            # we will pass 1000 lines as a time for the book to run, after that clear the cache and then go to the next 1000 lines.
            num_rows = len(data['exchange_timestamp'])
            i=0
            while i<num_rows:
                if i+1000<num_rows:
                    pass_data = { 'exchange_timestamp': data['exchange_timestamp'][i:i+1000],
                                 'asks_list_array': data['asks_list_array'][i:i+1000], 'bids_list_array': data['bids_list_array'][i:i+1000]}
                    i+=1000
                else:
                    pass_data = {'exchange_timestamp': data['exchange_timestamp'][i:],
                                 'asks_list_array': data['asks_list_array'][i:], 'bids_list_array': data['bids_list_array'][i:]}
                    i=num_rows
                
                self.cache.load(pass_data,orderbook_depth)
                # run_func(self.cache.data)
                self.cache.clear()
                print('The {} {} lines',file, i)
            
