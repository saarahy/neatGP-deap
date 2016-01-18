from numpy import sin, cos, divide, division, seterr
from my_operators import safe_div, mylog
from operator import add, sub, mul


def eval_(strg, x, *p):
    seterr(divide='ignore', invalid='ignore')
    try:
        x = eval(strg)
    except TypeError:
        print 'Error.', strg

    return x

