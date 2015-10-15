import math


def safe_div(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 0.0


def mylog(x):
    if x == 0:
        return 0.0
    else:
        return math.log10(abs(x))


def mysqrt(x):
    if x <= 0.0:
        return 0.0
    else:
        return math.sqrt(x)


def mypower2(x):
    y = math.pow(x, 2)
    if isinstance(y, complex) or math.isinf(y) or math.isnan(y):
        return 0.0
    else:
        return y


def mypower3(x):
    y = math.pow(x, 3)
    if isinstance(y, complex) or math.isinf(y) or math.isnan(y):
        return 0.0
    else:
        return y


def negative(x):
    return -x


def undivide(x):
    if x == 0:
        return 1.0
    else:
        return 1.0/x
