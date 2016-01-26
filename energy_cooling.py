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

pset = gp.PrimitiveSet("MAIN", 5)
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
pset.renameArguments(ARG0='x0',ARG1='x1', ARG2='x2', ARG3='x3', ARG4='x4')


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("FitnessTest", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, fitness_test=creator.FitnessTest)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, min_=1, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

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

def evalSymbRegKorns(individual, test):
    func = toolbox.compile(expr=individual)
    if test:
        long=int(len(Matrix.T)*.7)
    else:
        long=int(len(Matrix.T)*.3)
    spam_samp = random.sample(Matrix.T, long)
    vector = [data[10] for data in spam_samp]
    result = np.sum((func(*np.asarray(spam_samp).T[:10]) - vector)**2)
    return result/long,


def main(n_corr, p):


    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genFull, min_=0, max_=3)
    toolbox.register("mutate", gp.mutUniform, pset=pset)
    toolbox.register("evaluate", evalSymbRegKorns, test=False)
    toolbox.register("evaluate_test", evalSymbRegKorns, points=Matrix, test=True)

    pop = toolbox.population(n=500)
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
    neat_cx = True
    neat_alg = True
    neat_pelit = 0.5
    neat_h = 0.15
    funcEval.LS_flag = True
    LS_select = 1
    funcEval.cont_evalp=0
    cont_evalf = 2500000 #contador maximo de de evaluaciones

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb, mutpb, ngen, neat_alg, neat_cx, neat_h, neat_pelit, funcEval.LS_flag, LS_select, cont_evalf,pset,n_corr, p, params, stats=mstats, halloffame=hof, verbose=True)

    outfile = open('popfinal_%d_%d.txt' % (p, n_corr), 'w')

    outfile.write("\n Best individual is: %s %s %s " %( hof[0].fitness, hof[0].fitness_test, str(hof[0])))
    outfile.write("\n Best individual is: %s %s %s" % ( hof[1].fitness, hof[1].fitness_test, str(hof[1])))
    outfile.write("\n Best individual is: %s %s %s" % ( hof[2].fitness, hof[2].fitness_test, str(hof[2])))

    sortf = sort_fitnessvalues(pop)
    for ind in sortf:
        outfile.write('\n%s;%s;%s;%s;%s;%s;%s;%s' %(funcEval.cont_evalp,len(ind), ind.height, ind.get_specie(), ind.fitness.values[0], ind.get_fsharing(), ind.fitness_test.values[0], ind))
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