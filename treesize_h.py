import numpy as np
import random
from tree_subt import add_subt
from scipy.optimize.minpack import curve_fit_2
from tree2func import tree2f
from eval_str import eval_

def eval_prob(population):
    n_nodes=[]
    for ind in population:
        n_nodes.append(len(ind))
    nn_nodes=np.asarray(n_nodes)
    av_size=np.mean(nn_nodes)
    c=1.5
    for ind in population:
        ind.LS_probability(0.)
        y=c-(len(ind)/av_size)
        if y>1.:
            ps=1
            ind.LS_probability(1.)
        elif (y>=0. and y<=1.):
            ps=y
            ind.LS_probability(y)
def trees_h(population):
    eval_prob(population)
    for ind in population:
        if random.random()<ind.get_LS_prob():
            strg=ind.__str__() #convierte en str el individuo
            l_strg=add_subt(strg) #le anade el arbol y lo convierte en arreglo
            c = tree2f() #crea una instancia de tree2f
            cd=c.convert(l_strg) #convierte a l_strg en infijo
            cd2=c.convert_r(l_strg)
            direccion1="./data_corridas/Koza/corrida1/test_x.txt"
            xdata=np.genfromtxt(direccion1, delimiter=' ')
            direccion2="./data_corridas/Koza/corrida1/test_y.txt"
            ydata = np.genfromtxt(direccion2, delimiter=' ')
            print ind, len(ind)
            sizep=len(ind)+2
            ind.params_set(np.ones(sizep))
            print ind.get_params()
            beta_opt, beta_cov, info, msg, success= curve_fit_2(eval_,cd , xdata, ydata, p0=ind.get_params() ,full_output=1, maxfev=250000)
            #necesitamos sustituir los valores de la cadena de parametros
            ind.params_set(beta_opt)
            print ind.get_params()
            #print('number of function calls =', info['nfev'])
            #print msg
            #print beta_opt

def specie_h(population):
    return 'hey'

def best_specie(population):
    return 'hey'
