import numpy as np
import os
import dotenv
from convert import convert
from cleanup import validate, fix_local_disorder
dotenv.load_dotenv()

# data_path is the folder path to store the data
data_path = 'D:\hft-data\quite_market'





def main():
    # convert(data_path)
    validate(data_path)
    # fix_local_disorder(data_path)
    


if __name__ == '__main__':
    main()