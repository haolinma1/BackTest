
import numpy as np
import dotenv
import os
import numpy as np
from numba import float64, int64, int8, boolean
from numba.experimental import jitclass
from numba.typed import Dict, List
from numba.types import DictType, ListType, Tuple
dotenv.load_dotenv()
# data_path is the folder path to store the data


@jitclass
class Test:
    side:int64
    def __init__(self):
        self.side=1

order_ty = Test.class_type.instance_type
order_tup_ty = Tuple((order_ty, int64))
@jitclass
class Order:
    orderlist:ListType(order_tup_ty)
    def __init__(self) -> None:
        self.orderlist=List.empty_list(order_tup_ty)
    
    def getOrderList(self):
        return self.orderlist
    
    def append(self,test_instance,value):
        self.orderlist.append((test_instance, value))
    def __getitem__(self,key):
        if self.orderlist:
            return self.orderlist[key]
        else:
            return None


def main():
    """
    asks_list_array=[6.32685e+04 3.00000e-03 6.32688e+04 2.00000e+00 6.32689e+04 3.73200e+00
 6.32690e+04 3.03200e+00 6.32696e+04 3.05000e+00 6.32635e+04 2.62000e+00
 6.32685e+04 3.00000e-03 6.32687e+04 6.00000e-01 6.32688e+04 4.05500e+00
 6.32689e+04 1.00490e+01 6.32634e+04 1.00000e+00 6.32635e+04 2.62000e+00
 6.32687e+04 2.00000e+00 6.32688e+04 3.98100e+00 6.32689e+04 9.86000e+00]
    """    
    lines = [
    "1714246667143 [{'asks': [['63268.5', '0.003'], ['63268.8', '2.000'], ['63268.9', '3.732'], ['63269.0', '3.032'], ['63269.6', '3.050']], 'bids': [['63263.4', '7.154'], ['63263.3', '3.019'], ['63262.5', '0.553'], ['63262.4', '3.037'], ['63261.9', '3.021']], 'checksum': 0, 'ts': '1714246666077'}]",
"1714246667180 [{'asks': [['63263.5', '2.620'], ['63268.5', '0.003'], ['63268.7', '0.600'], ['63268.8', '4.055'], ['63268.9', '10.049']], 'bids': [['63263.3', '3.052'], ['63262.5', '0.553'], ['63262.4', '3.043'], ['63261.9', '3.038'], ['63261.6', '3.059']], 'checksum': 0, 'ts': '1714246666101'}]",
"1714246667259 [{'asks': [['63263.4', '1.000'], ['63263.5', '2.620'], ['63268.7', '2.000'], ['63268.8', '3.981'], ['63268.9', '9.860']], 'bids': [['63263.3', '3.051'], ['63262.5', '0.553'], ['63262.4', '3.012'], ['63261.9', '3.041'], ['63261.6', '3.014']], 'checksum': 0, 'ts': '1714246666193'}]"
    ]

    test1 = Test()
    test2 = Test()
    order=Order()
    order.append(test1,1)
    order.append(test2,2)
    
    # orderlist=order.getOrderList()[1][0]
    orderlist=order.__getitem__(0)[0].side
    print(orderlist)
    
        
    # data1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    # data2 = np.array([[10, 11, 12], [13, 14, 15], [16, 17, 18]])
    # np.savez('output.npz', asks_list_array=asks_list_array, bids_list_array=bids_list_array, timestamp_array=timestamp_array)

if __name__ == '__main__':
    main()