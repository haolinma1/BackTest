
import os
import numpy as np


def validate(data_path):
    """
    This module is used to validate the data from npz file and clean up the data
    including:1. the checking if the local timestamp is smaller than exchange timestamp
    2. checking if the exchange timestamp is in the correct order
    3. if the local timestamp is in the correct order
    """

    for file_name in os.listdir(data_path):
        if file_name.endswith('.npz'):
            file_path = os.path.join(data_path, file_name)
            data = np.load(file_path)
            # check if the local timestamp is in order
            # prev_local_timestamp = None
            # for index in range(len(data['local_timestamp'])):
            #     if prev_local_timestamp is None:
            #         prev_local_timestamp = data['local_timestamp'][index]
            #         continue
            #     elif data['local_timestamp'][index] < prev_local_timestamp:
            #         raise ValueError(
            #             "File {} Local timestamp not in order, in line {}".format(file_path, index+1))
            #     prev_local_timestamp = data['local_timestamp'][index]
            # check if the exchange timestamp is in order
            prev_exchange_timestamp = None
            for index in range(len(data['exchange_timestamp'])):
                if prev_exchange_timestamp is None:
                    prev_exchange_timestamp = data['exchange_timestamp'][index]
                    continue
                elif data['exchange_timestamp'][index] <= prev_exchange_timestamp:
                    raise ValueError(
                        "File {} Exchange timestamp not in order in line {}".format(file_path, index))
                prev_exchange_timestamp = data['exchange_timestamp'][index]

            # check if the local timestamp is smaller than exchange timestamp
            # if len(data['local_timestamp']) != len(data['exchange_timestamp']):
            #     raise ValueError(
            #         "File {} Local timestamp and exchange timestamp not equal in number".format(file_path))

            # for i in range(len(data['local_timestamp'])):
            #     if data['local_timestamp'][i] <= data['exchange_timestamp'][i]:
            #         raise ValueError(
            #             "File {} Local timestamp is greater than exchange timestamp in row {}".format(file_path, i+1))
            # print("File {} is valid".format(file_path))

def fix_local_disorder(data_path):
    """
    When the two sequent data from exchange is extremely small, the exchange timestamp will be the same, also get rid of the local timestamp
    """
    #
    for file_name in os.listdir(data_path):
        if file_name.endswith('.npz'):
            file_path = os.path.join(data_path, file_name)
            data = np.load(file_path)
            exchange_timestamp = data['exchange_timestamp']
            asks_list_array=data['asks_list_array']
            bids_list_array=data['bids_list_array']
            for index in range(len(exchange_timestamp)- 1):
                if exchange_timestamp[index] == exchange_timestamp[index+1]:
                    exchange_timestamp[index+1] = exchange_timestamp[index+1] + 1
                    print('fixed')
            np.savez(file_path, exchange_timestamp=exchange_timestamp, asks_list_array=asks_list_array, bids_list_array=bids_list_array)
            
    
    

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
