import sys
sys.path.append('../')
import numba as nb
import numpy as np
import math 
from numba import jit
from numba import float64, int64, int8, boolean
from numba.types import DictType, ListType, Tuple,unicode_type
from numba.typed import Dict, List
import os
from utility.utility import parse_list,str2int
import re
data = "[{'asks': [['59312.8', '3.297'], ['59317.8', '2.000'], ['59318.0', '3.920'], ['59318.1', '6.528'], ['59318.2', '3.042']], 'bids': [['59312.7', '4.881'], ['59309.9', '0.591'], ['59309.8', '3.014'], ['59309.7', '3.056'], ['59309.1', '3.027']], 'checksum': 0, 'ts': '1714680797447'}]"
data2= "[{'asks': [['3125.57', '1.05'], ['3125.75', '41.49'], ['3125.76', '190.84'], ['3125.77', '121.86'], ['3125.78', '120.22']], 'bids': [['3125.41', '17.12'], ['3125.36', '15.27'], ['3125.35', '21.81'], ['3125.33', '15.32'], ['3125.32', '25.37']], 'checksum': 0, 'ts': '1714965393591'}]"
@jit(nopython=True)
def parse_data_string(data_string):
    # Initialize an empty list to store the parsed data
    parsed_data = []
    inside_list = False
    current_list = []
    current_value = ""

    # Iterate over each character in the string
    for char in data_string:
        if char == '[':
            if not inside_list:
                inside_list = True
                current_list = []
        elif char == ']':
            if inside_list:
                if current_value:
                    current_list.append(current_value)
                parsed_data.append(current_list)
                inside_list = False
                current_value = ""
        elif char == ',':
            if inside_list:
                if current_value:
                    current_list.append(current_value)
                current_value = ""
        elif char == "'":
            pass  # Ignore single quotes
        elif char == ' ':
            pass  # Ignore spaces
        else:
            current_value += char

    return parsed_data

@jit(nopython=True)
def parse_float(line,index):
    print(line[index])



    

            


      



# [{'asks': [['59312.8', '3.297'], ['59317.8', '2.000'], ['59318.0', '3.920'], ['59318.1', '6.528'], ['59318.2', '3.042']], 'bids': [['59312.7', '4.881'], ['59309.9', '0.591'], ['59309.8', '3.014'], ['59309.7', '3.056'], ['59309.1', '3.027']], 'checksum': 0, 'ts': '1714680797447'}]
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


            


data_="D:/hft-data/test/BTCUSDT_20240427_books5.npz"

def main():
    """ asks_list1,bid_list1,ts=turn_line_array(data2)
    ask2,bid2,ts2=turn_line_array(data)
    asks_list1.extend(ask2)
    print(asks_list1) """
    data = np.load(data_)
    exchange_timestamp = data['exchange_timestamp']
    print(exchange_timestamp)


if __name__ == '__main__':
    main()
