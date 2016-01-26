import operator
import math
import random
import csv
import cProfile
import funcEval
import numpy as np
from decimal import Decimal
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
from neat_operators import neatGP
from ParentSelection import sort_fitnessvalues
from my_operators import safe_div, mylog, mypower2, mypower3, mysqrt, myexp
from tree2func import tree2f
from tree_subt import add_subt_cf

pset = gp.PrimitiveSet("MAIN", 8)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(safe_div, 2)
pset.addPrimitive(np.cos, 1)
pset.addPrimitive(np.sin, 1)
#pset.addPrimitive(myexp, 1)
pset.addPrimitive(mylog, 1)
pset.addPrimitive(mypower2, 1)
pset.addPrimitive(mypower3, 1)
pset.addPrimitive(mysqrt, 1)
pset.addPrimitive(np.tan, 1)
pset.addPrimitive(np.tanh, 1)
pset.addEphemeralConstant("rand101", lambda: random.uniform(-1, 1))
pset.renameArguments(ARG0='x0',ARG1='x1', ARG2='x2', ARG3='x3', ARG4='x4', ARG5='x5', ARG6='x6', ARG7='x7',  ARG8='x8')


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("FitnessTest", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, fitness_test=creator.FitnessTest)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, min_=1, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)




def evalSymbRegKorns(individual, test, points):
    func = toolbox.compile(expr=individual)
    vector = [data[8] for data in points]
    try:
        result = np.sum((func(*np.asarray(points).T[:8]) - vector)**2)
    except TypeError:
        result = np.sum(np.power((np.subtract(func(*np.asarray(points).T[:8]),vector)),2))
    return result/len(points),

def energy_coolng(n_corr):
    direccion="./data_corridas/EnergyCooling/energy_efficiency_Cooling.txt"
    with open(direccion) as spambase:
        spamReader = csv.reader(spambase,  delimiter=' ', skipinitialspace=True)
        num_c = sum(1 for line in open(direccion))
        num_r = len(next(csv.reader(open(direccion), delimiter=' ', skipinitialspace=True)))
        Matrix = np.empty((num_r, num_c,))
        for row, c in zip(spamReader, range(num_c)):
            for r in range(num_r):
                try:
                    Matrix[r, c] = row[r]
                except ValueError:
                    print 'Line {r} is corrupt' , r
                    break
    long_test=int(len(Matrix.T)*.7)
    long_train=int(len(Matrix.T)*.3)
    data_test = random.sample(Matrix.T, long_test)
    data_train = random.sample(Matrix.T, long_train)
    np.savetxt('./data_corridas/EnergyCooling/test_%d.txt'%(n_corr), data_test, delimiter=",", fmt="%s")
    np.savetxt('./data_corridas/EnergyCooling/train_%d.txt'%(n_corr), data_train, delimiter=",", fmt="%s")
    # outd=open('./data_corridas/EnergyCooling/test_%d.txt'%(n_corr), 'a')
    # outd.write(data_test[:])
    # outd.close()
    # outd=open('./data_corridas/EnergyCooling/train_%d.txt'%(n_corr), 'a')
    # outd.write(data_train[:])
    # outd.close()
    toolbox.register("evaluate", evalSymbRegKorns, test=False, points=data_train)
    toolbox.register("evaluate_test", evalSymbRegKorns,  test=True, points=data_test)


def main(n_corr, p):
    energy_coolng(n_corr)

    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genFull, min_=0, max_=3)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
    # toolbox.register("evaluate", evalSymbRegKorns, test=False, p=n_corr)
    # toolbox.register("evaluate_test", evalSymbRegKorns,  test=True, p=n_corr)

    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(3)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    stats_fit_test = tools.Statistics(lambda i: i.fitness_test.values)
    mstats = tools.MultiStatistics(fitness=stats_fit,size=stats_size, fitness_test=stats_fit_test)
    mstats.register("avg", np.mean)
    mstats.register("std", np.std)
    mstats.register("min", np.min)
    mstats.register("max", np.max)
    cxpb = 0.7
    mutpb = 0.3
    ngen = 30000
    params = ['best_of_each_specie', 2, 'yes']
    neat_cx = False
    neat_alg = False
    neat_pelit = 0.5
    neat_h = 0.15
    funcEval.LS_flag = False
    LS_select = 3
    funcEval.cont_evalp=0
    cont_evalf = 2500000 #contador maximo de de evaluaciones

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb, mutpb, ngen, neat_alg, neat_cx, neat_h, neat_pelit, funcEval.LS_flag, LS_select, cont_evalf,pset,n_corr, p, params, stats=mstats, halloffame=hof, verbose=True)

    outfile = open('popfinal_%d_%d.txt' % (p, n_corr), 'w')

    outfile.write("\n Best individual is: %s %s %s " %( hof[0].fitness, hof[0].fitness_test, str(hof[0])))
    outfile.write("\n Best individual is: %s %s %s" % ( hof[1].fitness, hof[1].fitness_test, str(hof[1])))
    outfile.write("\n Best individual is: %s %s %s" % ( hof[2].fitness, hof[2].fitness_test, str(hof[2])))

    sortf = sort_fitnessvalues(pop)
    if funcEval.LS_flag:
            for ind in sortf:
                strg=ind.__str__() #convierte en str el individuo
                l_strg=add_subt_cf(strg, args=[]) #le anade el arbol y lo convierte en arreglo
                c = tree2f() #crea una instancia de tree2f
                cd=c.convert(l_strg) #convierte a l_strg en infijo
                outfile.write('\n%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s' %(len(ind), ind.height, ind.get_specie(), ind.bestspecie_get(), ind.LS_applied_get(),ind.fitness.values[0], ind.get_fsharing(), ind.fitness_test.values[0], ind.LS_fitness_get(),cd,ind))
            print funcEval.cont_evalp
    else:
            for ind in sortf:
                outfile.write('\n%s;%s;%s;%s;%s;%s;%s;%s;%s;%s' %(len(ind), ind.height, ind.get_specie(), ind.bestspecie_get(), ind.LS_applied_get(),ind.fitness.values[0], ind.get_fsharing(), ind.fitness_test.values[0], ind.LS_fitness_get(),ind))
    outfile.close()
    return pop, log, hof


def run(number, problem):
    n = 1
    while n <= number:
        main(n, problem)
        n += 1


if __name__ == "__main__":
    n = 1
    while n < 31:
        #cProfile.run('print main(n, 9); print')
        main(n, 9)
        n += 1