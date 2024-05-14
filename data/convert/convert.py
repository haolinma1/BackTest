import os
import numpy as np
from numba import jit
import sqlite3
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
                db_path=os.path.join(data_path,file_name.replace('.dat','.db'))
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS PRICE
                 (TIMESTAMP INT PRIMARY KEY    NOT NULL,
                 LEVEL10          REAL    NOT NULL,
                 LEVEL9           REAL     NOT NULL,
                 LEVEL8          REAL    NOT NULL,
                 LEVEL7          REAL    NOT NULL,
                 LEVEL6          REAL    NOT NULL,
                 LEVEL5          REAL    NOT NULL,
                 LEVEL4          REAL    NOT NULL,
                 LEVEL3          REAL    NOT NULL,
                 LEVEL2          REAL    NOT NULL,
                 LEVEL1          REAL    NOT NULL);''')
        
                conn.execute('''CREATE TABLE IF NOT EXISTS QUANTITY
                 (TIMESTAMP INT NOT NULL,
                 LEVEL10          REAL    NOT NULL,
                 LEVEL9           REAL     NOT NULL,
                 LEVEL8          REAL    NOT NULL,
                 LEVEL7          REAL    NOT NULL,
                 LEVEL6          REAL    NOT NULL,
                 LEVEL5          REAL    NOT NULL,
                 LEVEL4          REAL    NOT NULL,
                 LEVEL3          REAL    NOT NULL,
                 LEVEL2          REAL    NOT NULL,
                 LEVEL1          REAL    NOT NULL,
                 FOREIGN KEY (TIMESTAMP) REFERENCES PRICE(TIMESTAMP));''')

                with open(file_path, 'r') as f:
                    data = f.readlines()
                    prev_timestamp=0
                    for line in data:
                        line = line.strip()
                        if not line:
                            continue
                        asks_list, bids_list,exchange_timestamp_=turn_line_array(line)
                        if exchange_timestamp_==prev_timestamp:
                            exchange_timestamp_=exchange_timestamp_+1
                        query = "INSERT INTO QUANTITY (TIMESTAMP, LEVEL10, LEVEL9, LEVEL8, LEVEL7,LEVEL6,LEVEL5,LEVEL4,LEVEL3,LEVEL2,LEVEL1) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                        cursor.execute(query, (exchange_timestamp_, asks_list[-1], asks_list[-3], asks_list[-5], asks_list[-7],asks_list[-9],bids_list[1],bids_list[3],bids_list[5],bids_list[7],bids_list[9]))
                        query = "INSERT INTO PRICE (TIMESTAMP, LEVEL10, LEVEL9, LEVEL8, LEVEL7,LEVEL6,LEVEL5,LEVEL4,LEVEL3,LEVEL2,LEVEL1) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                        cursor.execute(query, (exchange_timestamp_, asks_list[-2], asks_list[-4], asks_list[-6], asks_list[-8],asks_list[-10],bids_list[0],bids_list[2],bids_list[4],bids_list[6],bids_list[8]))
                        conn.commit()
                        prev_timestamp=exchange_timestamp_
                cursor.execute('VACUUM')
                conn.close()
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