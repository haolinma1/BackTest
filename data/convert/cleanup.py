
import os
import numpy as np
from numba import jit

def validate(file_path):
    """
    This function is used to open the file and return the data
    """

    for file_name in os.listdir(file_path):
        if file_name.endswith('.npz'):
            file_path = os.path.join(file_path, file_name)
            data = np.load(file_path)
            exchange_timestamp = data['exchange_timestamp']
            index=validate_(exchange_timestamp)
            # get_snapshot(index,data)
            if index is not None:
                raise ValueError("File {} is not correct,line {}".format(file_name,index))




@jit(nopython=True)
def validate_(exchange_timestamp: np.array):
    """
    This module is used to validate the data from npz file and clean up the data
    including:1. the checking if the local timestamp is smaller than exchange timestamp
    2. checking if the exchange timestamp is in the correct order
    3. if the local timestamp is in the correct order
    """
    prev_exchange_timestamp = None
    for index in range(len(exchange_timestamp)):
        if prev_exchange_timestamp is None:
            prev_exchange_timestamp = exchange_timestamp[index]
            continue
        elif exchange_timestamp[index] <= prev_exchange_timestamp:
            return index
        prev_exchange_timestamp = exchange_timestamp[index]
    return None


def fix_local_disorder(file_path,index):
    """
    When the two sequent data from exchange is extremely small, the exchange timestamp will be the same, also get rid of the local timestamp
    """
    data = np.load(file_path)
    exchange_timestamp = data['exchange_timestamp']
    asks_list_array = data['asks_list_array']
    bids_list_array = data['bids_list_array']
    correct_timestamp = None
    exchange_timestamp[index]+=1
    correct_timestamp = exchange_timestamp
    np.savez(file_path, asks_list_array=asks_list_array, bids_list_array=bids_list_array,exchange_timestamp=correct_timestamp)
    
    
            
    
    

def get_snapshot(index,data,mark_depth=5):
    """
    This function is used to get the snapshot of the order book
    """
    asks_list=[]
    bids_list=[]
    for i in range(index*mark_depth*2,index*mark_depth*2+mark_depth*2):
        asks_list.append(data['asks_list_array'][i])
        bids_list.append(data['bids_list_array'][i])
    print(asks_list)
    print(bids_list)
    print(data['exchange_timestamp'][index])
