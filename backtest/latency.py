import dotenv
dotenv.load_dotenv()
import os
import numpy as np
data_path = os.getenv("DATA_PATH")

class feed_latency:
    
    def __init__(self):
        self.entry_latency = None
        self.exit_latency = None

    def get_latency(self):
        """
        Connect with the exchange and get the entry latency by checking the difference timestamp and the order
        """
        file_path=[]
        latency_list = []
        for file in os.listdir(data_path):
            if file.endswith('.npz'):
                file_path.append(os.path.join(data_path, file))
        for file in file_path:
            data = np.load(file)
            local_timestamp = data['local_timestamp']
            exchange_timestamp = data['exchange_timestamp']
            latency_list += (local_timestamp - exchange_timestamp).tolist()
        latency=np.mean(latency_list)
        return latency
        
                
        