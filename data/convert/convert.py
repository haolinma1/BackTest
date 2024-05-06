import os
import numpy as np
from numba import jit
import sys
sys.path.append('../../')
from utility.utility import parse_list,str2int
from numba import jit
from numba import float64, int64, int8, boolean
from numba.types import DictType, ListType, Tuple,unicode_type
from numba.typed import Dict, List


def convert(data_path):
    """
    Convert the dat file from data to npz compressed file for the backtest to use
    delete the dat file
    if the file is order book, the asks_list_array or bids_list_array will just get all the data and store it in an array,
    we need to convert them back to the original format, example see test.py
    """  

    for file_name in os.listdir(data_path):
        if file_name.endswith('.dat'):
            # convert the data format .dat
            if file_name.__contains__('book'):
                # if the file is order book
                asks_list_array=np.array([])
                bids_list_array=np.array([])
                exchange_timestamp=np.array([])
                file_path = os.path.join(data_path, file_name)
                with open(file_path, 'r') as f:
                    data = f.readlines()
                    for line in data:
                        line = line.strip()
                        if not line:
                            continue
                        asks_list, bids_list,exchange_timestamp_=turn_line_array(line)
                        asks_list_array = np.append(asks_list_array, asks_list)
                        bids_list_array = np.append(bids_list_array, bids_list)
                        exchange_timestamp=np.append(exchange_timestamp,exchange_timestamp_)
                np.savez(os.path.join(data_path, file_name.replace('.dat', '.npz')), asks_list_array=asks_list_array, bids_list_array=bids_list_array,exchange_timestamp=exchange_timestamp)
            elif file_name.__contains__('trade'):
                # if the file channel is trade
                pass


@jit(nopython=True)
def turn_line_array(line):
    asks_list = List.empty_list(float64)
    bid_list = List.empty_list(float64)
    ts=int64
    begin = line.find("'asks'",0)+9
    end = line.find("'bids'",begin)-3
    asks_list=parse_list(line[begin:end])
    begin = line.find("'bids'",end)+9
    end = line.find("'checksum'",begin)-3
    bid_list=parse_list(line[begin:end])
    begin = line.find("'ts'",end)+7
    end = line.find("}",begin)-1
    ts=str2int(line[begin:end])
    return asks_list,bid_list,ts