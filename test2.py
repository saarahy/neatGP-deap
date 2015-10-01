import operator
import math
import random
import csv
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
# from fitness_sharing import *
# from speciation import *
# from ParentSelection import *
from neat_operators import *

def safeDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 0
def mylog(x):
    if x==0:
        return 0
    else:
        return math.log10(abs(x))

pset = gp.PrimitiveSet("MAIN", 1)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(safeDiv, 2)
pset.addPrimitive(math.cos, 1)
pset.addPrimitive(math.sin, 1)
#pset.addPrimitive(math.exp,1)
pset.addPrimitive(mylog,1)
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
    sqerrors = ((func(x) - x**4 - x**3 - x**2 - x)**2 for x in points)
    return math.fsum(sqerrors) / len(points),


with open("test_x.txt") as spambase:
    spamReader = csv.reader(spambase)
    spam = [float(row[0]) for row in spamReader]
with open("train_x.txt") as spamb:
    spamReader2 = csv.reader(spamb)
    spam2 = [float(row[0]) for row in spamReader2]
#print spam
#print [x/10. for x in range(-20,20)]

toolbox.register("evaluate", evalSymbReg, points=spam2)
toolbox.register("evaluate_test", evalSymbReg, points=spam)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=6)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

def main():
    pop = toolbox.population(n=150)
    hof = tools.HallOfFame(3)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    stats_fit_test=tools.Statistics(lambda i: i.fitness_test.values)
    mstats = tools.MultiStatistics(fitness=stats_fit,size=stats_size, fitness_test= stats_fit_test)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)
    params=['best_of_each_specie',2,'yes']
    pop, log = algorithms.eaSimple(pop, toolbox, 0.7, 0.3, 50,True,0.15,params,150,stats=mstats,halloffame=hof, verbose=True)

    outfile = open('popfinal.txt', 'w')

    outfile.write("\n Best individual is: %s %s %s " % (str(hof[0]), hof[0].fitness, hof[0].fitness_test))
    outfile.write("\n Best individual is: %s %s %s" % (str(hof[1]), hof[1].fitness, hof[1].fitness_test))
    outfile.write("\n Best individual is: %s %s %s" % (str(hof[2]), hof[2].fitness, hof[2].fitness_test))

    sortf=sort_fitnessvalues(pop)
    for ind in sortf:
        outfile.write("\n ind: %s %s %s " % (ind.fitness.values, ind.get_fsharing(), ind))

    outfile.close()
    return pop, log, hof

if __name__ == "__main__":
    main()