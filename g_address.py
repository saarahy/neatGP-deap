import numpy as np
import csv
def get_address(p,n, direccion):
    direccion=direccion%(p,n)
    with open(direccion) as spambase:
        spamReader = csv.reader(spambase,  delimiter=',', skipinitialspace=True)
        num_c = sum(1 for line in open(direccion))
        num_r = len(next(csv.reader(open(direccion), delimiter=',', skipinitialspace=True)))
        Matrix = np.empty((num_r, num_c,))
        for row, c in zip(spamReader, range(num_c)):
            for r in range(num_r):
                try:
                    Matrix[r, c] = row[r]
                except ValueError:
                    print 'Line {r} is corrupt' , r
                    break
        xdata=Matrix[:8]
        ydata=Matrix[8]
    return xdata,ydata
