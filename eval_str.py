from numpy import sin, cos
from my_operators import safe_div, mylog
def eval_(strg, x, *p):
    x= eval(strg)
    #print x
    return x