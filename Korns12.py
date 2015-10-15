import operator
import math
import random
import csv
import numpy
from decimal import Decimal
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
from neat_operators import neatGP
from ParentSelection import sort_fitnessvalues
from my_operators import safe_div, mylog, mypower2, mypower3, mysqrt

pset = gp.PrimitiveSet("MAIN", 2)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(safe_div, 2)
pset.addPrimitive(math.cos, 1)
pset.addPrimitive(math.sin, 1)
#pset.addPrimitive(math.exp,1)
pset.addPrimitive(mylog, 1)
pset.addPrimitive(mypower2, 1)
pset.addPrimitive(mypower3, 1)
pset.addPrimitive(mysqrt, 1)
pset.addPrimitive(math.tan, 1)
pset.addPrimitive(math.tanh, 1)
pset.addEphemeralConstant("rand101", lambda: random.uniform(-1, 1))
pset.renameArguments(ARG0='x0')
pset.renameArguments(ARG1='x1')
pset.renameArguments(ARG2='x2')
pset.renameArguments(ARG3='x3')
pset.renameArguments(ARG4='x4')

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("FitnessTest", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, fitness_test=creator.FitnessTest)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, min_=1, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)


def evalSymbRegKorns(individual, points):
    func = toolbox.compile(expr=individual)
    sqerrors = []
    for elem in range(len(points[0])):
        try:
            sqerrors.append((func(float(points[0][elem]), float(points[4][elem]))-(2.0-(2.1 * (math.cos(9.8 * float(points[0][elem]))*math.sin(1.3 * float(points[4][elem]))))))**2)
        except Exception:
            sqerrors.append((Decimal(func(float(points[0][elem]), float(points[0][elem])))-(Decimal(2.0)-(Decimal(2.1) * (Decimal(math.cos(Decimal(9.8) * Decimal(points[0][elem])))*Decimal(math.sin(Decimal(1.3) * Decimal(points[4][elem])))))))**2)
    return math.fsum(sqerrors) / len(points[0]),


def Korns(n_corr):
    with open("./data_corridas/Korns/corrida%d/test_x.txt" % n_corr) as spambase:
        spamReader = csv.reader(spambase,  delimiter=' ', skipinitialspace=True)
        Matrix = [[], [], [], [], []]
        for row in spamReader:
            Matrix[0].append(Decimal(row[0]))
            Matrix[1].append(Decimal(row[1]))
            Matrix[2].append(Decimal(row[2]))
            Matrix[3].append(Decimal(row[3]))
            Matrix[4].append(Decimal(row[4]))
        spam = Matrix
    with open("./data_corridas/Korns/corrida%d/train_x.txt" % n_corr) as spamb:
        spamReader2 = csv.reader(spamb,  delimiter=' ', skipinitialspace=True)
        Matrix = [[], [], [], [], []]
        for row in spamReader2:
            Matrix[0].append(Decimal(row[0]))
            Matrix[1].append(Decimal(row[1]))
            Matrix[2].append(Decimal(row[2]))
            Matrix[3].append(Decimal(row[3]))
            Matrix[4].append(Decimal(row[4]))
        spam2 = Matrix
    toolbox.register("evaluate", evalSymbRegKorns, points=spam2)
    toolbox.register("evaluate_test", evalSymbRegKorns, points=spam)


def main(n_corr, p):
    Korns(n_corr)

    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genFull, min_=0, max_=3)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(3)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    stats_fit_test = tools.Statistics(lambda i: i.fitness_test.values)
    mstats = tools.MultiStatistics(fitness=stats_fit,size=stats_size, fitness_test=stats_fit_test)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)
    params = ['best_of_each_specie', 2, 'yes']
    neatcx = True
    neat = True
    pelit = 0.6
    pop, log = algorithms.eaSimple(pop, toolbox, 0.7, 0.3, 100, neat, neatcx, 0.15, pelit, n_corr, p, params, stats=mstats, halloffame=hof, verbose=True)

    outfile = open('popfinal_%d_%d.txt' % (p, n_corr), 'w')

    outfile.write("\n Best individual is: %s %s %s " % (str(hof[0]), hof[0].fitness, hof[0].fitness_test))
    outfile.write("\n Best individual is: %s %s %s" % (str(hof[1]), hof[1].fitness, hof[1].fitness_test))
    outfile.write("\n Best individual is: %s %s %s" % (str(hof[2]), hof[2].fitness, hof[2].fitness_test))

    sortf = sort_fitnessvalues(pop)
    for ind in sortf:
        outfile.write("\n ind: %s %s %s " % (ind.fitness.values, ind.get_fsharing(), ind))

    outfile.close()
    return pop, log, hof


def run(number, problem):
    n = 1
    while n <= number:
        main(n, problem)
        n += 1


if __name__ == "__main__":
    n = 1
    while n < 30:
        main(n, 9)
        n += 1
