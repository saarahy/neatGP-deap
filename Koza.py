import operator
import math
import random
import csv
import numpy
import cProfile
import scipy
import funcEval
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
from numpy import genfromtxt
from neat_operators import neatGP
from ParentSelection import sort_fitnessvalues
from my_operators import safe_div, mylog



pset = gp.PrimitiveSet("MAIN", 1)

pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(safe_div, 2)
pset.addPrimitive(numpy.cos, 1)
pset.addPrimitive(numpy.sin, 1)
#pset.addPrimitive(math.exp,1)
pset.addPrimitive(mylog,1)
pset.renameArguments(ARG0='x')
#pset.addEphemeralConstant('eph',lambda: random.uniform(-1, 1))

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
    values=points[:]**4 + points[:]**3 + points[:]**2 + points[:]
    sqerrors = numpy.sum((func(points) - values)**2)
    return numpy.sqrt(sqerrors / len(points)),

def Koza(n_corr):
    direccion="./data_corridas/Koza/corrida%d/test_x.txt"
    direccion2="./data_corridas/Koza/corrida%d/train_x.txt"
    my_data = numpy.genfromtxt(direccion % n_corr, delimiter=' ')
    my_data2 = numpy.genfromtxt(direccion2 % n_corr, delimiter=' ')
    toolbox.register("evaluate", evalSymbReg, points=my_data2)
    toolbox.register("evaluate_test", evalSymbReg, points=my_data)

# def evalSymbReg(individual, points):
#     func = toolbox.compile(expr=individual)
#     sqerrors = ((func(x) - x**4 - x**3 - x**2 - x)**2 for x in points)
#     return math.fsum(sqerrors) / len(points),
#
#
# def Koza(n_corr):
#     with open("./data_corridas/Koza/corrida%d/test_x.txt" % n_corr) as spambase:
#         spamReader = csv.reader(spambase)
#         spam = [float(row[0]) for row in spamReader]
#     with open("./data_corridas/Koza/corrida%d/train_x.txt" % n_corr) as spamb:
#         spamReader2 = csv.reader(spamb)
#         spam2 = [float(row[0]) for row in spamReader2]
#     toolbox.register("evaluate", evalSymbReg, points=spam2)
#     toolbox.register("evaluate_test", evalSymbReg, points=spam)


def main(n_corr, p):
    funcEval.LS_flag = True
    Koza(n_corr)

    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genFull, min_=0, max_=3)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

    pop = toolbox.population(n=15)
    hof = tools.HallOfFame(3)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    stats_fit_test=tools.Statistics(lambda i: i.fitness_test.values)
    mstats = tools.MultiStatistics(fitness=stats_fit,size=stats_size, fitness_test=stats_fit_test)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)

    cxpb = 0.7
    mutpb = 0.3
    ngen = 10
    params = ['best_of_each_specie', 2, 'yes']
    neat_cx = False
    neat_alg = True
    neat_pelit = 0.5
    neat_h = 0.15
    funcEval.LS_flag = True
    LS_select = 1
    cont_evalf = 2500000 #contador maximo de de evaluaciones


    pop, log = algorithms.eaSimple(pop, toolbox, cxpb, mutpb, ngen, neat_alg, neat_cx, neat_h, neat_pelit, funcEval.LS_flag, LS_select, cont_evalf,pset,n_corr, p, params, stats=mstats, halloffame=hof, verbose=True)

    outfile = open('popfinal_%d_%d.txt' % (p, n_corr), 'w')

    outfile.write("\n Best individual is: %s %s %s " %( hof[0].fitness, hof[0].fitness_test, str(hof[0])))
    outfile.write("\n Best individual is: %s %s %s" % ( hof[1].fitness, hof[1].fitness_test, str(hof[1])))
    outfile.write("\n Best individual is: %s %s %s" % ( hof[2].fitness, hof[2].fitness_test, str(hof[2])))

    sortf = sort_fitnessvalues(pop)
    for ind in sortf:
        outfile.write('\n%s;%s;%s;%s;%s;%s;%s' %(len(ind), ind.height, ind.get_specie(), ind.fitness.values[0], ind.get_fsharing(), ind.fitness_test.values[0], ind))
    outfile.close()
    return pop, log, hof


def run(number,problem):
    n = 1
    while n <= number:
        main(n, problem)
        n += 1

if __name__ == "__main__":
    n = 1
    while n < 2:
        main(n, 1)
        #cProfile.run('print main(n, 1); print')
        n += 1
