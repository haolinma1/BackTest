import numpy as np
import os
import dotenv
dotenv.load_dotenv()
# data_path is the folder path to store the data
data_path = os.getenv("DATA_PATH")

def convert_order_book(line):
    timestamp, data_str = line.split(" ", 1)
    timestamp = int(timestamp)
    data_dict = eval(data_str)
    data_dict = data_dict[0]
    asks_list = data_dict['asks']
    bids_list = data_dict['bids']
    for sublist in asks_list:
        for i in range(len(sublist)):
            sublist[i] = float(sublist[i]) 
    for sublist in bids_list:
        for i in range(len(sublist)):
            sublist[i] = float(sublist[i])
    return [timestamp, asks_list, bids_list]



def main():
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
                timestamp_array=np.array([])
                asks_list_array=np.array([])
                bids_list_array=np.array([])
                file_path = os.path.join(data_path, file_name)
                with open(file_path, 'r') as f:
                    data = f.readlines()
                    for line in data:
                        line = line.strip()
                        if not line:
                            continue
                        timestamp, asks_list, bids_list=convert_order_book(line)
                        timestamp_array=np.append(timestamp_array, timestamp)
                        asks_list_array = np.append(asks_list_array, asks_list)
                        bids_list_array = np.append(bids_list_array, bids_list)
                np.savez(os.path.join(data_path, file_name.replace('.dat', '.npz')), asks_list_array=asks_list_array, bids_list_array=bids_list_array, timestamp_array=timestamp_array)
                        


if __name__ == '__main__':
    main()