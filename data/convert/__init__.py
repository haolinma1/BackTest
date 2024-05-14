import numpy as np
import os
import dotenv
from convert import convert
from cleanup import validate, fix_local_disorder
dotenv.load_dotenv()

# data_path is the folder path to store the data
data_path = 'C:/Users/haolin/Desktop/backtest/data/example'
# file_path = os.getenv("DATA_PATH")

file="D:/hft-data/process-data/BTCUSDT_20240502_books5.npz"

def getData(file_path):
    """
    This function is used to get the data from the npz file
    """
    data = np.load(file_path)
    exchange_timestamp = data['exchange_timestamp']
    asks_list_array = data['asks_list_array']
    bids_list_array = data['bids_list_array']
    return exchange_timestamp, asks_list_array, bids_list_array

def main():
    # convert the data
    convert(data_path)
    # validate(data_path)
    
    


if __name__ == '__main__':
    main()