
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
            for local_timestamp in data['local_timestamp']:
                if prev_local_timestamp is None:
                    prev_local_timestamp = local_timestamp
                    continue
                elif local_timestamp <= prev_local_timestamp:
                    raise ValueError("Local timestamp not in order")
                prev_local_timestamp = local_timestamp
            # check if the exchange timestamp is in order
            prev_exchange_timestamp = None
            for exchange_timestamp in data['exchange_timestamp']:
                if prev_exchange_timestamp is None:
                    prev_exchange_timestamp = exchange_timestamp
                    continue
                elif exchange_timestamp <= prev_exchange_timestamp:
                    raise ValueError("Exchange timestamp not in order")
                prev_exchange_timestamp = exchange_timestamp



    



