import os
import numpy as np

def convert_order_book(line):
    local_timestamp, data_str = line.split(" ", 1)
    local_timestamp = int(local_timestamp)
    data_dict = eval(data_str)
    data_dict = data_dict[0]
    exchange_timestamp = int(data_dict['ts'])
    asks_list = data_dict['asks']
    bids_list = data_dict['bids']
    for sublist in asks_list:
        for i in range(len(sublist)):
            sublist[i] = float(sublist[i]) 
    for sublist in bids_list:
        for i in range(len(sublist)):
            sublist[i] = float(sublist[i])
    return [local_timestamp, asks_list, bids_list,exchange_timestamp]

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
                local_timestamp=np.array([])
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
                        local_timestamp_, asks_list, bids_list,exchange_timestamp_=convert_order_book(line)
                        local_timestamp=np.append(local_timestamp, local_timestamp_)
                        asks_list_array = np.append(asks_list_array, asks_list)
                        bids_list_array = np.append(bids_list_array, bids_list)
                        exchange_timestamp=np.append(exchange_timestamp,exchange_timestamp_)
                np.savez(os.path.join(data_path, file_name.replace('.dat', '.npz')), asks_list_array=asks_list_array, bids_list_array=bids_list_array, local_timestamp=local_timestamp,exchange_timestamp=exchange_timestamp)
            elif file_name.__contains__('trade'):
                # if the file channel is trade
                pass