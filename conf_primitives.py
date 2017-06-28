import random
import operator
import numpy as np
import math
from deap import gp
from my_operators import safe_div, mylog, mypower2, mypower3, mysqrt, myexp, negexp, absolute, negative

def koza1(samples):
    return samples**4 + samples**3 + samples**2 + samples
def korns12(samples):
    return 2.0-(2.1 * (np.cos(9.8 * samples.T[:, 0]) * np.sin(1.3 * samples.T[:, 4])))
def nguyen3(samples):
    return samples ** 5 + samples ** 4 + samples ** 3 + samples ** 2 + samples,
def nguyen5(samples):
    return np.sin(samples ** 2) * np.cos(samples) - 1
def nguyen7(samples):
    return np.log(samples + 1.0) + np.log(samples ** 2 + 1.0)
def nguyen10(samples):
    return 2.0 * np.sin(samples.T[:, 0]) * np.cos(samples.T[:, 1])
def pagie1(samples):
    return (1 / (1 + samples.T[:, 0] ** -4)) + (1 / (1 + samples.T[:, 1] ** -4))
def keijzer6(samples):
    return np.sum(1.0 / samples)
def vladislavleva1(samples):
    return (np.exp(-((samples.T[:,0]-1)**2)))/(1.2+((samples.T[:,1]-2.5)**2))

def vector_benchmarks(argument, samples):
    if argument in 'koza-1':
        return koza1(samples)
    elif argument in 'nguyen-3':
        return nguyen3(samples)
    elif argument in 'nguyen-5':
        return nguyen5(samples)
    elif argument in 'nguyen-7':
        return nguyen7(samples)
    elif argument in 'nguyen-10':
        return nguyen10(samples)
    elif argument in 'pagie-1':
        return pagie1(samples)
    elif argument in 'korns-12':
        return korns12(samples)
    elif argument in 'keijzer-6':
        return keijzer6(samples)
    elif argument in 'vladislavleva-1':
        return vladislavleva1(samples)



def rename_arguments(argument,pset):
    switcher = {
        1: pset.renameArguments(ARG0='x0'),
        2: pset.renameArguments(ARG0='x0',ARG1='x1'),
        6: pset.renameArguments(ARG0='x0',ARG1='x1', ARG2='x2', ARG3='x3', ARG4='x4', ARG5='x5'),
        7: pset.renameArguments(ARG0='x0', ARG1='x1', ARG2='x2', ARG3='x3', ARG4='x4', ARG5='x5', ARG='x6'),
        8: pset.renameArguments(ARG0='x0',ARG1='x1', ARG2='x2', ARG3='x3', ARG4='x4', ARG5='x5', ARG6='x6', ARG7='x7'),
        13: pset.renameArguments(ARG0='x0', ARG1='x1', ARG2='x2', ARG3='x3', ARG4='x4', ARG5='x5', ARG6='x6', ARG7='x7',
                                 ARG8='x8', ARG9='x9', ARG10='x10', ARG11='x11', ARG12='x12'),
        25: pset.renameArguments(ARG0='x0', ARG1='x1', ARG2='x2', ARG3='x3', ARG4='x4', ARG5='x5', ARG6='x6', ARG7='x7',
                                 ARG8='x8', ARG9='x9', ARG10='x10', ARG11='x11', ARG12='x12', ARG13='x13', ARG14='x14',
                                 ARG15='x15',
                                 ARG16='x16', ARG17='x17', ARG18='x18', ARG19='x19', ARG20='x20', ARG21='x21',
                                 ARG22='x22', ARG23='x23', ARG24='x24'),
    }
    return pset



def conf_sets(num_var):
    pset = gp.PrimitiveSet("MAIN", num_var)
    pset.addPrimitive(operator.add, 2)
    pset.addPrimitive(operator.sub, 2)
    pset.addPrimitive(operator.mul, 2)
    pset.addPrimitive(safe_div, 2)
    pset.addPrimitive(np.cos, 1)
    pset.addPrimitive(np.sin, 1)
    pset.addPrimitive(mylog, 1)
    pset.addPrimitive(mypower2, 1)
    pset.addPrimitive(mypower3, 1)
    pset.addPrimitive(mysqrt, 1)
    pset.addPrimitive(np.tan, 1)
    pset.addPrimitive(np.tanh, 1)
    #pset.addPrimitive(myexp, 1)
    #pset.addPrimitive(negexp, 1)
    pset.addPrimitive(absolute, 1)
    pset.addPrimitive(negative, 1)
    pset.addEphemeralConstant("rand101", lambda: random.uniform(-1, 1))

    pset=rename_arguments(num_var, pset)
    return pset

