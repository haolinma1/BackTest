

class feed_latency:
    
    def __init__(self, latency):
        self.entry_latency = None
        self.exit_latency = None

    def get_latency(self):
        """
        Connect with the exchange and get the entry latency by checking the difference timestamp and the order
        """        
        