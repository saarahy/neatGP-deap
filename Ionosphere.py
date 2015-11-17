import random
import operator
import csv
import itertools

import numpy as np

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
import my_operators as mo

direccion="./data_corridas/Ionosphere/ionosphere.txt"
with open(direccion) as spambase:
    # spamReader = csv.reader(spambase)
    # spam = list(list(elem for elem in row) for row in spamReader)
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

# defined a new primitive set for strongly typed GP
pset = gp.PrimitiveSet("MAIN", 34)

# Define a new if-then-else function
def if_then_else(input, output1, output2):
    if input: return output1
    else: return output2

pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(mo.safe_div, 2)
pset.addPrimitive(np.sin, 1)
pset.addPrimitive(np.cos, 1)
pset.addPrimitive(mo.mysqrt, 1)
pset.addPrimitive(np.abs, 1)

#pset.addPrimitive(if_then_else, 3)
pset.renameArguments(ARG0='x0',ARG1='x1', ARG2='x2', ARG3='x3', ARG4='x4', ARG5='x5' , ARG6='x6' , ARG7='x7' , ARG8='x8' , ARG9='x9')

creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("FitnessTest", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax, fitness_test=creator.FitnessTest)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def evalSpambase(individual, test):
    func = toolbox.compile(expr=individual)
    if test:
        long=int(len(Matrix.T)*.7)
    else:
        long=int(len(Matrix.T)*.3)
    spam_samp = random.sample(Matrix.T, long)
    vector = [data[34] for data in spam_samp]
    result = np.sum((func(*np.asarray(spam_samp).T[:34]) - vector)**2)
    return result/long,
    
toolbox.register("evaluate", evalSpambase, test=False)
toolbox.register("evaluate_test", evalSpambase, test=True)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

def main(n_corr, p):
    pop = toolbox.population(n=200)
    hof = tools.HallOfFame(1)
    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    stats_fit_test = tools.Statistics(lambda i: i.fitness_test.values)
    mstats = tools.MultiStatistics(fitness=stats_fit,size=stats_size, fitness_test=stats_fit_test)
    mstats.register("avg", np.mean)
    mstats.register("std", np.std)
    mstats.register("min", np.min)
    mstats.register("max", np.max)

    params = ['best_of_each_specie', 2, 'yes']
    neatcx = True
    neat = True
    pelit = 0.5
    algorithms.eaSimple(pop, toolbox, 0.7, 0.3, 100, neat, neatcx, 0.15, pelit, n_corr, p, params, stats=mstats, halloffame=hof, verbose=True)

    return pop, mstats, hof

if __name__ == "__main__":
    n = 1
    p = 10
    while n < 31:
        main(n, p)
        n += 1
