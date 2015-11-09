import operator
import math
import random
import csv
import cProfile
import numpy as np
from numpy import genfromtxt
from decimal import Decimal
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
from neat_operators import neatGP
from ParentSelection import sort_fitnessvalues
from my_operators import undivide, negative, mysqrt

pset = gp.PrimitiveSet("MAIN", 1)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(undivide, 1)
pset.addPrimitive(negative, 1)
pset.addPrimitive(mysqrt, 1)
pset.renameArguments(ARG0='x')

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("FitnessTest", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, fitness_test=creator.FitnessTest)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, min_=1, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def evalSymbReg(individual, points):
    func = toolbox.compile(expr=individual)
    values=np.sum(1.0/points)
    sqerrors = np.sum((func(points) - values)**2)
    return sqerrors / len(points),

def Keijzer6(n_corr):
    direccion="./data_corridas/Keijzer6/corrida%d/test_x.txt"
    direccion2="./data_corridas/Keijzer6/corrida%d/train_x.txt"
    my_data = np.genfromtxt(direccion % n_corr, delimiter=' ')
    my_data2 = np.genfromtxt(direccion2 % n_corr, delimiter=' ')
    toolbox.register("evaluate", evalSymbReg, points=my_data2)
    toolbox.register("evaluate_test", evalSymbReg, points=my_data)

# def evalSymbReg(individual, points):
#     func = toolbox.compile(expr=individual)
#     sqerrors = []
#     for elem in range(len(points)):
#         num_div = [1.0/x for x in points[:elem]]
#         y=np.sum(num_div[x] for x in range(0,len(num_div)))
#         sqerrors.append((func(points[elem])-(y))**2)
#     return math.fsum(sqerrors) / len(points),
#
#
# def Keijzer6(n_corr):
#     direccion="./data_corridas/Keijzer6/corrida%d/test_x.txt"
#     direccion2="./data_corridas/Keijzer6/corrida%d/train_x.txt"
#     with open(direccion % n_corr) as spambase:
#         spamReader = csv.reader(spambase)
#         spam = [float(row[0]) for row in spamReader]
#     with open(direccion2% n_corr) as spamb:
#         spamReader2 = csv.reader(spamb)
#         spam2 = [float(row[0]) for row in spamReader2]
#     toolbox.register("evaluate", evalSymbReg, points=spam2)
#     toolbox.register("evaluate_test", evalSymbReg, points=spam)


def main(n_corr,p):
    Keijzer6(n_corr)

    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genFull, min_=0, max_=3)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

    pop = toolbox.population(n=500)
    hof = tools.HallOfFame(3)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    stats_fit_test=tools.Statistics(lambda i: i.fitness_test.values)
    mstats = tools.MultiStatistics(fitness=stats_fit,size=stats_size, fitness_test= stats_fit_test)
    mstats.register("avg", np.mean)
    mstats.register("std", np.std)
    mstats.register("min", np.min)
    mstats.register("max", np.max)
    params = ['best_of_each_specie', 2, 'yes']
    neatcx = True
    neat = True
    pelit = 0.5
    pop, log = algorithms.eaSimple(pop, toolbox, 0.7, 0.3, 100, neat, neatcx, 0.15, pelit, n_corr, p, params, stats=mstats, halloffame=hof, verbose=True)

    outfile = open('popfinal_%d_%d.txt'%(p,n_corr), 'w')

    outfile.write("\n Best individual is: %s %s %s " % (str(hof[0]), hof[0].fitness, hof[0].fitness_test))
    outfile.write("\n Best individual is: %s %s %s" % (str(hof[1]), hof[1].fitness, hof[1].fitness_test))
    outfile.write("\n Best individual is: %s %s %s" % (str(hof[2]), hof[2].fitness, hof[2].fitness_test))

    sortf = sort_fitnessvalues(pop)
    for ind in sortf:
        outfile.write('\n%s;%s;%s;%s;%s;%s' %(len(ind), ind.height, ind.get_specie(), ind.fitness.values[0], ind.get_fsharing(), ind))
        #outfile.write("\n ind: %s %s %s " % (ind.fitness.values, ind.get_fsharing(), ind))

    outfile.close()
    return pop, log, hof


def run(number,problem):
    n = 1
    while n <= number:
        main(n,problem)
        n += 1

if __name__ == "__main__":
    n = 1
    while n < 30:
        #main(n,6)
        cProfile.run('print main(n, 6); print')
        n += 1