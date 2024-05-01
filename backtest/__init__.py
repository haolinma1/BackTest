import dotenv
dotenv.load_dotenv()
import os
from latency import feed_latency
# data_path is the folder path to store the data
data_path = 'D:\hft-data\quite_market'
from orderbook import OrderBook



def main():
    # test the orderbook
    order=OrderBook()
    data=order.get_order_book(data_path)
    

if __name__ == '__main__':
    main()





