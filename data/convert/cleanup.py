
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
            prev_local_timestamp = None
            for index in len(data['local_timestamp']):
                if prev_local_timestamp is None:
                    prev_local_timestamp = data['local_timestamp'](index)
                    continue
                elif data['local_timestamp'](index) <= prev_local_timestamp:
                    # fix the local timestamp.
                    raise ValueError(
                        "File {} Local timestamp not in order, in line".format(file_path))
                prev_local_timestamp = data['local_timestamp'](index)
            # check if the exchange timestamp is in order
            prev_exchange_timestamp = None
            for exchange_timestamp in data['exchange_timestamp']:
                if prev_exchange_timestamp is None:
                    prev_exchange_timestamp = exchange_timestamp
                    continue
                elif exchange_timestamp <= prev_exchange_timestamp:
                    raise ValueError(
                        "File {} Exchange timestamp not in order".format(file_path))
                prev_exchange_timestamp = exchange_timestamp

            # check if the local timestamp is smaller than exchange timestamp
            if len(data['local_timestamp']) != len(data['exchange_timestamp']):
                raise ValueError(
                    "File {} Local timestamp and exchange timestamp not equal in number".format(file_path))

            for i in range(len(data['local_timestamp'])):
                if data['local_timestamp'][i] <= data['exchange_timestamp'][i]:
                    raise ValueError(
                        "File {} Local timestamp is greater than exchange timestamp in row {}".format(file_path, i+1))
            

def cleanup_local_disorder(file_path):
    """
    This function is used to clean up the local timestamp that is not in order
    """
    pass
