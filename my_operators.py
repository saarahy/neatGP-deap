import math
import numpy as np

z = np.array([0.])


def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return z

def myexp(x):
    with np.errstate(divide='ignore',invalid='ignore'):
        if isinstance(x, np.ndarray):
            x[x>700]=700
            x = np.exp(x)
            print x[np.isinf(x)]
            x[np.isinf(x)] = 0.0
            x[np.isnan(x)] = 0.0
        else:
            if x<700:
                x=700
            x=np.exp(x)
            if np.isinf(x):
                x=0.0
        return x


def safe_div(left, right):
    with np.errstate(divide='ignore',invalid='ignore'):
        x = np.divide(left, right)
        if isinstance(x, np.ndarray):
            x[np.isinf(x)] = 0.0
            x[np.isnan(x)] = 0.0
        elif np.isinf(x) or np.isnan(x):
            x = 0.0
    return x


def mylog(x):
    with np.errstate(divide='ignore',invalid='ignore'):
        if isinstance(x,np.ndarray):
            x=np.log10(abs(x))
            x[np.isinf(x)] = 0.
            x[np.isnan(x)] = 0.0
            return x
        else:
            if x == 0:
                return z
            else:
                return np.log10(abs(x))


def mysqrt(x):
    if isinstance(x,np.ndarray):
        x[x<=0.0]=0.0
        return np.sqrt(x)
    else:
        if x <= 0.0:
            return z
        else:
            return np.sqrt(x)


def mypower2(x):
    if isinstance(x,np.ndarray):
        y = np.power(x, 2)
    else:
        y = [np.power(x, 2)]
    if np.logical_or(isinstance(y, complex), np.isinf(y), np.isnan(y)).all():
        return z
    else:
        return np.array(y)


def mypower3(x):
    if isinstance(x,np.ndarray):
        y = np.power(x, 3)
    else:
        y = [np.power(x, 3)]
    if np.logical_or(isinstance(y, complex), np.isinf(y), np.isnan(y)).all():
        return z
    else:
        return np.array(y)


def negative(x):
    return -x


def undivide(x):
    if isinstance(x,np.ndarray):
        with np.errstate(divide='ignore',invalid='ignore'):
            x = np.divide(1.0, x)
            x[np.isinf(x)] = 0.0
            x[np.isnan(x)] = 0.0
            return x
    else:
        if x == 0:
            return 1.0
        else:
            return 1.0/x

def avg_nodes(population):
    n_nodes=[]
    for ind in population:
        n_nodes.append(len(ind))
    nn_nodes=np.asarray(n_nodes)
    av_size=np.mean(nn_nodes)
    return av_size