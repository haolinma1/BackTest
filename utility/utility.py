import math
from numba import jit
from numba.types import DictType, ListType, Tuple,unicode_type
from numba.typed import Dict, List
from numba import float64, int64, int8, boolean


@jit(nopython=True)
def str2float_helper(text):
    sep = ord(".")
    c_min = ord("0")
    c_max = ord("9")

    n = len(text)
    valid = n > 0
    # determine sign
    start = n - 1
    stop = -1
    sign = 1
    if valid:
        first = ord(text[0])
        if first == ord("+"):
            stop = 0
        elif first == ord("-"):
            sign = -1
            stop = 0
    # parse rest
    sep_pos = 0
    number = 0
    j = 0
    for i in range(start, stop, -1):
        c = ord(text[i])
        if c_min <= c <= c_max:
            number += (c - c_min) * 10 ** j
            j += 1
        elif c == sep and sep_pos == 0:
            sep_pos = j
        else:
            valid = False
            break
    return sign * number, sep_pos, valid

@jit(nopython=True)
def str2int(text):
    c_min = ord("0")
    c_max = ord("9")
    n = len(text)
    valid = n > 0
    # determine sign
    start = n - 1
    stop = -1
    sign = 1
    if valid:
        first = ord(text[0])
        if first == ord("+"):
            stop = 0
        elif first == ord('-'):
            sign = -1
            stop = 0
    # parse rest
    number = 0
    j = 0
    for i in range(start, stop, -1):
        c = ord(text[i])
        if c_min <= c <= c_max:
            number += (c - c_min) * 10 ** j
            j += 1
        else:
            valid = False
            break
    return sign * number if valid else None



@jit(nopython=True)
def str2float(text):
    if text == "nan" or text == "NAN" or text == "NaN":
        return math.nan
    exp_chars = b"eE"
    exp_pos = -1
    for exp_char in exp_chars:
        for i, c in enumerate(text[::-1]):
            c = ord(c)
            if c == exp_char:
                exp_pos = i
                break
        if exp_pos > -1:
            break
    if exp_pos > 0:
        exp_number = str2int(text[-exp_pos:])
        if exp_number is None:
            exp_number = 0
        number, sep_pos, valid = str2float_helper(text[:-exp_pos-1])
        result = number / 10.0 ** (sep_pos - exp_number) if valid else None
    else:
        number, sep_pos, valid = str2float_helper(text)
        result = number / 10.0 ** sep_pos if valid else None
    return result



@jit(nopython=True)
def parse_list(line):
    """
    parse a string list ['59312.8', '3.297'], ['59317.8', '2.000'], ['59318.0', '3.920'], ['59318.1', '6.528'], ['59318.2', '3.042']
    to float list [59312.8, 3.297, 59317.8, 2.0, 59318.0, 3.92, 59318.1, 6.528, 59318.2, 3.042]

    Args:
        line (_type_): _description_

    Returns:
        _type_: _description_
    """    
    list=List.empty_list(float64)
    str_num=unicode_type
    first_dot = True
    get_num = False
    start_i=0
    end_i=0
    for i in range(0,len(line)):
        if get_num and line[i] != '\'':
            end_i+=1

        if line[i]=='\'' and first_dot:
            first_dot=False
            get_num=True
            start_i=i+1
            end_i=i+1
        elif line[i]=='\'' and not first_dot:
            first_dot=True
            get_num=False
            str_num = line[start_i:end_i]
            start_i=0
            end_i=0
            list.append(str2float(str_num))
    return list
