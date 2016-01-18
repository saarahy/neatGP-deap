import numpy as np
def get_address(n):
    direccion1="./data_corridas/Koza/corrida%d/test_x.txt"
    xdata=np.genfromtxt(direccion1 % n, delimiter=' ')
    direccion2="./data_corridas/Koza/corrida%d/test_y.txt"
    ydata = np.genfromtxt(direccion2 % n, delimiter=' ')
    return xdata,ydata
